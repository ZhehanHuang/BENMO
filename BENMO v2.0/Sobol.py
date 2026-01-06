# ============================================================
# Step 1) Imports & Global Config (与 OAT 输出结构一致)
# ============================================================
import os
import json
import numpy as np
import pandas as pd
import subprocess
from copy import deepcopy
from tqdm import tqdm

import re
from SALib.sample import sobol as sobol_sample
from SALib.analyze import sobol

# -------------------------
# 1.1 路径配置：与你 OAT 一致
# -------------------------
OAT_SUMMARY_CSV = "./sensitivity_results_20/sensitivity_summary.csv"
PARAMETER_FILE  = "./parameters.json"
OBSERVE_FILE    = "./database/observe_data_20.xlsx"
BASE_SIM_DIR = "./baseline_results"

# 与 OAT 一致的输出文件命名规则
VARIABLES = ["PO4"]

# 输出目录
OUT_DIR = "./sobol_results"
os.makedirs(OUT_DIR, exist_ok=True)

# -------------------------
# 1.2 参数写入规则：与你 OAT 一致
# -------------------------
PARAM_SHOULD_BE_ARRAY = {
    "FEED_NH3": True,
    "FEED_NO3": True,
    "FEED_ON": True,
    "a": True,
    "b": True,
    "c": True,
    "d": True,
    "SOD": True
}

# -------------------------
# 1.3 fuzzy matching 与时间聚合：严格照你 plot_with_fuzzy_matching
# -------------------------
HOURS_PER_WEEK = 24 * 7        # 你原函数写的是 24*7
TIME_WINDOW_HOURS = 720        # 你原函数默认 720
N_ZONES = 20                   # 你原函数固定 20

# 若匹配对太少，NSE 不稳定；给一个最低门槛（不改变匹配逻辑，只是输出控制）
MIN_MATCH_PAIRS = 5

# -------------------------
# 1.4 Sobol 采样设置
# -------------------------
SOBOL_N = 32                   # 可先小一点调通；正式跑再增大（如 512/1024）
CALC_SECOND_ORDER = False      # True 会显著增加模型评估次数

# 参数范围：默认基线 ±20%（你可按机理改）
BOUND_FRAC = 0.2

# OAT Top-K 参数
TOPK = 20

# OAT 聚合方式：合并 ±10% 的两条记录（推荐 mean）
OAT_AGG = "mean"               # "mean" 或 "max"

# 二阶段Sobol的参数基础
USE_PREVIOUS_SOBOL = True             # 是否启用二阶段筛选
PREV_SOBOL_DIR = "./sobol_results"     # n=16 结果所在目录
PREV_SOBOL_N = 16                      # 标识 n=16
TOP_A = 10                              # 你要选的前 a 个参数（如 8 或 10）
PREV_SOBOL_METRIC = "ST"               # 用 ST 排序（推荐）

# ============================================================
# Step 2) 从 OAT 输出提取各营养盐 Top-20 参数（各自不一致）
# ============================================================
def load_oat_aggregate_table(oat_csv: str, nutrients: list[str], agg: str = "mean") -> pd.DataFrame:
    """
    返回 df_agg: index=param, columns=nutrients
    其中每个元素为该 param 对该 nutrient 的 OAT 响应强度（合并±0.1）
    """
    df = pd.read_csv(oat_csv)

    required = {"param", "change"} | set(nutrients)
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"OAT 文件缺少列：{missing}; 现有列={df.columns.tolist()}")

    if agg == "mean":
        df_agg = df.groupby("param")[nutrients].mean()
    elif agg == "max":
        df_agg = df.groupby("param")[nutrients].max()
    else:
        raise ValueError("agg must be 'mean' or 'max'")

    return df_agg


def get_topk_params_per_nutrient(df_agg: pd.DataFrame, topk: int) -> dict:
    """
    对 df_agg 的每一列（营养盐）分别取 TopK 参数
    返回：{nutrient: [param1, param2, ...]}
    """
    topk_dict = {}
    for nut in df_agg.columns:
        topk_dict[nut] = df_agg[nut].sort_values(ascending=False).head(topk).index.tolist()
    return topk_dict

# ============================================================
# Step 2.5) 从已有 Sobol 结果中筛选 Top-a 参数
# ============================================================
def load_topa_from_previous_sobol(
    nutrient: str,
    sobol_dir: str,
    prev_n: int,
    top_a: int,
    metric: str = "ST"
) -> list[str]:
    """
    从已有 Sobol 结果中读取 Top-a 参数
    """
    # 匹配你当前的输出命名规则
    pattern = f"sobol_{nutrient}_Top*_fuzzyNSE_OAT*_N{prev_n}_B*.csv"
    files = [f for f in os.listdir(sobol_dir) if f.startswith(f"sobol_{nutrient}") and f"_N{prev_n}_" in f]

    if not files:
        raise FileNotFoundError(
            f"未在 {sobol_dir} 中找到 {nutrient} 的 Sobol n={prev_n} 结果文件"
        )

    # 若有多个，取最新的
    files.sort()
    sobol_csv = os.path.join(sobol_dir, files[-1])

    df = pd.read_csv(sobol_csv)

    if metric not in df.columns:
        raise ValueError(f"Sobol 文件中不包含列 {metric}")

    top_params = (
        df.sort_values(metric, ascending=False)
          .head(top_a)["param"]
          .tolist()
    )

    print(f"[INFO] Using Top-{top_a} parameters from previous Sobol (n={prev_n}):")
    print(top_params)

    return top_params

# ============================================================
# Step 3) Sobol problem 构造：使用基线参数.json 的值构造 bounds
# ============================================================
def load_baseline_parameters(param_file: str) -> dict:
    with open(param_file, "r", encoding="utf-8") as f:
        return json.load(f)


def build_problem_from_baseline(
    baseline_param: dict,
    param_names: list[str],
    frac: float = 0.2
) -> dict:
    """
    SALib problem dict:
      - num_vars
      - names
      - bounds: [[lo, hi], ...]
    bounds 默认用 基线 ± frac
    """
    bounds = []
    for p in param_names:
        if p not in baseline_param:
            raise KeyError(f"参数 {p} 不在 parameters.json 中")

        v = baseline_param[p]
        base_scalar = v[0] if isinstance(v, list) else v
        base_scalar = float(base_scalar)

        lo = base_scalar * (1.0 - frac)
        hi = base_scalar * (1.0 + frac)

        # 基本健壮性处理
        if hi == lo:
            hi = lo + 1e-12
        if hi < lo:
            lo, hi = hi, lo

        bounds.append([lo, hi])

    return {"num_vars": len(param_names), "names": param_names, "bounds": bounds}

# ============================================================
# Step 4) 单次模型运行：写 parameters.json -> python main.py -> 读取输出 dict（与 OAT 一致）
# ============================================================
def write_parameters_json(
    baseline_param: dict,
    names: list[str],
    x: np.ndarray,
    out_file: str
):
    """
    将 Sobol 样本 x 写入 parameters.json
    数组扩展规则严格遵循 OAT 的 PARAM_SHOULD_BE_ARRAY
    """
    new_param = deepcopy(baseline_param)
    for name, val in zip(names, x):
        if PARAM_SHOULD_BE_ARRAY.get(name, False):
            new_param[name] = [float(val)] * 24
        else:
            new_param[name] = float(val)

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(new_param, f, indent=2, ensure_ascii=False)


def run_main_and_get_y(nutrient: str) -> float:
    """
    运行 main_20.py，让 main 直接输出 SOBOL_Y=...
    这样 Sobol 不依赖 npy 文件（main 的 save 已注释时仍可运行）。
    """
    # 你已在 main 中实现 sobol 模式输出，这里只负责调用与解析
    cmd = ["python", "main_20.py", "--no-gui", "--sobol-var", nutrient]

    r = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False
    )

    out = r.stdout.decode("utf-8", errors="ignore")
    err = r.stderr.decode("utf-8", errors="ignore")

    if r.returncode != 0:
        raise RuntimeError(
            "main_20.py 运行失败\n"
            f"CMD: {' '.join(cmd)}\n"
            f"STDOUT:\n{out}\n"
            f"STDERR:\n{err}\n"
        )

    m = re.search(r"SOBOL_Y\s*=\s*([-+0-9.eE]+)", out)
    if not m:
        # 有些实现输出 SOBOL_Y=xxx（无空格），这里也兼容
        m = re.search(r"SOBOL_Y=([-+0-9.eE]+)", out)

    if not m:
        raise RuntimeError(
            "未在 main_20.py 输出中找到 SOBOL_Y\n"
            f"STDOUT:\n{out}\n"
            f"STDERR:\n{err}\n"
        )

    return float(m.group(1))


def load_outputs_as_simulated_dict(variables: list[str]) -> dict:
    """
    读取 {VAR}_simulated.npy，构造 simulated_data_dict（与 OAT 一致）
    """
    simulated = {}
    for var in variables:
        fn = os.path.join(BASE_SIM_DIR, f"{var.upper()}_simulated_test.npy")
        if not os.path.exists(fn):
            raise RuntimeError(f"找不到输出文件 {fn}，请确认 main.py 输出命名/路径与 OAT 一致。")
        simulated[var] = np.load(fn)
    return simulated

# ============================================================
# Step 5) fuzzy matching + fuzzy-NSE：严格复刻 OAT 的匹配数据流
# ============================================================
def fuzzy_nse_from_simulated_dict(
    simulated_data_dict: dict,
    observe_df: pd.DataFrame,
    var_name: str,
    time_window_hours: int = TIME_WINDOW_HOURS,
    hours_per_week: int = HOURS_PER_WEEK,
    n_zones: int = N_ZONES,
    min_pairs: int = MIN_MATCH_PAIRS
) -> float:
    """
    输入结构与 OAT 一致：
      simulated_data_dict[var_name] 为 sim_array
      observe_df 来源于 observe_data.xlsx
    匹配规则严格照 plot_with_fuzzy_matching：
      - 将 sim_array reshape 为 (num_weeks, hours_per_week, 20)
      - weekly_means = mean(axis=1)
      - 对每条观测，在窗口内选 abs(sim-obs) 最小的候选周均值
    输出：
      pooled fuzzy-NSE（跨所有 zone 的匹配点拼接后计算 NSE）
    """
    sim_array = np.array(simulated_data_dict[var_name])

    num_weeks = sim_array.shape[0] // hours_per_week
    if num_weeks <= 0:
        return np.nan

    sim_array = sim_array[:num_weeks * hours_per_week].reshape(num_weeks, hours_per_week, n_zones)
    weekly_means = sim_array.mean(axis=1)  # (weeks, zones)

    col = var_name.lower()
    if col not in observe_df.columns:
        return np.nan

    matched_obs_all = []
    matched_sim_all = []

    for zone in range(n_zones):
        df_zone = observe_df[observe_df["zone"] == zone]

        matched_obs_vals = []
        matched_sim_vals = []

        for _, row in df_zone.iterrows():
            obs_time = int(row["timestep"])
            obs_val = row[col]
            if pd.isna(obs_val):
                continue

            sim_candidates = []
            for week_idx in range(num_weeks):
                sim_time = week_idx * hours_per_week
                if abs(sim_time - obs_time) <= time_window_hours:
                    sim_val = weekly_means[week_idx, zone]
                    sim_candidates.append((abs(sim_val - obs_val), float(sim_val)))

            if sim_candidates:
                _, sim_val_closest = min(sim_candidates, key=lambda x: x[0])
                matched_obs_vals.append(float(obs_val))
                matched_sim_vals.append(sim_val_closest)

        matched_obs_all.extend(matched_obs_vals)
        matched_sim_all.extend(matched_sim_vals)

    # NSE 计算
    if len(matched_obs_all) < max(2, min_pairs):
        return np.nan

    obs = np.array(matched_obs_all, dtype=float)
    sim = np.array(matched_sim_all, dtype=float)

    denom = np.sum((obs - np.mean(obs)) ** 2)
    if denom <= 0:
        return np.nan

    nse = 1.0 - np.sum((obs - sim) ** 2) / denom
    return float(nse)

# ============================================================
# Step 6) Sobol 主函数：对每个营养盐分别用其 Top-20 做 Sobol
# ============================================================
def run_sobol_for_one_nutrient(
    nutrient: str,
    top_params: list[str],
    baseline_param: dict,
    observe_df: pd.DataFrame,
    bound_frac: float = BOUND_FRAC,
    sobol_n: int = SOBOL_N,
    calc_second_order: bool = CALC_SECOND_ORDER
) -> pd.DataFrame:
    """
    对某个 nutrient，使用其 top_params 作为 Sobol 参数维度
    输出 DataFrame: param, S1, ST, conf intervals
    """
    # 6.1 problem 构造
    problem = build_problem_from_baseline(baseline_param, top_params, frac=bound_frac)

    # 6.2 采样矩阵 X（使用新接口，替代 saltelli.sample）
    X = sobol_sample.sample(problem, N=sobol_n, calc_second_order=calc_second_order)

    # 6.2.1 强校验：防止 N 太小或 second_order 不一致导致 sobol.analyze 报错
    D = problem["num_vars"]
    expected = sobol_n * (D + 2) if not calc_second_order else sobol_n * (2 * D + 2)
    if X.shape[0] != expected:
        raise RuntimeError(
            f"采样矩阵行数不符合 Sobol 要求：X.shape[0]={X.shape[0]}，期望={expected}。"
            f"请检查 N={sobol_n} 与 calc_second_order={calc_second_order}。"
        )

    # 6.3 模型评估得到 Y（直接从 main 输出 SOBOL_Y）
    Y = np.zeros(X.shape[0], dtype=float)

    for i in tqdm(
            range(X.shape[0]),
            desc=f"Sobol eval ({nutrient})",
            ncols=100
    ):
        # 写参数（与 OAT 一致：仍写到 ./parameters.json）
        write_parameters_json(baseline_param, problem["names"], X[i, :], PARAMETER_FILE)

        # 运行 main 并获取目标函数值（标量）
        y = run_main_and_get_y(nutrient)

        if np.isnan(y):
            y = -1e6
        Y[i] = y

        tqdm.write(f"[{nutrient}] Y[{i}] = {y:.4f}")

    # 6.4 Sobol 指数分析
    Si = sobol.analyze(problem, Y, calc_second_order=calc_second_order, print_to_console=False)

    # 6.5 输出结果表
    out = pd.DataFrame({
        "param": problem["names"],
        "S1": Si["S1"],
        "S1_conf": Si["S1_conf"],
        "ST": Si["ST"],
        "ST_conf": Si["ST_conf"],
    }).sort_values("ST", ascending=False)

    return out

# ============================================================
# Step 7) main：串起来（变量连贯，端到端可跑）
# ============================================================
def main():
    # 7.1 读 OAT 聚合表（合并 ±10% 两行）
    df_agg = load_oat_aggregate_table(OAT_SUMMARY_CSV, VARIABLES, agg=OAT_AGG)

    # 7.2 各营养盐 Sobol 参数集合（支持二阶段）
    topk_dict = {}

    for nut in VARIABLES:
        if USE_PREVIOUS_SOBOL:
            topk_dict[nut] = load_topa_from_previous_sobol(
                nutrient=nut,
                sobol_dir=PREV_SOBOL_DIR,
                prev_n=PREV_SOBOL_N,
                top_a=TOP_A,
                metric=PREV_SOBOL_METRIC
            )
        else:
            # 回退到 OAT Top-K
            df_agg = load_oat_aggregate_table(OAT_SUMMARY_CSV, VARIABLES, agg=OAT_AGG)
            topk_dict = get_topk_params_per_nutrient(df_agg, TOPK)

    # 7.3 读基线参数与观测数据（观测读一次即可；不影响结构一致性）
    baseline_param = load_baseline_parameters(PARAMETER_FILE)
    observe_df = pd.read_excel(OBSERVE_FILE)

    # 7.4 对每个营养盐分别 Sobol（各自用各自的 Top-20）
    for nut in VARIABLES:
        print("\n" + "=" * 70)
        print(f"Start Sobol for {nut} with Top-{TOPK} parameters (OAT-{OAT_AGG})")
        print("Params:", topk_dict[nut])

        df_sobol = run_sobol_for_one_nutrient(
            nutrient=nut,
            top_params=topk_dict[nut],
            baseline_param=baseline_param,
            observe_df=observe_df,
            bound_frac=BOUND_FRAC,
            sobol_n=SOBOL_N,
            calc_second_order=CALC_SECOND_ORDER
        )

        out_csv = os.path.join(
            OUT_DIR,
            f"sobol_{nut}_Top{TOPK}_fuzzyNSE_OAT{OAT_AGG}_N{SOBOL_N}_B{BOUND_FRAC}.csv"
        )
        df_sobol.to_csv(out_csv, index=False, encoding="utf-8-sig")
        print(f"[{nut}] saved: {out_csv}")
        print(df_sobol.head(10).to_string(index=False))

if __name__ == "__main__":
    main()
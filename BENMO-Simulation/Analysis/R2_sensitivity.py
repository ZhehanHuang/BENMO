import os
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score

# ========== 配置 ==========
baseline_dir = "baseline_results"
sensitivity_dir = "sensitivity_results_8groups"
observe_file = "database/observe_data_20.xlsx"
output_file = "sensitivity_analysis_output/sensitivity_5_source_by_zone_8groups.csv"

all_variables = ["nh4", "no3", "on", "po4", "op", "pp"]
r2_variables = ["nh4", "no3", "po4"]
hours_per_week = 24 * 7
time_window_hours = 360  # fuzzy 匹配范围 ±360 小时

# ========== 加载观测数据 ==========
observe_df = pd.read_excel(observe_file)

# ========== 加载基线模拟结果 ==========
baseline_data = {}
for var in all_variables:
    path = os.path.join(baseline_dir, f"{var.upper()}_simulated_test.npy")
    if not os.path.exists(path):
        print(f"[WARNING] 缺失基线文件：{path}")
        continue
    arr = np.load(path)
    num_weeks = arr.shape[0] // hours_per_week
    weekly = arr[:num_weeks * hours_per_week].reshape(num_weeks, hours_per_week, 20).mean(axis=1)
    baseline_data[var] = weekly

# ========== Fuzzy R² 计算函数 ==========
def fuzzy_match_r2(obs_df, var_name, baseline_weekly, sim_weekly, zone):
    obs_vals, sim_vals, base_vals = [], [], []
    num_weeks = baseline_weekly.shape[0]
    for _, row in obs_df.iterrows():
        t_obs = int(row["timestep"])
        y_obs = row[var_name]
        candidates = []
        for w in range(num_weeks):
            t_sim = w * hours_per_week
            if abs(t_sim - t_obs) <= time_window_hours:
                sim_y = sim_weekly[w, zone]
                base_y = baseline_weekly[w, zone]
                candidates.append((abs(sim_y - y_obs), sim_y, base_y))
        if candidates:
            _, sim_closest, base_closest = min(candidates, key=lambda x: x[0])
            obs_vals.append(y_obs)
            sim_vals.append(sim_closest)
            base_vals.append(base_closest)

    if len(obs_vals) >= 2:
        r2_base = r2_score(obs_vals, base_vals)
        r2_sim = r2_score(obs_vals, sim_vals)
        return (r2_sim - r2_base) / r2_base
    else:
        return np.nan

# ========== 遍历扰动结果文件 ==========
results = []
for fname in os.listdir(sensitivity_dir):
    if not fname.endswith(".npy"):
        continue
    parts = fname.replace(".npy", "").split("_")
    if len(parts) < 3:
        continue
    var = parts[0].lower()
    direction = parts[-1].lower()
    param = "_".join(parts[1:-1])
    if var not in all_variables:
        continue

    sim_path = os.path.join(sensitivity_dir, fname)
    sim_arr = np.load(sim_path)
    num_weeks = sim_arr.shape[0] // hours_per_week
    sim_weekly = sim_arr[:num_weeks * hours_per_week].reshape(num_weeks, hours_per_week, 20).mean(axis=1)
    baseline_weekly = baseline_data.get(var)
    if baseline_weekly is None:
        continue

    for zone in range(20):
        # === 平均绝对偏差 ===
        mad = np.mean(np.abs(sim_weekly[:, zone] - baseline_weekly[:, zone]))

        # === fuzzy R²变化 ===
        if var in r2_variables:
            df_zone = observe_df[observe_df['zone'] == zone].dropna(subset=[var])
            r2_delta = fuzzy_match_r2(df_zone, var, baseline_weekly, sim_weekly, zone)
        else:
            r2_delta = np.nan

        results.append({
            "param": param,
            "direction": direction,
            "zone": zone,
            "variable": var,
            "mean_abs_diff": mad,
            "r2_change": r2_delta,
            "sensitivity": r2_delta * 10 if direction == "increase" else -r2_delta * 10,
        })

# ========== 输出结果 ==========
df_result = pd.DataFrame(results)
df_result.to_csv(output_file, index=False)
print(f"[✓] 分析完成，结果已保存至：{output_file}")
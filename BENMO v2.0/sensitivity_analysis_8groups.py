#!/usr/bin/env python
# group_sensitivity_10pct.py
# ------------------------------------------------------------
# 8 类整体 ±10 % 敏感性分析（合并养殖）— Windows-safe 版本
# ------------------------------------------------------------
import os
import re
import json
import shutil
import subprocess
from multiprocessing import Pool, freeze_support
from pathlib import Path

import numpy as np
import pandas as pd

# ────────── 基础配置 ──────────
VARIABLES      = ["NH4", "NO3", "ON", "PO4", "OP", "PP"]
BASELINE_DIR   = "baseline_results"
OUTPUT_DIR     = "sensitivity_results_8groups"
PARAM_JSON     = "parameters.json"
SIM_SCRIPT     = "main_20.py"
MAX_PROC       = 8

Path(OUTPUT_DIR).mkdir(exist_ok=True)

# ────────── 1. 分类规则（合并养殖） ──────────
CLASS_RULES = {
    "Aquaculture"      : [r"_f\b", r"fish", r"feed", r"_sh\b", r"shell", r"_ma\b", r"macro"],
    "Natural_Bio"      : [r"_phy\b", r"phy", r"_pz\b", r"_dz\b", r"zoo", r"grz"],
    "N_Nutrient"       : [r"nh4", r"no3", r"_n\b", r"kn_", r"nc_", r"kc_nit"],
    "P_Nutrient"       : [r"po4", r"_p\b", r"kp_", r"pc_", r"pp\b", r"phosph"],
    "River"      : [r"RIVER_FACTOR"],
    "Outersea"   : [r"OUTERSEA_FACTOR"],
    "Groundwater": [r"GW_FACTOR"],
    "Atmosphere" : [r"ATM_FACTOR"],
    "PointPond"  : [r"PS_FACTOR", r"POND_FACTOR"],
}

# ────────── 2. 构建 group_map ──────────
with open(PARAM_JSON) as f:
    ALL_PARAMS = list(json.load(f).keys())

group_map = {g: [] for g in CLASS_RULES}
for p in ALL_PARAMS:
    for grp, pats in CLASS_RULES.items():
        if any(re.search(pt, p, re.IGNORECASE) for pt in pats):
            group_map[grp].append(p)
            break

# ────────── 3. patch main_20.py ──────────
def patch_main_py(dst: Path):
    patch = (
        "import json, os\n"
        "if os.path.exists('parameters.json'):\n"
        "    p = json.load(open('parameters.json'))\n"
        "    globals().update({k:v for k,v in p.items() if k.endswith('_FACTOR')})\n\n"
    )
    text = dst.read_text(encoding="utf-8")
    dst.write_text(patch + text, encoding="utf-8")

# ────────── 4. 运行单个任务 ──────────
def run_one(args):
    grp, delta, base_params = args
    tag = f"{grp}_{'plus' if delta>0 else 'minus'}"
    wdir = Path(OUTPUT_DIR) / f"run_{tag}"

    # 彻底清理旧文件/目录
    if wdir.exists():
        shutil.rmtree(wdir)
    wdir.mkdir()

    # 确保 baseline_results 目录存在，以供 main_20.py 输出
    (wdir / BASELINE_DIR).mkdir()

    # 复制脚本和数据
    shutil.copy(SIM_SCRIPT, wdir)
    patch_main_py(wdir / SIM_SCRIPT)
    shutil.copytree("database", wdir / "database", dirs_exist_ok=True)
    shutil.copytree("grd", wdir / "grd", dirs_exist_ok=True)

    # 写入修改后的 parameters.json
    params = base_params.copy()
    for key in group_map.get(grp, []):
        if key in params:
            if isinstance(params[key], list):
                params[key] = [v * (1 + delta) for v in params[key]]
            else:
                params[key] = params[key] * (1 + delta)
    with open(wdir / PARAM_JSON, "w") as f:
        json.dump(params, f, indent=2)

    # 执行模拟
    res = subprocess.run(
        ["python", SIM_SCRIPT],
        cwd=wdir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        errors="replace"
    )
    if res.returncode != 0:
        print(res.stdout)
        raise RuntimeError(f"Simulation failed for {tag}")

    # 收集并复制输出
    data = {}
    for v in VARIABLES:
        src = wdir / f"{BASELINE_DIR}/{v}_simulated_test.npy"
        dst = Path(OUTPUT_DIR) / f"{v}_{tag}.npy"
        shutil.copy(src, dst)
        data[v] = np.load(src)
    return tag, data

# ────────── 5. 主流程 ───────────────────────────────
def main():
    # 加载基线输出
    baseline_out = {
        v: np.load(f"{BASELINE_DIR}/{v}_simulated_test.npy")
        for v in VARIABLES
    }

    # 准备任务列表
    with open(PARAM_JSON) as f:
        base_params = json.load(f)
    tasks = [(grp, d, base_params) for grp in CLASS_RULES for d in (0.1, -0.1)]

    # 并行执行
    summary = []
    with Pool(min(MAX_PROC, len(tasks))) as pool:
        for tag, data in pool.imap_unordered(run_one, tasks):
            diffs = {v: float(np.mean(np.abs(data[v] - baseline_out[v])))
                     for v in VARIABLES}
            diffs["tag"] = tag
            summary.append(diffs)

    # 保存汇总
    pd.DataFrame(summary).to_csv(
        Path(OUTPUT_DIR) / "sensitivity_summary_group.csv", index=False)
    print("✅ Group sensitivity done. Results in", OUTPUT_DIR)

if __name__ == "__main__":
    freeze_support()
    main()

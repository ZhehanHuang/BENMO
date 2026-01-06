import os
import json
import numpy as np
import pandas as pd
import shutil
import subprocess
from multiprocessing import Pool
from figure_plot import plot_with_fuzzy_matching

# === Configurations ===
VARIABLES = ["NH4", "NO3", "ON", "PO4", "OP", "PP"]
PARAMETER_FILE = "parameters.json"
BASELINE_DIR = "baseline_results"
OUTPUT_DIR = "sensitivity_results_20"
MAX_PROCESSES = 8  # Safe default
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Load baseline simulation outputs ===
def load_baseline_outputs():
    baseline = {}
    for var in VARIABLES:
        path = os.path.join(BASELINE_DIR, f"{var.upper()}_simulated_test.npy")
        baseline[var] = np.load(path)
    return baseline

# === Compute absolute average error (used as R² delta proxy) ===
def compute_difference(baseline, current):
    diff = {}
    for var in VARIABLES:
        diff[var] = np.mean(np.abs(current[var] - baseline[var]))
    return diff

# === Run main_24.py in a temporary isolated directory ===
def run_simulation(param, new_value, tag):
    work_dir = os.path.join(OUTPUT_DIR, f"run_{tag}")
    os.makedirs(work_dir, exist_ok=True)

    # Copy required files
    for file in ["main_20.py", "BENMO_20.py", "figure_plot.py"]:
        shutil.copy(file, work_dir)
    shutil.copytree("database", os.path.join(work_dir, "database"), dirs_exist_ok=True)
    shutil.copytree("grd", os.path.join(work_dir, "grd"), dirs_exist_ok=True)

    # Create parameters.json
    with open(PARAMETER_FILE, 'r') as f:
        parameters = json.load(f)
    if isinstance(parameters.get(param), list):
        parameters[param] = [new_value] * 24
    else:
        parameters[param] = new_value
    with open(os.path.join(work_dir, "parameters.json"), 'w') as f:
        json.dump(parameters, f, indent=2)

    # Create baseline_results/ inside work dir to match main_24.py save location
    os.makedirs(os.path.join(work_dir, "baseline_results"), exist_ok=True)

    # Run simulation
    result = subprocess.run(["python", "main_20.py"], cwd=work_dir,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            encoding="utf-8", errors="replace")

    # Collect outputs
    sim_data = {}
    for var in VARIABLES:
        src = os.path.join(work_dir, "baseline_results", f"{var.upper()}_simulated_test.npy")
        if not os.path.exists(src):
            print(f"[ERROR] Missing output: {src}")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            raise RuntimeError(f"模拟失败，输出文件缺失：{src}")
        dest = os.path.join(OUTPUT_DIR, f"{var.upper()}_{tag}.npy")
        shutil.copy(src, dest)
        sim_data[var] = np.load(src)

    return sim_data

# === Task executed in parallel ===
def sensitivity_task(args):
    param, delta, base_value, baseline_outputs = args
    tag = f"{param}_{'plus' if delta > 0 else 'minus'}"
    new_value = base_value * (1 + delta)
    print(f"[INFO] Running: {tag} = {new_value}")
    result_data = run_simulation(param, new_value, tag)
    plot_with_fuzzy_matching(result_data, "database/observe_data_20.xlsx", show_plot=False, save_plot=False)
    error_diff = compute_difference(baseline_outputs, result_data)
    return {"param": param, "change": delta, **error_diff}

# === Main analysis function ===
def run_sensitivity_analysis():
    with open(PARAMETER_FILE, 'r') as f:
        params = json.load(f)

    baseline_outputs = load_baseline_outputs()
    tasks = []

    for param, value in params.items():
        base_val = value[0] if isinstance(value, list) else value
        for delta in [+0.1, -0.1]:
            tasks.append((param, delta, base_val, baseline_outputs))

    with Pool(processes=min(MAX_PROCESSES, len(tasks))) as pool:
        results = pool.map(sensitivity_task, tasks)

    df = pd.DataFrame(results)
    df.to_csv(os.path.join(OUTPUT_DIR, "sensitivity_summary.csv"), index=False)
    print("[DONE] 敏感性分析已完成。结果保存在：", OUTPUT_DIR)

if __name__ == "__main__":
    run_sensitivity_analysis()

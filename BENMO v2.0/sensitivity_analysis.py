import os
import json
import numpy as np
import pandas as pd
from figure_plot import plot_with_fuzzy_matching
from shutil import copyfile
import argparse

# ------------------------
# 用户配置
# ------------------------
BASE_SIM_DIR = "./baseline_results"
OBSERVE_FILE = "./database/observe_data.xlsx"
VARIABLES = ["NH4", "NO3", "ON", "PO4", "OP", "PP"]
PARAMETER_FILE = "./parameters.json"  # 存储参数列表及其当前值

# 参数维度设定（True 表示需要扩展为数组，False 表示保持标量）
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

# 输出目录
OUTPUT_DIR = "sensitivity_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------
# 载入基线 R2
# ------------------------
def load_baseline_r2():
    base_r2 = {}
    for var in VARIABLES:
        result = np.load(os.path.join(BASE_SIM_DIR, f"{var.upper()}_simulated_test.npy"))
        base_r2[var] = result
    return base_r2

# ------------------------
# 替换参数值并重新运行模拟
# ------------------------
def run_simulation_with_param_change(param_name, new_value):
    # 模拟参数文件注入
    with open(PARAMETER_FILE, 'r') as f:
        param_data = json.load(f)

    if PARAM_SHOULD_BE_ARRAY.get(param_name, False):
        param_data[param_name] = [new_value] * 24
    else:
        param_data[param_name] = new_value

    with open(PARAMETER_FILE, 'w') as f:
        json.dump(param_data, f, indent=2)

    cmd = f"python main.py"
    os.system(cmd)

    result = {}
    for var in VARIABLES:
        filename = f"{var.upper()}_simulated.npy"
        if not os.path.exists(filename):
            raise RuntimeError(f"模拟失败：找不到输出文件 {filename}")
        result[var] = np.load(filename)
    return result

# ------------------------
# 比较 R2 结果
# ------------------------
def compute_r2_deltas(baseline_r2, perturbed_r2):
    r2_deltas = {}
    for var in VARIABLES:
        base_arr = baseline_r2[var]
        pert_arr = perturbed_r2[var]
        diff = np.abs(pert_arr - base_arr)
        r2_deltas[var] = np.mean(diff)
    return r2_deltas

# ------------------------
# 敏感性分析主函数
# ------------------------
def sensitivity_analysis(use_gui=False, show_plot=False):
    with open(PARAMETER_FILE, 'r') as f:
        param_dict = json.load(f)

    baseline_r2 = load_baseline_r2()
    summary = []

    for param, base_value in param_dict.items():
        if isinstance(base_value, list):
            base_scalar = base_value[0]
        else:
            base_scalar = base_value

        for delta in [0.1, -0.1]:
            new_value = base_scalar * (1 + delta)
            print(f"Evaluating {param} with change {delta:+.0%}...")
            perturbed_result = run_simulation_with_param_change(param, new_value)

            plot_with_fuzzy_matching(perturbed_result, OBSERVE_FILE, show_plot=show_plot, save_plot=False)
            delta_r2 = compute_r2_deltas(baseline_r2, perturbed_result)
            summary.append({"param": param, "change": delta, **delta_r2})

    # 保存结果
    df = pd.DataFrame(summary)
    df.to_csv(os.path.join(OUTPUT_DIR, "sensitivity_summary.csv"), index=False)
    print("敏感性分析完成，结果保存在：", OUTPUT_DIR)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run sensitivity analysis.")
    parser.add_argument('--use-gui', action='store_true', help='Use GUI for parameter loading')
    parser.add_argument('--show-plot', action='store_true', help='Show plots instead of saving only')
    args = parser.parse_args()

    sensitivity_analysis(use_gui=args.use_gui, show_plot=args.show_plot)

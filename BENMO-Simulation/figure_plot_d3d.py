"""
weekly_plot_fuzzy_dates.py
------------------------------------------------------------
• Our & Delft3D 均用 “模糊匹配” 逻辑：
      在 ±time_window_hours 内找 |sim - obs| 最小的周
• 横轴改成真实日期：
      起点 2016-01-01，Δt = hours_per_block (默认 48 h)
      仅显示每年 1 月、7 月刻度，标签格式 YYYY-MM
------------------------------------------------------------
"""

import re
import datetime as dt
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.metrics import r2_score, mean_squared_error

# ── 1. 读取 Delft3D CSV（多列同海区取行均值）────────────────────
_ZONE_RE = re.compile(r"(\d{1,2})")

def load_delft_csv_avg(csv_path: str | Path,
                       total_zones: int = 20,
                       zone_start_1: bool = True) -> np.ndarray:
    df = pd.read_csv(csv_path)
    df = df.drop(columns=df.columns[0])                       # 去时间戳

    zone_cols: dict[int, list[str]] = {}
    for col in df.columns:
        m = _ZONE_RE.match(col.strip())
        if not m:
            continue
        z = int(m.group(1)) - (1 if zone_start_1 else 0)
        zone_cols.setdefault(z, []).append(col)

    arr = np.full((len(df), total_zones), np.nan)
    for z, cols in zone_cols.items():
        if 0 <= z < total_zones:
            arr[:, z] = df[cols].mean(axis=1).to_numpy(float)
    return arr


# ── 2. 主绘图函数 ────────────────────────────────────────────────
def plot_weekly_means_fuzzy_dates(
        simulated_data_dict: dict[str, np.ndarray],
        observe_file_path: str,
        delft_csv_dict: dict[str, str] | None = None,
        hours_per_block: int = 24*2,          # 48 h
        time_window_hours: int = 24*5,        # ±5 days
        total_zones: int = 20,
        save_plot: bool = False,
        show_plot: bool = True,
        out_suffix: str = ""
):
    import math

    delft_csv_dict = delft_csv_dict or {}
    obs_df = pd.read_excel(observe_file_path)

    # Checking column names in obs_df
    print("Columns available in the observation data:", obs_df.columns)

    # 日期起点与刻度格式
    start_date = dt.datetime(2016, 1, 1)
    major_locator = mdates.MonthLocator(bymonth=[1, 7])
    major_formatter = mdates.DateFormatter('%Y-%m')

    # —— 获取所有有观测数据的海区 —— #
    observed_zones = {}
    for var in simulated_data_dict.keys():
        var_l = var.lower()

        # Check if the variable has observation data
        if var_l in obs_df.columns:
            observed_zones[var] = sorted(obs_df.loc[~obs_df[var_l].isna(), "zone"].unique().tolist())
        else:
            observed_zones[var] = []  # No observation data for this variable
            print(f"[WARNING] Column '{var_l}' not found in observation data.")

    # If a variable has no observed zones, assign it a predefined set of zones
    predefined_zones = [1, 3, 4, 6, 8, 9, 10, 12, 13, 14, 18, 19]  # For variables without observation data
    for var in simulated_data_dict.keys():
        if not observed_zones.get(var):
            observed_zones[var] = predefined_zones
            print(f"[INFO] No observation data available for '{var}', using predefined zones: {predefined_zones}.")

    # Proceed with plotting the data
    for var, sim_arr in simulated_data_dict.items():
        var_l = var.lower()
        sim_arr = np.asarray(sim_arr)

        # Skip the variable if it doesn't have observation data and is using predefined zones
        if not observed_zones.get(var):
            continue

        # Read Delft3D data if available
        has_d3d = var in delft_csv_dict
        if has_d3d:
            d3d_arr = load_delft_csv_avg(delft_csv_dict[var], total_zones=total_zones)
            min_len = min(len(sim_arr), len(d3d_arr))
            sim_arr, d3d_arr = sim_arr[:min_len], d3d_arr[:min_len]
        else:
            min_len, d3d_arr = len(sim_arr), None
            sim_arr = sim_arr[:min_len]

        # —— Compute weekly averages —— #
        num_blk = min_len // hours_per_block
        if num_blk == 0:
            print(f"[WARNING] Not enough data to form blocks for '{var}', skipping.")
            continue

        sim_blk = sim_arr[:num_blk * hours_per_block].reshape(num_blk, hours_per_block, total_zones).mean(1)
        if has_d3d:
            d3d_blk = d3d_arr[:num_blk * hours_per_block].reshape(num_blk, hours_per_block, total_zones).mean(1)

        # Dates for plotting
        date_idx = [start_date + dt.timedelta(hours=hours_per_block * b) for b in range(num_blk)]

        # Plotting setup for observed zones
        n = len(observed_zones[var])
        ncol = 4
        nrow = math.ceil(n / ncol)

        fig, axes = plt.subplots(nrow, ncol, figsize=(3.6 * ncol, 3.0 * nrow), sharex=True, sharey=True, constrained_layout=True)
        axes = np.atleast_2d(axes)
        axes_list = [axes[r, c] for r in range(axes.shape[0]) for c in range(axes.shape[1])]
        for ax in axes_list[n:]:
            ax.set_visible(False)

        # fig.suptitle(f"{var.upper()} Weekly Mean vs Observations (mg/L)", fontsize=15)
        legend_done = False

        # Loop through the zones with data
        for k, zone in enumerate(observed_zones[var]):
            ax = axes_list[k]

            # Plot simulated data (BENMO-Nutrients)
            ax.plot(date_idx, sim_blk[:, zone], c='#4c9dff', lw=1, zorder=2, alpha=0.8, label='BENMO-Nutrients' if not legend_done else None)

            # Plot Delft3D data
            if has_d3d:
                ax.plot(date_idx, d3d_blk[:, zone], c='#1E8449', lw=1, zorder=2, alpha=0.8, label='Delft3D' if not legend_done else None)

            # —— 观测 / Fuzzy 匹配 —— #
            df_z = obs_df[(obs_df['zone'] == zone) & (~obs_df[var_l].isna())]
            obs_vals, sim_match, d3d_match = [], [], []
            obs_label_added = False

            for _, row in df_z.iterrows():
                t_obs = int(row['timestep'])
                v_obs = row[var_l]

                # Match simulation data
                cand_sim = [(abs(sim_blk[b, zone] - v_obs), b) for b in range(num_blk) if abs(b * hours_per_block - t_obs) <= time_window_hours]
                if cand_sim:
                    _, b_sim = min(cand_sim, key=lambda x: x[0])
                    sim_match.append(sim_blk[b_sim, zone])
                    ax.scatter(date_idx[b_sim], v_obs, c='tomato', s=8, zorder=10, label='Observation' if (not legend_done and not obs_label_added) else '_nolegend_')
                    obs_label_added = True
                else:
                    sim_match.append(np.nan)

                # Match Delft3D data
                if has_d3d:
                    cand_d = [(abs(d3d_blk[b, zone] - v_obs), b) for b in range(num_blk) if abs(b * hours_per_block - t_obs) <= time_window_hours]
                    if cand_d:
                        _, b_d = min(cand_d, key=lambda x: x[0])
                        d3d_match.append(d3d_blk[b_d, zone])
                    else:
                        d3d_match.append(np.nan)

                obs_vals.append(v_obs)

            # Evaluate the fitting metrics (NSE, RMSE)
            title = [f"Zone {zone+1}"]
            obs_arr = np.asarray(obs_vals)

            mask_s = ~np.isnan(sim_match)
            if mask_s.sum() > 1:
                rmse_s = mean_squared_error(obs_arr[mask_s], np.array(sim_match)[mask_s], squared=False)
                title.append(f"Us:  NSE={r2_score(obs_arr[mask_s], np.array(sim_match)[mask_s]):.2f}, RMSE={rmse_s:.4f}")

            if has_d3d:
                mask_d = ~np.isnan(d3d_match)
                if mask_d.sum() > 1:
                    rmse_d = mean_squared_error(obs_arr[mask_d], np.array(d3d_match)[mask_d], squared=False)
                    # title.append(f"D3D: NSE={r2_score(obs_arr[mask_d], np.array(d3d_match)[mask_d]):.2f}, RMSE={rmse_d:.4f}")

            if len(title) == 1:
                title.append("Insufficient Data")

            ax.set_title("\n".join(title), fontsize=9)

            ax.xaxis.set_major_locator(major_locator)
            ax.xaxis.set_major_formatter(major_formatter)
            ax.tick_params(axis='x', rotation=0, labelsize=8)
            ax.grid(alpha=0.3)

            if not legend_done:
                ax.legend(loc='upper left', fontsize=7)
                legend_done = True

            if k // ncol == nrow - 1:
                ax.set_xlabel("")
            if k % ncol == 0:
                ax.set_ylabel("Conc. (mg/L)")

        if save_plot:
            plt.savefig(f"{var.upper()}_weekly_fuzzy_dates{out_suffix}_RMSE_obsOnly.svg")
        if show_plot:
            plt.show()
        plt.close(fig)

# ── 3. 示例调用 ───────────────────────────────────────────────
if __name__ == "__main__":
    # 你的模型（6 变量）
    sim_data = {
        'nh4': np.load("./baseline_results/NH4_simulated_test.npy"),
        'no3': np.load("./baseline_results/NO3_simulated_test.npy"),
        'po4': np.load("./baseline_results/PO4_simulated_test.npy"),
        'op':  np.load("./baseline_results/OP_simulated_test.npy"),
        'pp':  np.load("./baseline_results/PP_simulated_test.npy"),
        'on': np.load("./baseline_results/ON_simulated_test.npy")
    }

    # Delft3D 仅 3 变量（若无，可传空字典）
    d3d_csv = {
        'nh4': "./delft_csv/NH4_all_stations.csv",
        'no3': "./delft_csv/NO3_all_stations.csv",
        'po4': "./delft_csv/PO4_all_stations.csv",
    }

    plot_weekly_means_fuzzy_dates(
        simulated_data_dict = sim_data,
        observe_file_path   = "./database/observe_data_20.xlsx",
        delft_csv_dict      = d3d_csv,
        hours_per_block     = 24*30,
        time_window_hours   = 24*2,
        save_plot           = True,
        show_plot           = False,
        out_suffix          = "_v2"
    )

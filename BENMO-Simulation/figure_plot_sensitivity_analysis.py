import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
from matplotlib.ticker import FuncFormatter

# 设置绘图风格
sns.set(style="whitegrid")
sci_fmt = FuncFormatter(lambda x, _: f"{x:.2e}")

# === 参数设置 ===
csv_path = "sensitivity_analysis_output/sensitivity_5_source_by_zone_8groups.csv"  # 本地路径
output_dir = "8groups_figs"
os.makedirs(output_dir, exist_ok=True)

# === 读取 CSV 文件 ===
df = pd.read_csv(csv_path, engine="python")  # 如有问题可加 encoding="utf-8-sig"

# 自动生成调色板（确保支持 plus / minus）
direction_values = df["direction"].dropna().unique().tolist()
palette = {d: c for d, c in zip(direction_values, sns.color_palette("Set2", len(direction_values)))}
direction_colors = {"plus": '#F1948A', "minus": '#85C1E9'}

# ========== 1. MAD 图 ==========
for var in df["variable"].unique():
    df_var = df[df["variable"] == var].dropna(subset=["mean_abs_diff"])
    if df_var.empty:
        continue

    max_val = df_var["mean_abs_diff"].abs().max() * 1.1

    fig, axes = plt.subplots(4, 5, figsize=(24, 16), sharex=False, sharey=False)
    fig.suptitle(f"Top 10 Sensitivities (±) by MAD - {var.upper()}", fontsize=20)

    for zone in range(20):
        ax = axes[zone // 5, zone % 5]
        df_zone = df_var[df_var["zone"] == zone].copy()
        if df_zone.empty:
            ax.set_title(f"Zone {zone + 1}\nNo Data")
            ax.axis("off")
            continue

        df_zone["abs_value"] = df_zone["mean_abs_diff"].abs()
        df_zone["param_dir"] = df_zone["param"]
        df_top = df_zone.sort_values("abs_value", ascending=False).head(10)

        sns.barplot(data=df_top, y="param_dir", x="mean_abs_diff", hue="direction",
                    ax=ax, palette=direction_colors, hue_order=["plus", "minus"], dodge=False)
        ax.set_title(f"Zone {zone + 1}", fontsize=10)
        ax.set_xlabel("MAD", fontsize=9)
        ax.set_ylabel("")
        ax.xaxis.set_major_formatter(sci_fmt)
        ax.set_xlim(0, max_val)
        ax.tick_params(axis='y', labelsize=8)
        ax.tick_params(axis='x', labelsize=8)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(os.path.join(output_dir, f"top10_mad_{var}_8groups.png"), dpi=300)
    plt.close()

# ========== 2. R² 图（仅 nh4 和 no3） ==========
per_mille_fmt = FuncFormatter(lambda x, pos: f"{x*1000:.1f}‰")

for var in ["nh4", "no3", "po4"]:
    df_var = df[(df["variable"] == var) & (df["r2_change"].notna())]
    zones_with_data = sorted(df_var["zone"].unique())
    if len(zones_with_data) == 0:
        continue

    # 动态计算行列数（最多4列）
    num_zones = len(zones_with_data)
    ncols = min(4, num_zones)
    nrows = math.ceil(num_zones / ncols)

    fig, axes = plt.subplots(nrows, ncols,
                             figsize=(ncols * 5, nrows * 4),
                             sharex=False, sharey=False)
    axes = axes.flatten() if num_zones > 1 else [axes]
    fig.suptitle(f"Sensitivities (±) by R² Change - {var.upper()}", fontsize=20)

    for i, zone in enumerate(zones_with_data):
        ax = axes[i]
        df_zone = df_var[df_var["zone"] == zone].copy()
        if df_zone.empty:
            ax.set_title(f"Zone {zone + 1}\nNo R² Data")
            ax.axis("off")
            continue

        # 计算绝对值并排序
        df_zone["abs_value"] = df_zone["sensitivity"].abs()
        df_top = df_zone.sort_values("abs_value", ascending=False)

        # 绘制条形图
        sns.barplot(data=df_top,
                    y="param",
                    x="sensitivity",
                    hue="direction",
                    ax=ax,
                    palette=direction_colors,
                    hue_order=["plus", "minus"],
                    dodge=True,
                    width=0.7)

        ax.set_axisbelow(True)
        ax.xaxis.grid(True, alpha=0.3)
        ax.yaxis.grid(False)

        # 按绝对长度降序设置 zorder，保证短的在上
        patches = sorted(ax.patches,
                         key=lambda p: abs(p.get_width()),
                         reverse=True)
        for z_order, patch in enumerate(patches):
            patch.set_zorder(z_order+10)

        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(0.5)
        ax.xaxis.label.set_color('black')
        ax.yaxis.label.set_color('black')

        # 标题与标签
        ax.set_title(f"Zone {zone + 1}", fontsize=10)
        ax.set_xlabel("Sensitivity (‰)", fontsize=9)
        ax.set_ylabel("")

        # 设置千分比刻度
        ax.xaxis.set_major_formatter(per_mille_fmt)

        # 刻度参数
        ax.xaxis.grid(False)
        ax.yaxis.grid(False)

        # 确保下方和左侧的 ticks 打开（Seaborn 默认只开启了网格）
        ax.tick_params(
            axis='x',
            which='both',
            bottom=True,
            top=False,
            labelsize=8,
            colors='black',
            direction='out',
            length=3,  # 刻度线长度
            width=0.5  # 刻度线宽度
        )
        ax.tick_params(
            axis='y',
            which='both',
            left=True,
            right=False,
            labelsize=8,
            colors='black',
            direction='out',
            length=3,
            width=0.5
        )

        # 确保对应的 spine 可见并设置粗细
        ax.spines['left'].set_visible(True)
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_linewidth(0.5)
        ax.spines['bottom'].set_linewidth(0.5)

        # —— 仅第一张子图保留 legend
        if i == 0:
            ax.legend(loc='lower left', fontsize=8)
        else:
            leg = ax.get_legend()
            if leg:
                leg.remove()

    # 删除多余空子图
    for j in range(len(zones_with_data), len(axes)):
        axes[j].axis("off")

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(os.path.join(output_dir, f"top10_r2_{var}_8groups_split.svg"))
    plt.close()

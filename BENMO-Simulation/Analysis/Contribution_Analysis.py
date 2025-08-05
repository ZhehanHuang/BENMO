import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 读取 CSV 文件
df = pd.read_csv('cumulative_contributions_3y.csv')

# 获取所有的营养盐
nutrients = df['Nutrient'].unique()

# 设置图表风格
sns.set(style="whitegrid")

# --------------------------
# 1️⃣ 绘制每种营养盐的组图，每个海区一个小图
# --------------------------
for nutrient in nutrients:
    # 筛选当前营养盐的数据
    nutrient_data = df[df['Nutrient'] == nutrient]

    # 创建 20 个小图（每个海区一个子图）
    fig, axes = plt.subplots(5, 4, figsize=(20, 15))  # 5 行 4 列的子图布局
    fig.suptitle(f'Contributions for {nutrient} (Cumulative for 3 Years)', fontsize=16)

    # 遍历所有海区（Area1 到 Area20）
    for i, ax in enumerate(axes.flatten()):
        area_name = f'Area{i + 1}'

        # 选取当前海区的所有过程
        area_data = nutrient_data[[col for col in nutrient_data.columns if area_name in col]]

        # 绘制每个过程的累计贡献
        ax.bar(area_data.columns, area_data.iloc[0], color='skyblue')
        ax.set_title(area_name)
        ax.set_ylabel('Contribution')
        ax.set_xticklabels(area_data.columns, rotation=45)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # 调整布局
    plt.show()


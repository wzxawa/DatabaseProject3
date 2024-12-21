import matplotlib.pyplot as plt
import numpy as np
import os

# 线程数和对应的时间（单位：秒）
thread_counts = [1, 2, 4, 8, 16, 32, 64]
execution_times = [2906.23, 1531.03, 780.57, 401.06, 219.98, 119.78, 84.41]

# 获取当前 Python 脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 创建柱状图
plt.figure(figsize=(10, 6))

# 使用 np.arange 来创建均匀的 x 轴位置
x_positions = np.arange(len(thread_counts))

# 绘制柱状图，设置宽度和颜色
plt.bar(x_positions, execution_times, color='seagreen', width=0.6)

# 设置标题和标签
plt.title('Time taken for concurrent insert with different thread counts-OpenGauss', fontsize=14)
plt.xlabel('Thread Count', fontsize=12)
plt.ylabel('Time (seconds)', fontsize=12)

# 设置 x 轴标签，使其与线程数对应
plt.xticks(x_positions, thread_counts)

# 显示线程数和时间的数值
for i in range(len(thread_counts)):
    plt.text(x_positions[i], execution_times[i] + 1, f'{execution_times[i]:.2f}', ha='center', va='bottom')

# 保证布局紧凑
plt.tight_layout()

# 文件保存路径为当前脚本所在目录
save_path = os.path.join(script_dir, 'scalability_opengauss.png')

# 保存图像到当前脚本所在目录
plt.savefig(save_path)

# 显示图表
plt.show()

# 打印保存的路径
print(f"Graph saved at: {save_path}")

import csv
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt

# 设置CSV文件路径
csv_file_path = 'run_times.csv'

# 读取CSV文件中的时间数据
times = []
with open(csv_file_path, mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过标题行
    for row in reader:
        if len(row) == 2:
            time_str = row[1]
            time_obj = datetime.strptime(time_str, '%H:%M:%S')
            times.append(time_obj.hour + time_obj.minute / 60 + time_obj.second / 3600)

# 使用Seaborn设置风格以提高图表美观度
sns.set(style="whitegrid")

# 生成直方图
plt.figure(figsize=(10, 6))
sns.histplot(times, bins=24, kde=False, color="skyblue", edgecolor="black", binrange=(0,24))

# 美化图表
plt.title(f'Daily First Run Time Distribution for {datetime.now().strftime("%B %Y")}')
plt.xlabel('Hour of Day')
plt.ylabel('Frequency')
plt.xticks(range(0, 25))

# 保存直方图为图片
histogram_image_path = 'run_times_histogram_seaborn.png'
plt.savefig(histogram_image_path)
plt.close()


# 生成HTML内容，包含直方图图片，并确保内容居中
html_content = f"""
<html>
<head>
    <title>Run Times Histogram</title>
    <style>
        body {{
            text-align: center;
            font-family: Arial, sans-serif;
        }}
        img {{
            margin: 20px;
        }}
    </style>
</head>
<body>
    <h2>Daily First Run Time Distribution for {datetime.now().strftime("%B %Y")}</h2>
    <img src="{histogram_image_path}" alt="Daily First Run Time Distribution">
</body>
</html>
"""

# 设置HTML文件路径
html_file_path = 'run_times_histogram.html'

# 将HTML内容写入文件
with open(html_file_path, 'w') as file:
    file.write(html_content)

print("HTML文件已生成，包含直方图图片。")

import csv
from datetime import datetime, timedelta
from collections import Counter
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
import os
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument('--cutoff', type=float, default=8.5, help='The cutoff hour for counting runs in the last 7 days')
args = argparser.parse_args()
# makedirs(data) 方法用于递归创建目录
os.makedirs('./docs/data', exist_ok=True)
# 数据准备
csv_file_path = './docs/data/run_times.csv'
times = []

with open(csv_file_path, mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过标题行
    for row in reader:
        date, time = row
        date_time_obj = datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M:%S')
        times.append(date_time_obj)

# 筛选本月和本年的数据
current_month = datetime.now().month
current_year = datetime.now().year
times_this_month = [time for time in times if time.month == current_month and time.year == current_year]
times_this_year = [time for time in times if time.year == current_year]
times_last_7_days = [time for time in times if time > datetime.now() - timedelta(days=7)]

def count_continuous_early_rises_from_yesterday(times, cutoff_hour=8.5):
    """
    从昨天开始向前数连续早起的天数。
    
    参数:
    - times: datetime对象列表，可能是无序的。
    - cutoff_hour: 特定的小时（24小时制）。
    
    返回:
    - 自昨天起连续在特定小时之前开始工作的天数。
    """
    # 确保times是排序的，以确保能够从最近的一天开始检查
    sorted_times = sorted(times)
    
    # 初始化计数器和当前检查的日期
    count = 0
    current_date = datetime.now().date()
    last_date = datetime.now().date() + timedelta(days=1)
    for i in range(len(sorted_times)):
        idx = len(sorted_times) - i - 1
        current_time = sorted_times[idx]
        if current_time.date() == last_date - timedelta(days=1):
            if current_time.hour + current_time.minute / 60 < cutoff_hour:
                count += 1
                last_date = current_time.date()
        else:
            break
    
    return count

# 假设times_example已经定义并包含datetime对象列表
# 由于环境限制，以下代码仅展示函数定义，无法直接测试
# 请在本地环境中根据实际情况定义times列表并调用此函数进行测试

recent_runs_before_cutoff = count_continuous_early_rises_from_yesterday(times)
print(recent_runs_before_cutoff)

def real_time_to_hours_minutes(real_time):
    """
    将实数转化为小时和分钟的字符串形式。
    
    参数:
    - real_time: 实数，表示小时数。例如，1.5小时表示为1小时30分钟。
    
    返回:
    - 字符串，格式为 "HH小时MM分钟"。
    """
    hours = int(real_time)  # 获取小时数
    minutes = int((real_time - hours) * 60)  # 将小数部分转换为分钟数
    
    return f"{hours}:{minutes}"

def plot_times_with_cutoff_and_line(times, cutoff_hour):
    """
    使用Plotly绘制时间点的折线图，并添加一条表示cutoff的水平线。
    点按时间顺序连接，并且使点更大且好看。
    """
    times_sorted = sorted(times, key=lambda x: x)  # 按时间排序
    x_data = [time.strftime("%Y-%m-%d %H:%M:%S") for time in times_sorted]
    y_data = [time.hour + time.minute / 60 for time in times_sorted]

    colors = ['red' if y > cutoff_hour else 'blue' for y in y_data]  # 晚于cutoff为红色，否则为蓝色

    fig = go.Figure()

    # 使用折线连接所有点，通过颜色区分晚于和早于cutoff的点
    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers',
                             marker=dict(size=10, color=colors, line=dict(width=2)),
                             line=dict(color='grey', width=2)))

    # 添加表示cutoff的水平线
    fig.add_hline(y=cutoff_hour, line=dict(color='green', width=2, dash='dash'),
                  annotation_text=f"Cutoff Hour: {cutoff_hour}", annotation_position="bottom right")

    fig.update_layout(title='',
                      xaxis_title='Date and Time',
                      yaxis_title='Hour of Day',
                      yaxis=dict(range=[0, 24]))

    return fig.to_html(full_html=False, include_plotlyjs='cdn')

# 生成并显示图表
plot_getup_last_7_days = plot_times_with_cutoff_and_line(times_last_7_days, args.cutoff)

def generate_histogram_plotly_html(times, title):
    """
    使用Plotly生成直方图的HTML字符串，并将频率归一化到0-1之间。
    
    参数:
    - times: 时间数据的列表，每个元素是datetime对象。
    - title: 图表的标题。
    
    返回:
    - 一个HTML字符串，表示生成的直方图。
    """
    # 将时间转换为一天中的小时数（浮点数）
    times_in_hours = [time.hour + time.minute / 60 for time in times]
    
    # 创建直方图并设置histnorm为'probability'以归一化频率到0-1之间
    fig = go.Figure(data=[go.Histogram(
        x=times_in_hours,
        xbins=dict(start=0, end=24, size=1),  # 定义24个小时的bins
        marker_color='skyblue',  # 柱体颜色
        marker_line_color='black',  # 柱体边界颜色
        marker_line_width=1.5,  # 柱体边界宽度
        opacity=0.7,  # 柱体透明度
        histnorm='probability'  # 归一化频率到0-1之间
    )])
    
    # 更新布局设置，使图表更美观
    fig.update_layout(
        title=title,
        xaxis_title='Hour of Day',
        yaxis_title='Frequency',
        bargap=0.2,  # 柱体之间的间隙
        template="plotly_white",  # 使用白色背景的模板
    )
    
    # 返回HTML字符串
    return fig.to_html(full_html=False, include_plotlyjs='cdn')
# 生成本月和本年的直方图
monthly_plot_html = generate_histogram_plotly_html(times_this_month, "Monthly Wake Up Time Distribution")
yearly_plot_html = generate_histogram_plotly_html(times_this_year, "Yearly Wake Up Time Distribution")

def generate_pie_chart_html(times, title):
    times_in_half_hours = [(time.hour * 2 + (1 if time.minute >= 30 else 0)) for time in times]
    time_frequencies = Counter(times_in_half_hours)
    labels = [f"{int(hh/2)}:{'30' if hh % 2 else '00'}" for hh in sorted(time_frequencies.keys())]
    values = [time_frequencies[hh] for hh in sorted(time_frequencies.keys())]

    # 使用新的颜色集
    moderate_saturation_colors = [
        'rgba(255, 159, 128, 0.8)',  # 柔和的珊瑚
        'rgba(255, 205, 86, 0.8)',   # 柔和的黄色
        'rgba(75, 192, 192, 0.8)',   # 柔和的青色
        'rgba(153, 102, 255, 0.8)',  # 柔和的紫色
        'rgba(54, 162, 235, 0.8)',   # 柔和的蓝色
        'rgba(255, 99, 132, 0.8)',   # 柔和的红色
        'rgba(101, 143, 75, 0.8)',   # 柔和的绿色
        'rgba(255, 159, 64, 0.8)',   # 柔和的橙色
        'rgba(201, 203, 207, 0.8)',  # 柔和的灰色
    ]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=moderate_saturation_colors))])
    fig.update_layout(title_text=title)
    return fig.to_html(full_html=False, include_plotlyjs='cdn')


monthly_pie_html = generate_pie_chart_html(times_this_month, "Monthly Wake Up Time Pie Chart")
yearly_pie_html = generate_pie_chart_html(times_this_year, "Yearly Wake Up Time Pie Chart")

# 假设monthly_pie_html和yearly_pie_html已经由Plotly生成并包含圆饼图的HTML代码
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Wake Up Time Statistics</title>
    <style>
        .container {{
            display: flex;
            flex-direction: column; /* 修改为垂直布局 */
            justify-content: space-around;
            align-items: center;
        }}
        .item {{
            flex-basis: 48%;
        }}
        img {{
            max-width: 100%;
            height: auto;
        }}
        .chart-container {{
            text-align: center;
        }}
    </style>
</head>
<body>
    <center>
    <p>
        <span style="font-size: 28px; color: black;">Qihang has been an early bird for</span>
        <span style="font-size: 40px; color: purple;"> {recent_runs_before_cutoff}</span>
        <span style="font-size: 28px; color: black;"> consecutive days</span>
        <span style="font-size: 28px; color: blue;"> (before {real_time_to_hours_minutes(args.cutoff)})</span>
    </p>
</body>
<body>
    <center><h2>Wake Up Time Statistics for Last 7 days</h2></center>
    <div class="container">
        <div class="item chart-container">
            {plot_getup_last_7_days}
        </div>
    </div>
</body>
<hr>
<body>
    <center><h2>Wake Up Time Statistics for {datetime.now().strftime("%B %Y")}</h2></center>
    <div class="container">
        <div class="item">
            {monthly_plot_html}
        </div>
        <div class="item chart-container">
            {monthly_pie_html}
        </div>
    </div>
</body>
<body>
    <center><h2>Wake Up Time Statistics for {datetime.now().strftime("%Y")}</h2></center>
    <div class="container">
        <div class="item">
            {yearly_plot_html}
        </div>
        <div class="item chart-container">
            {yearly_pie_html}
        </div>
    </div>
</body>
</html>
"""

with open('docs/index.md', 'w') as file:
    file.write(html_content)
    
print("plot has been generated.")

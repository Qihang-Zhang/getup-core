import csv
from datetime import datetime, timedelta
from collections import Counter
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
import os

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

def count_runs_before_time_in_last_7_days(times, cutoff_hour=10):
    """
    计算最近七天内，在特定小时之前开始工作的次数。
    
    参数:
    - times: datetime对象列表。
    - cutoff_hour: 特定的小时（24小时制）。
    
    返回:
    - 在特定小时之前开始工作的次数。
    """
    cutoff_time = timedelta(hours=cutoff_hour)
    count = 0
    for time in times:
        if time.date() >= datetime.now().date() - timedelta(days=7) and time.time() < (datetime.min + cutoff_time).time():
            count += 1
    return count

def generate_beautiful_number_html(number):
    """
    生成一个美观显示数字的HTML代码。
    
    参数:
    - number: 要显示的数字。
    
    返回:
    - 包含数字显示HTML代码的字符串。
    """
    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Beautiful Number Display</title>
        <style>
            body {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #f0f0f0;
            }}
            .number-container {{
                font-size: 4em;
                font-weight: bold;
                color: #3178C6; /* A nice shade of blue */
                background-color: #E6F1FF; /* Light blue background */
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
        </style>
    </head>
    <body>
        <div class="number-container">
            {number}
        </div>
    </body>
    </html>
    """
    return html_code

recent_runs_before_cutoff = count_runs_before_time_in_last_7_days(times)
html_number = generate_beautiful_number_html(recent_runs_before_cutoff)

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
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Beautiful Number Display</title>
    <style>
        body {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f0f0f0;
        }}
        .number-container {{
            font-size: 4em;
            font-weight: bold;
            color: #3178C6; /* A nice shade of blue */
            background-color: #E6F1FF; /* Light blue background */
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}
    </style>
</head>
<body>
    <div class="number-container">
        {recent_runs_before_cutoff}
    </div>
</body>
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

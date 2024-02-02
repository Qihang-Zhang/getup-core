import csv
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import os

# 数据准备
csv_file_path = 'run_times.csv'
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

def generate_histogram(times, title, file_name):
    times_in_hours = [time.hour + time.minute / 60 for time in times]
    
    plt.figure(figsize=(10, 6))
    plt.hist(times_in_hours, bins=24, range=(0, 24), alpha=0.7, color='skyblue', edgecolor='black', density=True)
    plt.title(title)
    plt.xlabel('Hour of Day')
    plt.ylabel('Frequency')
    plt.xticks(range(0, 25))
    plt.savefig(file_name)
    plt.close()

# 生成本月和本年的直方图
generate_histogram(times_this_month, "Monthly Wake Up Time Distribution", "monthly_histogram.png")
generate_histogram(times_this_year, "Yearly Wake Up Time Distribution", "yearly_histogram.png")

def generate_pie_chart_html(times, title):
    times_in_half_hours = [(time.hour * 2 + (1 if time.minute >= 30 else 0)) for time in times]
    time_frequencies = Counter(times_in_half_hours)
    labels = [f"{int(hh/2)}:{'30' if hh % 2 else '00'}" for hh in sorted(time_frequencies.keys())]
    values = [time_frequencies[hh] for hh in sorted(time_frequencies.keys())]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
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
<body>
    <center><h2>Wake Up Time Statistics for {datetime.now().strftime("%B %Y")}</h2></center>
    <div class="container">
        <div class="item">
            <img src="monthly_histogram.png" alt="Monthly Histogram">
        </div>
        <div class="item chart-container">
            {monthly_pie_html}
        </div>
    </div>
</body>
<body>
    <center><h2>Wake Up Time Statistics for {datetime.now().strftime("%B %Y")}</h2></center>
    <div class="container">
        <div class="item">
            <img src="yearly_histogram.png" alt="Monthly Histogram">
        </div>
        <div class="item chart-container">
            {yearly_pie_html}
        </div>
    </div>
</body>
</html>
"""

with open('wake_up_time_statistics.html', 'w') as file:
    file.write(html_content)


with open('wake_up_time_statistics.html', 'w') as file:
    file.write(html_content)

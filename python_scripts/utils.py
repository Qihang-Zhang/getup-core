
import csv
from datetime import datetime, timedelta
from collections import Counter
import plotly.graph_objects as go

def count_continuous_early_rises_from_yesterday(times, last_date, getup_threshold):  
    # 初始化计数器和当前检查的日期
    count = 0
    for i in range(len(times)):
        idx = len(times) - i - 1
        current_time = times[idx]
        if current_time.date() == last_date - timedelta(days=1):
            if current_time.hour + current_time.minute / 60 < getup_threshold:
                count += 1
                last_date = current_time.date()
        else:
            break
    
    return count

def count_continuous_late_rises_from_yesterday(times, getup_threshold):  
    # 初始化计数器和当前检查的日期
    current_time = datetime.now()
    last_date=datetime.now().date()
    last_day_count = 0
    for i in range(len(times)):
        idx = len(times) - i - 1
        current_time = times[idx]
        if current_time.hour + current_time.minute / 60 > getup_threshold:
            last_day_count = 1
        else:
            break
        
    delta = last_date - current_time.date()
    
    return delta.days + int(i ==0)*last_day_count

def real_time_to_hours_minutes(real_time):
    hours = int(real_time)
    minutes = int((real_time - hours) * 60)
    
    return f"{hours}:{minutes}"

def plot_times_with_getup_threshold_and_line(times, getup_threshold):
    times_sorted = sorted(times, key=lambda x: x)  # 按时间排序
    x_data = [time.strftime("%Y-%m-%d %H:%M:%S") for time in times_sorted]
    y_data = [time.hour + time.minute / 60 for time in times_sorted]

    colors = ['red' if y > getup_threshold else 'blue' for y in y_data]  # 晚于getup_threshold为红色，否则为蓝色

    fig = go.Figure()

    # 使用折线连接所有点，通过颜色区分晚于和早于getup threshold的点
    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers',
                             marker=dict(size=10, color=colors, line=dict(width=2)),
                             line=dict(color='grey', width=2)))

    # 添加表示getup threshold的水平线
    fig.add_hline(y=getup_threshold, line=dict(color='green', width=2, dash='dash'),
                  annotation_text=f"Get-up threshold Hour: {getup_threshold}", annotation_position="bottom right")

    fig.update_layout(title='',
                      xaxis_title='Date and Time',
                      yaxis_title='Hour of Day',
                      yaxis=dict(range=[0, 24]))

    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def generate_histogram_plotly_html(times, title):
    times_in_hours = [time.hour + time.minute / 60 for time in times]
    
    # 创建直方图并设置histnorm为'probability'以归一化频率到0-1之间
    fig = go.Figure(data=[go.Histogram(
        x=times_in_hours,
        xbins=dict(start=0, end=24, size=1),  # 定义24个小时的bins
        marker_color='skyblue',  # 柱体颜色
        marker_line_color='black',  # 柱体边界颜色
        marker_line_width=1.5,  # 柱体边界宽度
        opacity=0.6,  # 柱体透明度
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

def conditional_emoji(recent_runs_before_getup_threshold, recent_runs_after_getup_threshold):

    if recent_runs_before_getup_threshold > 0 and recent_runs_after_getup_threshold == 0:
        emoji = "😆"
        Character = "early bird 🐤"
        days = recent_runs_before_getup_threshold
        before_or_after = "before"
    elif recent_runs_before_getup_threshold == 0 and recent_runs_after_getup_threshold > 0:
        emoji = "😡"
        Character = "lazybones 🦉"
        days = recent_runs_after_getup_threshold
        before_or_after = "after"
    else:
        emoji = "😆"
        Character = "early bird 🐤"
        days = recent_runs_before_getup_threshold
        before_or_after = "before"
        
    return emoji, Character, days, before_or_after

def write_md_file_today(times, recent_runs_before_getup_threshold, recent_runs_after_getup_threshold, args, plot_getup_recent_days):
    if recent_runs_before_getup_threshold > 0 and recent_runs_after_getup_threshold == 0:
        emoji = "😆"
        character = "early bird 🐤"
        days = recent_runs_before_getup_threshold
        before_or_after = "before"
    elif recent_runs_before_getup_threshold == 0 and recent_runs_after_getup_threshold > 0:
        emoji = "😡"
        character = "lazybones 🦉"
        days = recent_runs_after_getup_threshold
        before_or_after = "after"
    else:
        emoji = "😆"
        character = "early bird 🐤"
        days = recent_runs_before_getup_threshold
        before_or_after = "before"
        
    data_today = f"{times[-1].hour}:{times[-1].minute}:{times[-1].second}"
    # 假设monthly_pie_html和yearly_pie_html已经由Plotly生成并包含圆饼图的HTML代码
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<body>
    <center>
    <p>
        <span style="font-size: 28px; color: black;">{args.name} Got up at</span>
        <span style="font-size: 40px; color: purple;"> {data_today}</span>
        <span style="font-size: 28px; color: black;"> today {emoji}</span>
    </p>
    </center>
</body>
<body>
    <center>
    <p>
        <span style="font-size: 28px; color: black;">{args.name} has been an</span>
        <span style="font-size: 32px; color: black;">  {character}</span>
        <span style="font-size: 28px; color: black;"> for</span>
        <span style="font-size: 40px; color: purple;">   {days}</span>
        <span style="font-size: 28px; color: black;"> consecutive days  {emoji}</span>
        <span style="font-size: 28px; color: blue;"> (  {before_or_after}  {real_time_to_hours_minutes(args.getup_threshold)})</span>
    </p>
    </center>
</body>
<body>
    <center><h2>Wake Up Time Statistics for Last {args.recent_days} days</h2></center>
    <div class="container">
        <div class="img">
            {plot_getup_recent_days}
        </div>
    </div>
</body>
</html>
    """

    with open('docs/index.md', 'w') as file:
        file.write(html_content)
   
def write_md_file_monthly(monthly_plot_html, monthly_pie_html):
    
    # 假设monthly_pie_html和yearly_pie_html已经由Plotly生成并包含圆饼图的HTML代码
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<body>
    <center><h2>Wake Up Time Statistics for {datetime.now().strftime("%B %Y")}</h2></center>
    <div class="container">
        <div class="img">
            {monthly_plot_html}
        </div>
        <div class="img">
            {monthly_pie_html}
        </div>
    </div>
</body>
</html>
    """

    with open('docs/home/monthly_stats.md', 'w') as file:
        file.write(html_content)
    
def write_md_file_yearly(yearly_plot_html, yearly_pie_html):
    
    # 假设monthly_pie_html和yearly_pie_html已经由Plotly生成并包含圆饼图的HTML代码
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<body>
    <center><h2>Wake Up Time Statistics for {datetime.now().strftime("%Y")}</h2></center>
    <div class="container">
        <div class="img">
            {yearly_plot_html}
        </div>
        <div class="img">
            {yearly_pie_html}
        </div>
    </div>
</body>
</html>
    """

    with open('docs/home/yearly_stats.md', 'w') as file:
        file.write(html_content)

def write_md_file_from_github():  
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<body>
    <center>
    <p>
        <span style="font-size: 28px; color: black;">{args.name} Got up at</span>
        <span style="font-size: 40px; color: purple;"> {times[-1].hour}:{times[-1].minute}:{times[-1].second}</span>
        <span style="font-size: 28px; color: black;"> today {emoji}</span>
    </p>
    </center>
</body>
<body>
    <center>
    <p>
        <span style="font-size: 28px; color: black;">{args.name} has been an</span>
        <span style="font-size: 32px; color: black;"> {Character}</span>
        <span style="font-size: 28px; color: black;"> for</span>
        <span style="font-size: 40px; color: purple;">  {days}</span>
        <span style="font-size: 28px; color: black;"> consecutive days {emoji}</span>
        <span style="font-size: 28px; color: blue;"> ({before_or_after} {real_time_to_hours_minutes(args.getup_threshold)})</span>
    </p>
    </center>
</body>
<body>
    <center><h2>Wake Up Time Statistics for Last {args.recent_days} days</h2></center>
    <div class="container">
        <div class="img">
            {plot_getup_recent_days}
        </div>
    </div>
</body>
</html>
    """



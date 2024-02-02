import csv
from datetime import datetime
import plotly.graph_objects as go

# 读取CSV文件中的时间数据
times = []
csv_file_path = 'run_times.csv'
with open(csv_file_path, mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过标题行
    for row in reader:
        if len(row) == 2:
            time_str = row[1]
            time_obj = datetime.strptime(time_str, '%H:%M:%S')
            times.append(time_obj.hour + time_obj.minute / 60 + time_obj.second / 3600)

# 使用Plotly创建直方图
fig = go.Figure(go.Histogram(
    x=times,
    xbins=dict(start=0, end=24, size=1),  # 指定直方图的分组范围和大小
    marker=dict(
        color='skyblue',
        line=dict(color='black', width=1),
    ),
    autobinx=False,
))

# 更新布局以添加圆角
fig.update_traces(marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)
fig.update_layout(
    title_text=f'Daily First Run Time Distribution for {datetime.now().strftime("%B %Y")}',  # 图表标题
    xaxis_title_text='Hour of Day',  # X轴标题
    yaxis_title_text='Frequency',  # Y轴标题
    bargap=0.2,  # 柱体之间的间隙大小
)

# 显示图表
fig.show()

# 保存图表为HTML文件
html_file_path = 'run_times_histogram_plotly.html'
fig.write_html(html_file_path)

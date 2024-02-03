import csv
from datetime import datetime
import os
import argparse
import sys
from utils import *
import argparse

# 创建参数解析器
argparser = argparse.ArgumentParser()
argparser.add_argument('--cutoff', type=float, default=5, help='The cutoff hour for counting runs in the last 7 days')
argparser.add_argument('--getup_threshold', type=float, default=8.5, help='The cutoff hour for counting runs in the last 7 days')
argparser.add_argument('--data', type=str, default='./docs/data/run_times.csv', help='The path to the data file')
argparser.add_argument('--recent_days', type=int, default=30, help='The number of recent days to plot')
argparser.add_argument('--name', type=str, default='Qihang', help='Your name')
argparser.add_argument('--manual_recording', type=bool, default=False, help='Whether to manually record the data')
args = argparser.parse_args()

# makedirs(data) 方法用于递归创建目录
os.makedirs('./docs/data', exist_ok=True)

now = datetime.now()
current_date = now.date()
current_time = now.strftime('%H:%M:%S')

if not os.path.exists(args.data):
    with open(args.data, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'First Run Time'])
    print("file has been created.")
        
if now.hour + now.minute / 60 < args.cutoff:
    print("You stayed up too late last night!")
    sys.exit()
else:
    if args.manual_recording:
        print("manual recording is enabled. Please enter the data manually in the CSV file before running the program")
    else:
        if not is_recorded(current_date, args.data):
            with open(args.data, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([current_date, current_time])
                print("data has been recorded.")
        else:
            print("You have already recorded today's data.")
            sys.exit()
    
times = []
with open(args.data, mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过标题行
    for row in reader:
        date, time = row
        date_time_obj = datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M:%S')
        times.append(date_time_obj)   
times = sorted(times)

current_month = datetime.now().month
current_year = datetime.now().year
times_this_month = [time for time in times if time.month == current_month and time.year == current_year]
times_this_year = [time for time in times if time.year == current_year]
times_recent_days = [time for time in times if time > datetime.now() - timedelta(days=args.recent_days)]

recent_runs_before_getup_threshold = max(
                            count_continuous_early_rises_from_yesterday(times),
                            count_continuous_early_rises_from_yesterday(times, last_date=datetime.now().date())
                            )
plot_getup_recent_days = plot_times_with_getup_threshold_and_line(times_recent_days, args.getup_threshold)

# 生成本月和本年的直方图
monthly_plot_html = generate_histogram_plotly_html(times_this_month, "Monthly Wake Up Time Distribution")
yearly_plot_html = generate_histogram_plotly_html(times_this_year, "Yearly Wake Up Time Distribution")

monthly_pie_html = generate_pie_chart_html(times_this_month, "Monthly Wake Up Time Pie Chart")
yearly_pie_html = generate_pie_chart_html(times_this_year, "Yearly Wake Up Time Pie Chart")

write_md_file(times, recent_runs_before_getup_threshold, args, plot_getup_recent_days, monthly_plot_html, yearly_plot_html, monthly_pie_html, yearly_pie_html)

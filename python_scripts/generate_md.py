import csv
from datetime import datetime
import os
import argparse
from utils import *
import argparse
import pdb

argparser = argparse.ArgumentParser()
argparser.add_argument('--cutoff', type=float, default=5, help='The cutoff hour for counting runs in the last 7 days')
argparser.add_argument('--getup_threshold', type=float, default=7.75, help='The cutoff hour for counting runs in the last 7 days')
argparser.add_argument('--data_dir', type=str, default='./data', help='The path to the data directory')
argparser.add_argument('--data', type=str, default='./data/run_times.csv', help='The path to the data file')
argparser.add_argument('--recent_days', type=int, default=30, help='The number of recent days to plot')
argparser.add_argument('--name', type=str, default='Qihang', help='Your name')
args = argparser.parse_args()

os.makedirs(args.data_dir, exist_ok=True)

now = datetime.now()
current_date = now.date()
current_time = now.strftime('%H:%M:%S')
    
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
                            count_continuous_early_rises_from_yesterday(times, last_date=datetime.now().date() + timedelta(days=1), getup_threshold=args.getup_threshold),
                            count_continuous_early_rises_from_yesterday(times, last_date=datetime.now().date(), getup_threshold=args.getup_threshold)
                            )
recent_runs_after_getup_threshold = count_continuous_late_rises_from_yesterday(times, getup_threshold=args.getup_threshold)

plot_getup_recent_days = plot_times_with_getup_threshold_and_line(times_recent_days, args.getup_threshold)

monthly_plot_html = generate_histogram_plotly_html(times_this_month, "Monthly Wake Up Time Distribution")

yearly_plot_html = generate_histogram_plotly_html(times_this_year, "Yearly Wake Up Time Distribution")
    
monthly_pie_html = generate_pie_chart_html(times_this_month, "Monthly Wake Up Time Pie Chart")
    
yearly_pie_html = generate_pie_chart_html(times_this_year, "Yearly Wake Up Time Pie Chart")

write_md_file_today(times, recent_runs_before_getup_threshold, recent_runs_after_getup_threshold, args, plot_getup_recent_days)
write_md_file_monthly(monthly_plot_html, monthly_pie_html)
write_md_file_yearly(yearly_plot_html, yearly_pie_html)
print("Markdown files have been written.")

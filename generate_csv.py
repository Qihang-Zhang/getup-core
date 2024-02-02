import csv
from datetime import datetime
import os
import argparse
import sys

# 创建参数解析器
argparser = argparse.ArgumentParser()
argparser.add_argument('--cutoff', type=float, default=5, help='The cutoff hour for counting runs in the last 7 days')
args = argparser.parse_args()

# 设置CSV文件路径
csv_file_path = './docs/data/run_times.csv'

# 获取当前日期和时间
now = datetime.now()
current_date = now.date()
current_time = now.strftime('%H:%M:%S')

if now.hour + now.minute / 60 < args.cutoff:
    print("You stayed up too late last night!")
    sys.exit()

# 检查文件是否存在，如果不存在，则创建并添加标题行
if not os.path.exists(csv_file_path):
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'First Run Time'])

# 读取CSV文件，检查今天的日期是否已经记录
already_recorded = False
with open(csv_file_path, mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) > 0 and row[0] == str(current_date):
            already_recorded = True
            break

# 如果今天的日期还没有记录，就添加一条新记录
if not already_recorded:
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_date, current_time])
        print("data has been recorded.")

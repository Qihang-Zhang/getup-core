import csv
from datetime import datetime
import os

# 设置CSV文件路径
csv_file_path = './docs/data/run_times.csv'

# 获取当前日期和时间
now = datetime.now()
current_date = now.date()
current_time = now.strftime('%H:%M:%S')

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

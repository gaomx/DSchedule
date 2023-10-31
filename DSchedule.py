# pip install icalendar

# %%
from fileinput import filename
import pandas as pd
import datetime
import os
import requests

url = 'http://y.saoju.net/yyj/artist/1538/download'  # 下载文件的URL
save_path = '/DSchedule/'  # 文件保存路径
now = datetime.datetime.now()
current_time = now.strftime("%Y-%m-%d_%H-%M-%S")
filename = "DSchedule" + current_time + ".csv"

# 发送HTTP GET请求并获取响应
response = requests.get(url)

# 检查响应状态码是否为200，表示请求成功
if response.status_code == 200:
    # 构造文件保存路径
    filepath = os.path.join(save_path, filename)

    # 写入文件
    with open(filepath, 'wb') as f:
        f.write(response.content)

df = pd.read_csv(filepath,
                encoding='utf-8',
                header=0, 
                parse_dates=[0], 
                date_parser=lambda x: pd.to_datetime(x, format='%Y/%m/%d %H:%M:%S')
                )

print(df)

# %%
from icalendar import Calendar, Event

cal = Calendar()
cal.add('version', '2.0')
cal.add('prodid', '-//139 Mail//calendar 2.3//CN')
cal.add('calscale', 'GREGORIAN')
cal.add('method', 'PUBLISH')
cal.add('x-wr-calname', 'DYWSchedule')
cal.add('x-wr-timezone', 'Asia/Shanghai')

for row in df.itertuples(index=False):
    stime, thing, description, location = row[0], row[2], row[3], row[4]

    # print(row[0], row[1], row[2])

    event = Event()
    event.add('summary', thing)
    event.add('dtstart', stime)
    event.add('location', location)
    event.add('description', description)
      # print(event)

    cal.add_component(event)

    txt = cal.to_ical()
    print(str(txt, encoding='utf8'))


# %%
with open('/DSchedule/DSchedule.ics', 'wb') as f:
    f.write(txt)

import requests
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser(description='查詢護照預約可點擊的日期')
parser.add_argument('--deptId', choices=['A', 'B', 'C', 'D', 'E'], required=True, help='部門ID (A: 外交部領事事務局, B: 外交部中部辦事處, C: 外交部雲嘉南辦事處, D: 外交部南部辦事處, E: 外交部東部辦事處)', default='A')
parser.add_argument('--year', type=int, required=True, help='年份 (例如: 2025)', default=2025)
parser.add_argument('--from', dest='from_month', type=int, required=True, help='起始月份 (1-12)', default=1)
parser.add_argument('--to', dest='to_month', type=int, required=True, help='結束月份 (1-12)', default=12)

args = parser.parse_args()

url = "https://ppass.boca.gov.tw/sp-a-service-1.html"

# multipart/form-data 的欄位用 files 傳遞（不是真的檔案，也可以）
files = {
    'action': (None, 'getCalendars'),
    'deptId': (None, args.deptId),
    'ApplyCnt': (None, '1'),
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'Origin': 'https://ppass.boca.gov.tw',
    'Referer': 'https://ppass.boca.gov.tw/sp-ipm-step1-2.html',
}

response = requests.post(url, files=files, headers=headers)

print("Status Code:", response.status_code)

html_text = response.text

soup = BeautifulSoup(html_text, 'html.parser')

# 根據命令列參數生成月份列表
months = []
for month in range(args.from_month, args.to_month + 1):
    months.append(f'{args.year}年{month:02d}月')
result = {}

for month in months:
    month_div = None
    for div in soup.find_all('div', class_='col'):
        time_tag = div.find('time')
        if time_tag and month in time_tag.text:
            month_div = div
            break

    if month_div:
        clickable_dates = []
        for td in month_div.find_all('td'):
            if 'Unclick' not in td.get('class', []) and td.a and 'javascript:SelectDate' in td.a.get('href', ''):
                date_text = td.a.span.text
                clickable_dates.append(date_text)
        result[month] = clickable_dates

for month, dates in result.items():
    print(f'{month} 可點擊的日期:', dates)

print('網站連結: https://ppass.boca.gov.tw/sp-ipm-step1-2.html')
print('祝您能比別人快撿到好時間！')

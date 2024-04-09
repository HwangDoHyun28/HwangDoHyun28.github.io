import requests
from bs4 import BeautifulSoup
import csv
import json

response = requests.get("http://paullab.synology.me/stock.html")

response.encoding = 'utf-8'
html = response.text

soup = BeautifulSoup(html, 'html.parser')

oneStep = soup.select('.main')[2]
twoStep = oneStep.select('tbody > tr')[1:]

날짜 = []
종가 = []
전일비 = []
거래량 = []

#################################
# 파일을 1개로 합친 이유 : 1번 크롤링 해서 모든 정보를 뽑아올 수 있기 때문
# 해당 서버의 부하를 줄이기 위해서 입니다.

시가총액 = soup.select('#_market_sum')[0].text
시가총액순위 = soup.select('#_market_sum')[1].text
상장주식수 = soup.select('#_market_sum')[2].text
나머지값 = soup.select('tr > td')
배당수익률 = 나머지값[5].text.strip()
매출 = 나머지값[6].text
비용 = 나머지값[7].text
순익 = 나머지값[8].text

##################################

for i in twoStep:
    날짜.append(i.select('td')[0].text)
    종가.append(int(i.select('td')[1].text.replace(',', '')))
    전일비.append(int(i.select('td')[2].text.replace(',', '')))
    거래량.append(int(i.select('td')[6].text.replace(',', '')))

l = []

for i in range(len(날짜)):
    l.append({
        '날짜': 날짜[i],
        '종가': 종가[i],
        '전일비': 전일비[i],
        '거래량': 거래량[i],
    })

# 파일을 한 번 쓴다.
with open('data.js', "w", encoding="UTF-8-sig") as f_write:
    json.dump(l, f_write, ensure_ascii=False, indent=4)

# 파일을 다시 읽는다.
data = ""
with open('data.js', "r", encoding="UTF-8-sig") as f:
    line = f.readline()
    while line:
        data += line
        line = f.readline()

# 파일에 변수명을 추가하여 다시 쓴다.

final_data = f"var data = {data};"
final_data = f"var 시가총액 = '{시가총액}';\n\
var 시가총액순위 = '{시가총액순위}';\n\
var 상장주식수 = '{상장주식수}';\n\
var 배당수익률 = '{배당수익률}';\n\
var 매출 = '{매출}';\n\
var 비용 = '{비용}';\n\
var 순익 = '{순익}';\n\
" + final_data

with open('data.js', "w", encoding="UTF-8-sig") as f_write:
    f_write.write(final_data)

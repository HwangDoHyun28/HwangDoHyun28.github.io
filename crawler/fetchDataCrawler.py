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

시가총액 = soup.select('#_market_sum')[0].text
시가총액순위 = soup.select('#_market_sum')[1].text
상장주식수 = soup.select('#_market_sum')[2].text
나머지값 = soup.select('tr > td')
배당수익률 = 나머지값[5].text.strip()
매출 = 나머지값[6].text
비용 = 나머지값[7].text
순익 = 나머지값[8].text

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

with open('json/fetchtestdata.json', "w", encoding="UTF-8-sig") as f_write:
    json.dump(l, f_write, ensure_ascii=False, indent=4)

ll = [{
      "이름": "제주코딩베이스캠프",
      "시가총액": 시가총액,
      "시가총액순위": 시가총액순위,
      "상장주식수": 상장주식수,
      "배당수익률": 배당수익률,
      "매출": 매출,
      "비용": 비용,
      "순익": 순익
      }]

with open('json/fetchtestbasicdata.json', "w", encoding="UTF-8-sig") as f_write:
    json.dump(ll, f_write, ensure_ascii=False, indent=4)

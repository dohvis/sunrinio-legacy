from bs4 import BeautifulSoup as bs
from requests import get
from re import search
import json

year = "2016"
month = "07"
url = "http://stu.sen.go.kr/sts_sci_md00_001.do"
param = {
    "insttNm": "선린인터넷고등학교",
    "schulCode": "B100000658",
    "schulCrseScCode": "4",
    "schulKndScCode": "04",
    "ay": year,
    "mm": month,
}

html = get(url, params=param).text
print("connect")
soup = bs(html, "html.parser")
table = soup.find("table")
rows = table.find_all("tr")
data = {}
for r in rows:
    for x in r.find_all('td'):
        today = str(x)
        try:
            date = search(r"(\d?\d)", today).group(0)
        except AttributeError:
            continue
        l_index = today.find("[중식]")
        d_index = today.find("[석식]")
        lunch_list = today[l_index:d_index].split("<br/>")
        dinner_list = today[d_index:today.find("</div>")].split("<br/>")

        if len(lunch_list) > 1:
            lunch_list = lunch_list[1:-1]  # to delete dummy data
        else:
            continue

        if len(dinner_list) > 1:
            dinner_list = lunch_list[1:]  # to delete dummy data
        else:
            continue
        for menu in lunch_list:
            last_one = menu[-1:]
            last_two = menu[-2:]

            if last_one == '밥' or menu[-3:] == '라이스':
                print('밥')
            elif last_one == '국' or last_one == '탕' \
                    or last_two == '찌개' or last_two == '스프':
                print('국')
            elif last_two == '박이' or last_two == '김치' or last_two == '두기':
                print("김치")
            elif last_two == '소스':
                print("소스")
            else:
                print(menu)
        data[str(date)] = {0: None, 1: None}
        data[str(date)][0], data[str(date)][1] = lunch_list, dinner_list

print(json.dumps(data, ensure_ascii=False, indent=4))

import requests
from bs4 import BeautifulSoup
import datetime as dt
from datetime import timedelta

#국내 농구 일정
input = dt.date.today() - timedelta(0)
ans = ""

def Search(search):
    global ans
    #오프시즌일 때
    if search.month in offSeason:
        ans += f"{search}일은 시즌 중의 날짜가 아닙니다."
    search = search.strftime("%Y-%m-%d")
    for data in dataList:
        if(data["dateForSearch"] == search):
            # 경기일정이 있을 때
            if (data.get('time') != '-'):
                # 끝나거나, 진행 중인 경기일 때
                if (data.get('homeScore') != '-'):
                    # 홈 팀이 이겼을 떄
                    if (int(data.get('homeScore')) > int(data.get('awayScore'))):
                        ans += f"{data.get('date')}에 {data.get('stadium')}경기장에서 진행된 경기는\n(홈){data.get('home')} {data.get('homeScore')} : {data.get('awayScore')} {data.get('away')}(원정) 으로 홈팀 {data.get('home')}이(가) 승리하였습니다\n\n"

                    # 원정 팀이 이겼을 때
                    if (int(data.get('homeScore')) < int(data.get('awayScore'))):
                        ans += f"{data.get('date')}에 {data.get('stadium')}경기장에서 진행된 경기는\n(홈){data.get('home')} {data.get('homeScore')} : {data.get('awayScore')} {data.get('away')}(원정) 으로 원정팀 {data.get('away')}이(가) 승리하였습니다\n\n"

                # 경기가 취소됐을 때
                elif(data.get('platform') == "해당 경기는 현지 사정으로 취소되었습니다."):
                    ans += f"{data.get('date')} {data.get('time')}에 {data.get('stadium')}경기장에서 진행 될 (홈){data.get('home')} VS {data.get('away')}(원정) {data.get('platform')}\n"
                # 진행 예정인 경기일 때
                else:
                    ans += f"{data.get('date')} 일정은 {data.get('time')}에\n(홈){data.get('home')} VS {data.get('away')}(원정) 경기가 {data.get('stadium')}경기장에서 진행될 예정입니다.\n\n"

            # 경기 일정이 없을 때
            else:
                ans += f"{data.get('date')}요일 경기 일정은 없습니다."
    return ans
offSeason = [7,8,9]
months = [1,2,3,4,5,6,10,11,12]
dataList = []
for month in months :
    url = f"https://sports.news.naver.com/basketball/schedule/index?date=20221001&month={month}&year=2022&teamCode=&category=nba"
    res = requests.get(url)
    res.raise_for_status() #웹 정보를 못 불러왔을 경우 오류 출력

    soup = BeautifulSoup(res.text, "lxml")
    soupData = [soup.findAll("div",{"class" : "sch_tb"}),soup.findAll("div",{"class" : "sch_tb2"})] #짝수, 홀수
    for dataTb in soupData:
        for data in dataTb:
            #모든 날짜
            dateValue = data.find("span", {"class": "td_date"}).text

            # input을 위한 날짜 정규화
            dateValue2 = data.find("strong").text
            dateValue2 = dateValue2.split(".")
            if (int(dateValue2[0]) < 10):
                if (int(dateValue2[1]) > 0 and int(dateValue2[1]) < 10):
                    dateValue2 = f"2022-0{dateValue2[0]}-0{dateValue2[1]}"
                else:
                    dateValue2 = f"2022-0{dateValue2[0]}-{dateValue2[1]}"
            else:
                if (int(dateValue2[1]) > 0 and int(dateValue2[1]) < 10):
                    dateValue2 = f"2022-{dateValue2[0]}-0{dateValue2[1]}"
                else:
                    dateValue2 = f"2022-{dateValue2[0]}-{dateValue2[1]}"

            if (len(dateValue.split(" ")[0].split(".")[1]) == 1):
                dateValue = dateValue.split(" ")[0].split(".")[0] + ".0" + dateValue.split(" ")[0].split(".")[1] + " " + dateValue.split(" ")[1]

            matchNum = data.find("td")["rowspan"] #경기가 없는 날의 rowspan == 5, 있는 날의 rowspan은 경기수
            if (int(matchNum) == 5):
                matchNum = '1'
            for i in range(int(matchNum)):
                matchData = {} #모든 경기정보 저장하는 딕셔너리
                #날짜
                matchData["date"] = dateValue
                matchData["dateForSearch"] = dateValue2
                #시간
                matchData["time"] = data.findAll("tr")[i].find("span", {"class": "td_hour"}).text
                if matchData["time"] != "-":  # 경기 일정이 있을때
                    # 홈팀
                    matchData["home"] = data.findAll("tr")[i].find("span", {"class": "team_rgt"}).text
                    # 어웨이팀
                    matchData["away"] = data.findAll("tr")[i].find("span", {"class": "team_lft"}).text
                    # VS일 시 무승부나 진행예정경기
                    if data.findAll("tr")[i].find("strong", {"class": "td_score"}).text != "VS":  # 종료된 경기일 때
                        # 홈팀 스코어
                        matchData["homeScore"] = \
                        data.findAll("tr")[i].find("strong", {"class": "td_score"}).text.split(":")[1]
                        # 어웨이팀 스코어
                        matchData["awayScore"] = \
                        data.findAll("tr")[i].find("strong", {"class": "td_score"}).text.split(":")[0]
                    else:  # 진행 예정 경기일 떄
                        matchData["homeScore"] = "-"
                        matchData["awayScore"] = "-"
                    #경기장
                    matchData["stadium"] = data.findAll("tr")[i].findAll("span", {"class": "td_stadium"})[0].text
                else:  # 경기 일정이 없을 시
                    matchData["home"] = "-"
                    matchData["away"] = "-"
                    matchData["homeScore"] = "-"
                    matchData["awayScore"] = "-"
                    matchData["stadium"] = "-"
                dataList.append(matchData)
#print(dataList)
a = Search(input)
print(a)












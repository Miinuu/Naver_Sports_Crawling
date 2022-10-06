import requests
from bs4 import BeautifulSoup
import datetime as dt

#국내 야구 일정

#일정 조회 함수

input = dt.date.today()
input = input.strftime("%Y-%m-%d")

def Schdeul_Search(search):
    for key, item in matchData.items():
        if (key == 'dateForSearch'):
            if (item == search):
                if (matchData.get('time') != '-'):
                    ans = f"{matchData.get('date')} 일정은 {matchData.get('time')}에 홈 팀 {matchData.get('home')}, 원정 팀 {matchData.get('away')}(으)로 {matchData.get('stadium')}경기장에서 " \
                             f"진행될 예정이며, {matchData.get('platform')}을 통해서 중계됩니다."
                else:
                    ans = "금일 경기 일정은 없습니다."
                return ans



months = [3,4,5,6,7,8,9,10]
for month in months :
    url = f"https://sports.news.naver.com/kbaseball/schedule/index?date=20220929&month={month}&year=2022&teamCode="
    res = requests.get(url)
    res.raise_for_status() #웹 정보를 못 불러왔을 경우 오류 출력
    soup = BeautifulSoup(res.text, "lxml")

    soupData = [soup.findAll("div", {"class" : "sch_tb"}),soup.findAll("div", {"class" : "sch_tb2"})] #sch_tb 짝수날짜, sch_tb2 홀수날짜
    dataList = []

    for dataTb in soupData:
        for data in dataTb:
            #모든 날짜
            dateValue = data.find("span",{"class" : "td_date"}).text
            #input을 위한 날짜 정규화
            dateValue2 = data.find("strong").text
            dateValue2 = dateValue2.split(".")
            if(int(dateValue2[1])>0 and int(dateValue2[1])<10):
                dateValue2 = f"2022-{dateValue2[0]}-0{dateValue2[1]}"
            else:
                dateValue2 = f"2022-{dateValue2[0]}-{dateValue2[1]}"

            if(len(dateValue.split(" ")[0].split(".")[1]) ==1):
                #날짜 정규화
                dateValue = dateValue.split(" ")[0].split(".")[0] + ".0" + dateValue.split(" ")[0].split(".")[1] + " " + dateValue.split(" ")[1]
            matchNum = data.find("td")["rowspan"]
            for i in range(int(matchNum)):
                matchData = {} #모든 경기 정보 저장하는 딕셔너리
                #날짜
                matchData["date"] = dateValue
                matchData["dateForSearch"] = dateValue2
                #시간
                matchData["time"] = data.findAll("tr")[i].find("span",{"class":"td_hour"}).text
                #경기 없을 시 matchData["time"] = "-"
                if matchData["time"] != "-" : #경기 일정이 있을때
                    #홈팀
                    matchData["home"] = data.findAll("tr")[i].find("span", {"class" : "team_lft"}).text
                    #어웨이팀
                    matchData["away"] = data.findAll("tr")[i].find("span", {"class" : "team_rgt"}).text
                    # VS일 시 진행예정경기
                    if data.findAll("tr")[i].find("strong", {"class":"td_score"}).text != "VS" : #종료된 경기일 때
                        #홈팀 스코어
                        matchData["homeScore"] = data.findAll("tr")[i].find("strong", {"class":"td_score"}).text.split(":")[1]
                        #어웨이팀 스코어
                        matchData["awayScore"] = data.findAll("tr")[i].find("strong", {"class": "td_score"}).text.split(":")[0]
                    else :#진행 예정 경기일 떄
                        matchData["homeScore"] = "-"
                        matchData["awayScore"] = "-"
                    #경기장
                    matchData["stadium"] = data.findAll("tr")[i].findAll("span", {"class" : "td_stadium"})[1].text
                    #중계방송사
                    matchData["platform"] = data.findAll("tr")[i].findAll("span", {"class": "td_stadium"})[0].text.strip()
                else : #경기 일정이 없을 시
                    matchData["home"] = "-"
                    matchData["away"] = "-"
                    matchData["homeScore"] = "-"
                    matchData["awayScore"] = "-"
                    matchData["stadium"] = "-"
                    matchData["platform"] = "-"
                dataList.append(matchData)

            Schdeul_Search("2022-08-07")

           #print(matchData.items())

            ''''for key, item in matchData.items():
                if (key == 'dateForSearch'):
                    if (item == '2022-10-06'):
                        if (matchData.get('time') != '-'):
                            ans = f"{matchData.get('date')} 일정은 {matchData.get('time')}에 홈 팀 {matchData.get('home')}, 원정 팀 {matchData.get('away')}(으)로 {matchData.get('stadium')}경기장에서 " \
                                     f"진행될 예정이며, {matchData.get('platform')}을 통해서 중계됩니다."
                        else:
                            ans = "금일 경기 일정은 없습니다."
                        print(ans)'''


    #데이터 정렬
    #result = sorted(dataList,key= lambda x: x["date"].split(" ")[0])
    #print(result)


#print(input)


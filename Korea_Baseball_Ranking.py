import requests
from bs4 import BeautifulSoup

#국내 야구 순위


url = f"https://sports.news.naver.com/kbaseball/record/index?category=kbo"
res = requests.get(url)
res.raise_for_status() #웹 정보를 못 불러왔을 경우 오류 출력

soup = BeautifulSoup(res.text, "lxml")
soupData = soup.find("tbody",{"id" : "regularTeamRecordList_table"})
dataList= [] #모든 순위정보 저장 리스트
for data in soupData.find_all("tr"):
    teamData = {} #순위 정보 저장 딕셔너리
    rank_tag = data.find("th")
    # 팀 순위
    teamData["rank"] = rank_tag.find('strong').text
    # 팀 이름
    teamData["team"] = data.findAll("span")[1].text
    # 경기수
    teamData["total"] = data.findAll("span")[2].text
    # 승리수
    teamData["win"] = data.findAll("span")[3].text
    # 패배수
    teamData["lose"] = data.findAll("span")[4].text
    # 무승부 수
    teamData["draw"] = data.findAll("span")[5].text
    # 승률
    teamData["winRate"] = round((int(teamData["win"]) / int(teamData["total"])),3)
    # 게임차
    teamData["diffrence"] = data.findAll("span")[6].text
    # 연속
    teamData["streak"] = data.findAll("span")[7].text
    # 출루율
    teamData["onBasePer"] = data.findAll("span")[8].text
    # 장타율
    teamData["slugPer"] = data.findAll("span")[9].text
    # 최근 10경기
    teamData["lastTenMatches"] = data.findAll("span")[10].text
    dataList.append(teamData)   
    print(teamData["winRate"])

print(dataList)

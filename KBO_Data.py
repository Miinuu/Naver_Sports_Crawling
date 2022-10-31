import requests
from bs4 import BeautifulSoup

#국내 야구 순위

def Baseball_TeamData(team):
    for key, item in teamData.items():
        if (key == 'team'):
            if (item == team):
                ans = f"{teamData.get('team')}팀의 순위는 {teamData.get('rank')}입니다." \
                      f"현재 {teamData.get('total')}전 {teamData.get('win')}승 {teamData.get('lose')}패 {teamData.get('draw')}무를 기록 중이며," \
                      f"승률은 {teamData.get('winRate')}%로 1위와는 현재 {teamData.get('difference')} 게임차입니다." \
                      f"출루율은 {teamData.get('onBasePer')}, 장타율은 {teamData.get('slugPer')}입니다." \
                      f"최근 10게임 전적은 {teamData.get('lastTenMatches')}입니다."
            else:
                ans = "해당 팀은 존재하지 않습니다."
        return ans

ans = ""
url = f"https://sports.news.naver.com/kbaseball/record/index?category=kbo"
res = requests.get(url)
res.raise_for_status() #웹 정보를 못 불러왔을 경우 오류 출력

soup = BeautifulSoup(res.text, "lxml")
soupData = soup.find("tbody",{"id" : "regularTeamRecordList_table"})
dataList= [] #모든 순위정보 저장 리스트
for data in soupData.findAll("tr"):
    ans = ""
    teamData = {} #순위 정보 저장 딕셔너리
    # 팀 순위
    teamData["rank"] = data.findAll('strong')[0].text
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
    teamData["winRate"] = data.findAll('strong')[1].text
    # 게임차
    teamData["difference"] = data.findAll("span")[6].text
    # 연속
    teamData["streak"] = data.findAll("span")[7].text
    # 출루율
    teamData["onBasePer"] = data.findAll("span")[8].text
    # 장타율
    teamData["slugPer"] = data.findAll("span")[9].text
    # 최근 10경기
    teamData["lastTenMatches"] = data.findAll("span")[10].text
    dataList.append(teamData)

def Search(teamname):
    global ans
    for data in dataList:
        if (data["team"].replace(" ","") == teamname.replace(" ","")):
            ans = f"{data.get('team')}의 순위는 {data.get('rank')}위입니다.\n" \
                  f"현재 {data.get('total')}전 {data.get('win')}승 {data.get('lose')}패 {data.get('draw')}무를 기록 중으로 " \
                  f"승률은 {float(data.get('winRate')) * 100}%, 1위와 {data.get('difference')} 게임차입니다.\n" \
                  f"출루율은 {data.get('onBasePer')}, 장타율은 {data.get('slugPer')}입니다.\n" \
                  f"최근 10게임 전적은 {data.get('lastTenMatches')}입니다."
            break
        else:
            ans = "해당 팀은 존재하지 않습니다."
    return ans
a = Search('KT')
print(a)
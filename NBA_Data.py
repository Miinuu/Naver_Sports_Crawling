import requests
from bs4 import BeautifulSoup

#국내 농구 순위

locations = ["EAST","WEST"]
dataList= [] #모든 순위정보 저장 리스트
for location in locations:
    url = f"https://sports.news.naver.com/basketball/record/index?category=nba&year=2023&conference={location}"
    res = requests.get(url)
    res.raise_for_status()  # 웹 정보를 못 불러왔을 경우 오류 출력

    soup = BeautifulSoup(res.text, "lxml")
    soupData = soup.find("tbody", {"id": "regularTeamRecordList_table"})
    for data in soupData.findAll("tr"):
        teamData = {} #순위 정보 저장 딕셔너리
        # 팀 순위
        teamData["rank"] = data.findAll("strong")[0].text
        # 팀 이름
        teamData["team"] = data.findAll("span")[1].text
        # 디비전
        teamData["division"] = data.findAll("span")[2].text
        # 경기수
        teamData["total"] = data.findAll("span")[3].text
        # 승리수
        teamData["win"] = data.findAll("span")[4].text
        # 패배수
        teamData["lose"] = data.findAll("span")[5].text
        # 승률
        teamData["winRate"] = data.findAll("strong")[1].text
        # 승차
        teamData["difference"] = data.findAll("span")[6].text
        # 홈승
        teamData["homeWin"] = data.findAll("span")[7].text
        # 홈패
        teamData["homeLose"] = data.findAll("span")[8].text
        # 원정승
        teamData["awayWin"] = data.findAll("span")[9].text
        # 원정패
        teamData["awayLose"] = data.findAll("span")[10].text
        # 디비전승
        teamData["divisionWin"] = data.findAll("span")[11].text
        # 디비전패
        teamData["divisionLose"] = data.findAll("span")[12].text
        # 연속
        teamData["winStreak"] = data.findAll("span")[13].text
        dataList.append(teamData)

def Search(teamname):
    for data in dataList:
        if (data['team'].replace(" ","") == teamname.replace(" ","")):
            ans = f"{data.get('division')}디비전 {data.get('team')}의 순위는 {data.get('rank')}위입니다.\n" \
                  f"현재 {data.get('total')}전 {data.get('win')}승 {data.get('lose')}패를 기록 중으로 " \
                  f"승률은 {round(float(data.get('winRate')) * 100,3)}%, 1위와 {data.get('difference')} 게임차입니다.\n" \
                  f"홈 승: {data.get('homeWin')}승 홈 패: {data.get('homeLose')}패 원정 승: {data.get('awayWin')}승 원정 패: {data.get('awayLose')}패 연속: {data.get('winStreak')} "
            break
        else:
            ans = "해당 팀은 존재하지 않습니다."
    return ans
#print(dataList)
a = Search('LAL')
print(a)
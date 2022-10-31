import requests
from bs4 import BeautifulSoup

#국내 농구 순위


url = f"https://sports.news.naver.com/basketball/record/index?category=kbl"
res = requests.get(url)
res.raise_for_status() #웹 정보를 못 불러왔을 경우 오류 출력

soup = BeautifulSoup(res.text, "lxml")
soupData = soup.find("tbody",{"id" : "regularTeamRecordList_table"})
dataList= [] #모든 순위정보 저장 리스트
for data in soupData.findAll("tr"):
    teamData = {} #순위 정보 저장 딕셔너리
    # 팀 순위
    teamData["rank"] = data.findAll("strong")[0].text
    # 팀 이름
    teamData["team"] = data.findAll("span")[1].text
    # 경기수
    teamData["total"] = data.findAll("span")[2].text
    # 승리수
    teamData["win"] = data.findAll("span")[3].text
    # 패배수
    teamData["lose"] = data.findAll("span")[4].text
    # 승률
    teamData["winRate"] = data.findAll("strong")[1].text
    # 승차
    teamData["difference"] = data.findAll("span")[5].text
    # 득점
    teamData["points"] = data.findAll("span")[6].text
    # 어시스트
    teamData["assist"] = data.findAll("span")[7].text
    # 리바운드
    teamData["rebound"] = data.findAll("span")[8].text
    # 스틸
    teamData["steal"] = data.findAll("span")[9].text
    # 블록
    teamData["block"] = data.findAll("span")[10].text
    # 3점슛
    teamData["threePoint"] = data.findAll("span")[11].text
    # 자유투
    teamData["freethrow"] = data.findAll("span")[12].text
    # 자유투 성공률
    teamData["freethrowPer"] = data.findAll("span")[13].text
    dataList.append(teamData)

def Search(teamname):
    for data in dataList:
        if (data['team'].replace(" ","") == teamname.replace(" ","")):
            ans = f"{data.get('team')}의 순위는 {data.get('rank')}위입니다.\n" \
                  f"현재 {data.get('total')}전 {data.get('win')}승 {data.get('lose')}패를 기록 중으로 " \
                  f"승률은 {float(data.get('winRate')) * 100}%, 1위와 {data.get('difference')} 게임차입니다.\n\n" \
                  f"========================== 팀 데이터 ==========================\n"\
                  f"득점: {data.get('points')} 어시스트: {data.get('assist')} 리바운드: {data.get('rebound')} 스틸: {data.get('steal')} 블로킹: {data.get('block')}\n" \
                  f"3점 슛: {data.get('threePoint')} 자유투: {data.get('freethrow')} 자유투 성공률: {data.get('freethrowPer')}"
            break
        else:
            ans = "해당 팀은 존재하지 않습니다."
    return ans
a = Search('')
print(a)
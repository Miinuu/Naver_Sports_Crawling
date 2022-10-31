import requests
from bs4 import BeautifulSoup

#국내 배구

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
genders = ["kovo","wkovo"]
dataList= [] #모든 순위정보 저장 리스트
for gender in genders:
    url = f"https://sports.news.naver.com/volleyball/record/index?category={gender}&year=2022"
    res = requests.get(url)
    res.raise_for_status() #웹 정보를 못 불러왔을 경우 오류 출력

    soup = BeautifulSoup(res.text, "lxml")
    soupData = soup.find("tbody",{"id" : "regularTeamRecordList_table"})

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
        # 세트득실률
        teamData["setScore"] = data.findAll("span")[5].text
        # 점수 득실률
        teamData["pointPer"] = data.findAll("span")[6].text
        # 세트수
        teamData["set"] = data.findAll("span")[7].text
        # 공격 성공률
        teamData["attackPer"] = data.findAll("span")[8].text
        # 블로킹
        teamData["blocking"] = data.findAll("span")[9].text
        # 서브
        teamData["serve"] = data.findAll("span")[10].text
        # 득점
        teamData["score"] = data.findAll("span")[11].text
        dataList.append(teamData)
def Search(teamname):
    global ans
    for data in dataList:
        if (data["team"].replace(" ","") == teamname.replace(" ","")):
            ans = f"{data.get('team')}의 순위는 {data.get('rank')}위입니다.\n" \
                  f"현재 {data.get('total')}전 {data.get('win')}승 {data.get('lose')}패를 기록 중입니다.\n" \
                  f"==================== 팀 데이터 ====================\n"\
                  f"세트: {data.get('set')} 세트득실률: {data.get('setScore')} 점수득실률: {data.get('pointPer')}\n" \
                  f"공격성공률: {data.get('attackPer')} 블로킹: {data.get('blocking')} 서브: {data.get('serve')} 득점: {data.get('score')}"
            break
        else:
            ans = "해당 팀은 존재하지 않습니다."
    return ans
a = Search('대한 항공')
print(a)
# 머신러닝 데이터베이스 (과거 경기 데이터 저장)
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# API 키 및 헤더 설정
API_KEY = os.getenv("API_SPORTS_KEY")
HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "v3.football.api-sports.io"
}

# API 호출 함수
def fetch_fixtures(team_id, season):
    """
    API-Sports에서 특정 팀의 경기 데이터를 가져옵니다.
    """
    url = "https://v3.football.api-sports.io/fixtures"
    params = {"team": team_id, "season": season}
    
    response = requests.get(url, headers=HEADERS, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"API 요청 실패: {response.status_code}")
        return None

# 데이터 수집 및 가공 함수
def collect_match_data(team_id, season, output_file="match_data.csv"):
    """
    특정 팀의 시즌 경기 데이터를 수집하고 CSV로 저장합니다.
    """
    data = fetch_fixtures(team_id, season)
    if not data or "response" not in data:
        print("API 데이터가 유효하지 않습니다.")
        return

    fixtures = data["response"]
    match_data = []

    for fixture in fixtures:
        match = fixture["fixture"]
        teams = fixture["teams"]
        goals = fixture["goals"]

        # 승리 팀 결정
        if teams["home"]["winner"]:
            winner = teams["home"]["name"]  # 홈 팀 승리
        elif teams["away"]["winner"]:
            winner = teams["away"]["name"]  # 원정 팀 승리
        else:
            winner = "Draw"  # 무승부

        # 데이터 가공
        match_data.append({
            "date": match["date"],  # 경기 날짜
            "home_team": teams["home"]["name"],  # 홈 팀
            "away_team": teams["away"]["name"],  # 원정 팀
            "home_score": goals["home"],  # 홈 팀 득점
            "away_score": goals["away"],  # 원정 팀 득점
            "winner": winner,  # 승리 팀
            "status": match["status"]["short"]  # 경기 상태
        })


    # DataFrame으로 변환
    df = pd.DataFrame(match_data)

    # CSV 파일로 저장
    df.to_csv(output_file, index=False)
    print(f"{output_file}에 데이터가 저장되었습니다.")

# 실행 부분
if __name__ == "__main__":
    TEAM_ID = 530  # Atlético Madrid ID
    SEASON = 2021  # 분석할 시즌
    OUTPUT_FILE = "match_data.csv"

    collect_match_data(TEAM_ID, SEASON, OUTPUT_FILE)


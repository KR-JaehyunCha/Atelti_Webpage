from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
import os
import json
import joblib
import logging
from dotenv import load_dotenv
from .utils import fetch_api_data
from operator import itemgetter
from datetime import datetime

# .env 파일 로드
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  # 환경 변수에서 API 키 가져오기
)

# API_Sports 설정
API_KEY = os.getenv("API_SPORTS_KEY")
HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "v3.football.api-sports.io"
}

# 로깅 설정
logger = logging.getLogger(__name__)

# Home 페이지 뷰
def index(request):
    return render(request, 'index.html')

# Players 페이지 뷰
def players(request):
    endpoint = "https://v3.football.api-sports.io/players"
    params = {
        "team": 530,  # Atlético Madrid ID
        "season": 2021  # 무료 플랜의 시즌
    }

    data = fetch_api_data(endpoint, params, HEADERS)

    if "error" in data:
        return render(request, 'players.html', {'error': data["error"]})

    # 선수 데이터 가공
    players = [
        {
            "id": player["player"]["id"],
            "name": player["player"]["name"],
            "position": player["statistics"][0]["games"]["position"],
            "nationality": player["player"]["nationality"],
            "birth_date": player["player"]["birth"]["date"],
            "image_url": player["player"]["photo"]
        }
        for player in data["response"]
    ]

    return render(request, 'players.html', {'players': players})

# Match Schedule 페이지 뷰
def schedule(request):
    endpoint = "https://v3.football.api-sports.io/fixtures"
    params = {
        "team": 530,  # Atlético Madrid ID
        "season": 2021  # 무료 플랜에서는 2022 시즌 사용 가능
    }

    # API 데이터 가져오기
    data = fetch_api_data(endpoint, params, HEADERS)

    if "error" in data:
        return render(request, 'schedule.html', {'error': data["error"]})

    # 데이터 가공
    matches = [
        {
            "date": datetime.strptime(fixture["fixture"]["date"], "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d %H:%M"),
            "opponent": fixture["teams"]["away"]["name"] if fixture["teams"]["home"]["id"] == 530 else fixture["teams"]["home"]["name"],
            "home_away": "Home" if fixture["teams"]["home"]["id"] == 530 else "Away",
            "result": f'{fixture["score"]["fulltime"]["home"]}-{fixture["score"]["fulltime"]["away"]}' if fixture["score"]["fulltime"]["home"] is not None else "TBD",
            "league": fixture["league"]["name"],
            "league_logo": fixture["league"]["logo"]
        }
        for fixture in data["response"]
    ]

        # 날짜순으로 정렬
    matches = sorted(matches, key=itemgetter("date"))

    # 템플릿에 전달
    return render(request, 'schedule.html', {'matches': matches})

# Chatbot 엔드포인트
def chatbot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()

        # OpenAI API 호출
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ],
        )

        # 응답 반환
        bot_response = completion.choices[0].message.content.strip()
        return JsonResponse({'response': bot_response})

    return JsonResponse({'response': 'Invalid request method.'}, status=405)

def player_detail(request, player_id):
    endpoint = f"https://v3.football.api-sports.io/players"
    params = {
        "id": player_id,
        "season": 2021
    }

    data = fetch_api_data(endpoint, params, HEADERS)

    if "error" in data:
        return JsonResponse({"error": data["error"]}, status=400)

    if not data["response"]:
        return JsonResponse({"error": "No data found for the player."}, status=404)

    player = data["response"][0]["player"]
    statistics = data["response"][0]["statistics"][0]

    player_detail = {
        "name": player["name"],
        "position": statistics["games"]["position"],
        "nationality": player["nationality"],
        "birth_date": player["birth"]["date"],
        "image_url": player["photo"],
        "goals": statistics["goals"]["total"],
        "assists": statistics["goals"]["assists"]
    }

    return JsonResponse(player_detail)

# 모델 로드
model_path = os.path.join(os.path.dirname(__file__), 'match_predictor.pkl')
model = joblib.load(model_path)

def predict_match(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        home_score = data.get('home_score', 0)
        away_score = data.get('away_score', 0)

        # 예측 (피처 이름 없이 데이터만 전달)
        prediction = model.predict([[home_score, away_score]])
        result = ['Home Win', 'Draw', 'Away Win'][prediction[0]]

        return JsonResponse({'prediction': result})

    return JsonResponse({'error': 'Invalid request'}, status=400)
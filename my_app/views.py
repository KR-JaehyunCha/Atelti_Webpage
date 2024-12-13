from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
import requests
import os
import json
import logging
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  # 환경 변수에서 API 키 가져오기
)

# API_Sports API 키
API_KEY = os.getenv("API_SPORTS_KEY")
API_URL = "https://v3.football.api-sports.io/players"

# 로깅 설정
logger = logging.getLogger(__name__)

# Home 페이지 뷰
def index(request):
    return render(request, 'index.html')  # index.html 파일 렌더링

# Match Schedule 페이지 뷰
def schedule(request):
    return render(request, 'schedule.html')  # schedule.html 파일 렌더링

# Players 페이지 뷰
def players(request):
    return render(request, 'players.html')  # players.html 파일 렌더링

## Chatbot 엔드포인트
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

# Players 엔드포인트
def players(request):
    team_id = 530  # Atlético Madrid ID
    season = 2021
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "v3.football.api-sports.io"
    }
    params = {
        "team": team_id,
        "season": season
    }

    try:
        # API 호출
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        # 선수 데이터 가공
        players = [
            {
                "name": player["player"]["name"],
                "position": player["statistics"][0]["games"]["position"],
                "nationality": player["player"]["nationality"],
                "birth_date": player["player"]["birth"]["date"],
                "image_url": player["player"]["photo"]
            }
            for player in data["response"]
        ]

        # 템플릿에 데이터 전달
        return render(request, 'players.html', {'players': players})
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching players: {e}")
        return render(request, 'players.html', {'error': 'Failed to fetch player data.'})
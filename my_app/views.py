from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
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
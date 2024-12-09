from django.shortcuts import render
from .models import Player  # Players 데이터를 사용하기 위해 모델 임포트

# Home 페이지 뷰
def index(request):
    return render(request, 'index.html')

# Players 페이지 뷰
def players(request):
    players = Player.objects.all()  # 데이터베이스에서 모든 Player 데이터를 가져옴
    return render(request, 'players.html', {'players': players})

# Match Schedule 페이지 뷰
def schedule(request):
    return render(request, 'schedule.html')



from django.shortcuts import render
from .models import Player  # Players 데이터를 사용하기 위해 모델 임포트
from .models import Match

# Match Schedule
def schedule(request):
    matches = Match.objects.all().order_by('date')  # 날짜순 정렬
    return render(request, 'schedule.html', {'matches': matches})

# Home 페이지 뷰
def index(request):
    return render(request, 'index.html')

# Players 페이지 뷰
def players(request):
    players = Player.objects.all()  # 데이터베이스에서 모든 Player 데이터를 가져옴
    return render(request, 'players.html', {'players': players})
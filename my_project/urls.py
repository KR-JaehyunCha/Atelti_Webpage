"""
URL configuration for my_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from my_app import views

urlpatterns = [
    path('admin/', admin.site.urls),                 # Django 관리자 페이지
    path('', views.index, name='home'),              # Home 페이지
    path('players/', views.players, name='players'), # Players 페이지
    path('schedule/', views.schedule, name='schedule'), # Match Schedule 페이지
    path('schedule/add/', views.schedule, name='add_match'), # 경기 일정 추가 페이지
    path('schedule/api/', views.schedule, name='match_api'), # 경기 일정 API 처리
    path('chatbot/', views.chatbot, name='chatbot'),
    path('player/<int:player_id>/', views.player_detail, name='player_detail'),
    path('predict', views.predict_match, name='predict_match'),
]
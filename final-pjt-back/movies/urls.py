from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.movies_main), # 메인 영화 조회
    path('create/', views.movie_create), # 영화 등록
    path('<int:sort_num>/sort/', views.movie_sort), # 필터링된 영화 정보(장르 포함)
    path('<int:movie_pk>/', views.movie_detail), # 단일 영화 조회
    path('<int:movie_pk>/review/', views.movie_review), # 영화별 게시글 조회
    path('<int:genre_id>/genre/', views.movie_genre), # 장르별 추천 영화 조회
    path('<int:movie_pk>/edit/', views.movie_update_or_delete), # 영화 수정 및 삭제 : 관리자만 가능하게 해야함(관리자 번호 : 1) 
    path('<int:movie_pk>/rate/', views.movie_rate), # 로그인 유저의 평점 등록
    path('<int:user_pk>/rate_list/', views.movie_rate_list), # 평점 조회
    path('<int:movie_pk>/rate/<int:rate_pk>/', views.movie_rate_update_or_delete), # 로그인 유저의 평점 수정/삭제
    path('<int:movie_pk>/like/', views.movie_like), # 영화 좋아요 등록 및 해제(좋아요 수까지 출력)
    path('<int:movie_pk>/wish/', views.movie_wish),# 위시리스트 등록 및 해제(위시리스트 수까지 출력)


]
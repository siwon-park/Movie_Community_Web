from django.urls import path
from . import views

app_name = 'accounts'
# 회원가입(POST) : account/signup/
# 프로필 정보 조회 및 수정(GET/PUT) : account/user
# 비밀번호 번형(POST) : account/password/change/
# 비밀번호 찾기(POST) : account/password/reset/

urlpatterns = [
    path('delete/', views.user_delete,), # 회원탈퇴
    path('<int:user_pk>/list/', views.user_movie_list), # 사용자가 좋아요/위시리스트/평점을 준 영화 목록 조회각 목록과 그 수를 출력)
    path('<int:user_pk>/hate_genre/', views.hate_genre_list), # 싫어하는 장르 조회
    path('<int:user_pk>/hate_genre/<int:genre_pk>/', views.hate_genre_update_or_delete), # 싫어하는 장르 등록 및 해제
    path('<int:user_pk>/follow/', views.follow), # 팔로우 등록 및 해제 : 팔로우 수까지
    path('<int:user_pk>/follow/list/', views.follow_list), # 팔로우 조회
    path('<int:user_pk>/profile/', views.user_profile),# 상대방 프로필 조회
    path('<int:user_pk>/friend/', views.user_friend), # 지역을 고려한 친구 추천
    path('<int:user_pk>/reco_like/', views.user_reco_like), # 사용자가 좋아요를 한 영화리스트에서 해당 영화와 유사한 영화를 출력
    path('<int:user_pk>/reco_rate/', views.user_reco_rate), # 사용자가 평점을 준 영화리스트에서 가장 높은 평점을 받은 영화와 유사한 영화를 출력
]
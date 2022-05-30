from django.db import models
from django.conf import settings


class Genre(models.Model):
    id = models.IntegerField(primary_key=True) # 장르 id
    name = models.CharField(max_length=50) # 장르 name


class Movie(models.Model):
    # null, blank : 빈 값, null 가능 여부
    id = models.IntegerField(primary_key=True) # 영화 id
    title = models.CharField(max_length=100)
    release_date = models.DateField(null=True, blank=True)
    popularity = models.FloatField(null=True, blank=True) # 관객 수
    overview = models.TextField(null=True, blank=True)
    vote_average = models.FloatField(null=True, blank=True) # 평점
    vote_count = models.IntegerField(null=True, blank=True) # 평점 투표수
    poster_path = models.CharField(max_length=200, null=True, blank=True)
    # 예고편 링크
    video_url = models.CharField(max_length=200, null=True, blank=True)

    # 영화를 등록한 사용자
    register_manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='register_movies', default=1)
    # 장르
    genre_check = models.ManyToManyField(Genre, related_name='genre_movies')
    # 영화를 좋아요한 사용자
    like_movie_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies', blank=True)
    # 위시리스트에 담은 사용자
    wish_lists_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='wish_moives', blank=True)
    # 평점을 준 사용자 : 중개 테이블 작성(through)
    rates_users = models.ManyToManyField('accounts.User', related_name='user_rated_movie', through='Rate')

    

# 평점 중개 테이블 직접 작성 : 평점 필드가 필요함
class Rate(models.Model):
    rate_user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='user_rated')
    rate_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    # 사용자가 준 평점 : 추가 필드
    rate_score = models.FloatField()

from dataclasses import field
from rest_framework import serializers
from movies.models import Movie, Rate
from django.contrib.auth import get_user_model

User = get_user_model()

# 로그인한 유저의 평점 등록/수정/삭제/조회
class RateSerializer(serializers.ModelSerializer):

    class MovieSerializer(serializers.ModelSerializer):

        class Meta:
            model = Movie
            fields = ('title',)

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('username',)
    
    rate_movie = MovieSerializer(read_only=True)
    rate_user = UserSerializer(read_only=True)

    class Meta:
        model = Rate
        # 평점 id, 평점을 준 영화 제목, 평점을 준 사용자, 평점
        fields = '__all__'


# 사용자가 평점을 준 영화 목록 조회
class UserRateSerializer(serializers.ModelSerializer):

    class MovieSerializer(serializers.ModelSerializer):

        class Meta:
            model = Movie
            fields = ('id','title',)

    class RateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Rate
            fields = ('id', 'rate_score', 'rate_movie',)
    
    user_rated = RateSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'user_rated')
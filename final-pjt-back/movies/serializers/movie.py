from rest_framework import serializers
from community.models import Review
from movies.models import *
from django.contrib.auth import get_user_model

User = get_user_model()

# 전체/단일/장르별 영화 조회
class MovieListSerializer(serializers.ModelSerializer):   

    class GenreSerializer(serializers.ModelSerializer):
 
        class Meta:
            model = Genre
            # 단일 컬럼 출력 시 ,(콤마) 필수(없으면 인식 못함) 
            fields = '__all__'
    
    genre_check = GenreSerializer(many=True)
    like_movie_users_count = serializers.IntegerField() # 좋아요한 사용자 수
    wish_lists_users_count = serializers.IntegerField() # 위시리스트에 담은 사용자 수
    review_movie_count = serializers.IntegerField() # 리뷰글의 수

    class Meta:
        model = Movie
        # 영화 id, 좋아요한 사용자 수, 위시리스트에 담은 사용자 수, 리뷰글의 수, 제목, 장르(id, name), 개봉일, 관객 수, 평점, 포스터 주소, 개요
        fields = ('id', 'like_movie_users_count', 'wish_lists_users_count', 'review_movie_count', 'title', 'genre_check', 'release_date', 'popularity', 'vote_average', 'poster_path', 'overview')


# 영화별 게시글 조회
class MovieReviewSerializer(serializers.ModelSerializer):   
    
    class ReviewSerializer(serializers.ModelSerializer):
        class Meta:
            model = Review
            fields = '__all__'

    write_movie_review = ReviewSerializer(many=True) # 영화에 작성된 게시글


    class Meta:
        model = Movie
        # 영화 id, 영화에 작성된 게시글
        fields = ('id', 'write_movie_review')

# 영화 등록: 관리자만 가능하게 해야함(관리자 번호 : 1)
class MovieRegisterSerializer(serializers.ModelSerializer):   

    class GenreSerializer(serializers.ModelSerializer):
 
        class Meta:
            model = Genre
            # 단일 컬럼 출력 시 ,(콤마) 필수(없으면 인식 못함) 
            fields = '__all__'
    
    genre_check = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        # 영화 id, 제목, 장르(id, name), 개봉일, 관객 수, 평점, 포스터 주소, 개요
        fields = ('id', 'title', 'genre_check', 'release_date', 'popularity', 'vote_average', 'poster_path', 'overview',)


# 영화 수정, 삭제 : 관리자만 가능하게 해야함(관리자 번호 : 1)
class MovieUpdateSerializer(serializers.ModelSerializer):   

    class GenreSerializer(serializers.ModelSerializer):
 
        class Meta:
            model = Genre
            # 단일 컬럼 출력 시 ,(콤마) 필수(없으면 인식 못함) 
            fields = '__all__'
    
    genre_check = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        # 영화 id, 제목, 장르(id, name), 개봉일, 관객 수, 평점, 포스터 주소, 개요
        fields = ('id', 'title', 'genre_check', 'release_date', 'popularity', 'vote_average', 'poster_path', 'overview')
        read_only_fields = ('id',)


# 영화 좋아요 등록 및 해제
class MovieLikeSerialzer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'username',)

    # 좋아요한 사용자
    like_movie_users = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Movie
        # 영화 id, 좋아요를 한 사용자 목록, 좋아요 수
        fields = ('id','like_movie_users', )


# 영화 위시리스트 등록 및 해제
class MovieWishSerialzer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'username',)

    # 위시리스트를 등록 사용자
    wish_lists_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        # 영화 id, 위시리스트를 등록한 사용자 목록
        fields = ('id', 'wish_lists_users')


    


    
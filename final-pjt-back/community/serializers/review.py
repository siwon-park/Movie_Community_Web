from queue import Empty
from rest_framework import serializers
from community.models import Review
from movies.models import Movie
from django.contrib.auth import get_user_model
from .comment import CommentSerializer

User = get_user_model()

# 전체 게시글 목록 조회 및 영화를 선택하지 않은 게시글 생성
class ReviewListSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'username',)
    
    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('id', 'title',)

    write_review_movie = MovieSerializer(read_only=True) # 게시글이 달린 영화
    write_review_user = UserSerializer(read_only=True) # 게시글 작성자
    comment_count = serializers.IntegerField() # 댓글 수
    like_count = serializers.IntegerField() # 좋아요 수
    
    
    class Meta:
        model = Review
        # 전체 게시글 출력 필드
        # id, 제목, 생성 시간, 좋아요 수, 댓글 수, 작성자, 리뷰한 영화 제목
        fields = ('id', 'title', 'created_at', 'updated_at', 'like_count', 'comment_count', 'write_review_user', 'write_review_movie')



# 단일 게시글 조회, 수정, 삭제
class ReviewSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'username',)

    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('id', 'title',)

    write_review_movie = MovieSerializer(read_only=True) # 게시글이 달린 영화
    write_review_user = UserSerializer(read_only=True) # 게시글 작성자
    like_count = serializers.IntegerField(read_only=True) # 좋아요 수
    comment_count = serializers.IntegerField(read_only=True) # 댓글 수

    class Meta:
        model = Review
        # 전체 게시글 출력 필드
        # 게시글 id, 작성자, 제목, 내용, 생성 시간, 좋아요 수, 댓글 수, 게시글이 달린 영화
        fields = ('id', 'write_review_user', 'title', 'content', 'updated_at', 'created_at', 'like_count', 'comment_count', 'write_review_movie',)


# 게시글 좋아요 등록 및 해제
class ReviewLikeSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'username',)
    
    like_review_users = UserSerializer(many=True, read_only=True) # 좋아요한 작성자

    class Meta:
        model = Review
        # 게시글 id, 좋아요한 사용자 목록
        fields = ('id', 'like_review_users')



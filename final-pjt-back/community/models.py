from django.db import models
from django.conf import settings

class Review(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 게시글이 달린 영화
    write_review_movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='write_movie_review', null=True, blank=True)
    # 게시글을 작성한 사용자
    write_review_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='write_review') 
    # 게시글을 좋아요한 사용자
    like_review_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')


class Comment(models.Model):
    content = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 댓글 작성자
    write_comment_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='write_comment')
    # 상위 댓글
    super_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='commented', null=True, blank=True)
    # 댓글을 좋아요한 사용자
    like_comment_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments')
    # 댓글이 달린 리뷰글
    commented_review= models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_comment')



class Question(models.Model):
    title = models.CharField(max_length=50)
    # 투표를 하고 답변을 남긴 사용자 : 중개 테이블 작성(through)
    question_answer = models.ManyToManyField('accounts.User', through='Vote')


# 투표 중개 테이블 직접 작성 : 의견을 적은 필드가 필요함
class Vote(models.Model):
    vote_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    vote_user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    # 사용자가 선택한 답변(T/F 로 응답을 2개로 나눔)
    vote_answer = models.BooleanField()
    # 사용자가 남긴 의견
    vote_content = models.CharField(max_length=100, null=True, blank=True)
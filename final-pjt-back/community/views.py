from django.http import JsonResponse
from django.db.models import Count
from django.shortcuts import get_object_or_404
from .models import *
from .serializers.review import *
from .serializers.comment import *
from .serializers.question import *
from rest_framework import status
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes


# 전체 게시글 목록 조회 및 영화를 선택하지 않은 게시글 생성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
def review_list_or_create(request):
    # 게시글 전체 조회
    def review_list():
        reviews = Review.objects.annotate(
                comment_count=Count('review_comment', distinct=True), # 댓글 수
                like_count=Count('like_review_users', distinct=True) # 좋아요 수
            ).order_by('-pk')
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)

    # 게시글 생성
    def review_create():
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # 게시글 작성자 입력 변수 주의 !!
            serializer.save(write_review_user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == 'GET':
        return review_list()
    elif request.method == 'POST':
        return review_create()

# 필터링된 게시글 정보(최신순, 좋아요, 댓글 많은 순)
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
def review_sort(request, sort_num):
    reviews = Review.objects.annotate(
                comment_count=Count('review_comment', distinct=True), # 댓글 수
                like_count=Count('like_review_users', distinct=True) # 좋아요 수
            )
    if sort_num == 1: # 최신순
        sort_reviews = reviews.order_by('-created_at')
    elif sort_num == 2: # 좋아요 순
        sort_reviews = reviews.order_by('-like_count')
    elif sort_num == 3: # 댓글 많은 순
        sort_reviews = reviews.order_by('-comment_count')
        
    serializer = ReviewListSerializer(sort_reviews, many=True)
    return Response(serializer.data)


# 영화를 선택한 게시글 생성
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def review_create_with_movie(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # 게시글 작성자 입력 변수 주의 !!
        serializer.save(write_review_user = request.user, write_review_movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 단일 게시글 조회, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
def review_detail_or_update_or_delete(request, review_pk):
    reviews = Review.objects.annotate(
            comment_count=Count('review_comment', distinct=True), # 댓글 수
                like_count=Count('like_review_users', distinct=True)) # 좋아요 수
    review = get_object_or_404(reviews, pk=review_pk)

    def review_detail():
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    def review_update():
        if request.user == review.write_review_user:
            serializer = ReviewSerializer(review, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)

    def review_delete():
        if request.user == review.write_review_user:
            review.delete()
            data = {
            'delete': f'게시글 {review_pk}번이 삭제되었습니다.'
            }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    if request.method == 'GET':
        return review_detail()
    elif request.method == 'PUT':
        if request.user == review.write_review_user:
            return review_update()
    elif request.method == 'DELETE':
        if request.user == review.write_review_user:
            return review_delete()


# 게시글 좋아요 등록 및 해제
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def review_like(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    user = request.user
    if review.like_review_users.filter(pk=user.pk).exists():
        review.like_review_users.remove(user)
    else:
        review.like_review_users.add(user)
        
    serializer = ReviewLikeSerializer(review)

    like_status = {
        'id' : serializer.data.get('id'),
        'count' : review.like_review_users.count(),
        'like_list' : serializer.data.get('like_review_users'),
    }    
    return JsonResponse(like_status)


# (최상위) 기본 댓글 생성 및 게시글 별 댓글 조회
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
def comment_list_or_create(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    def comment_list():
        serializer = ReivewOnlySerializer(review)
        # 해당 댓글이 달린 게시물의 모든 댓글 출력
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def comment_create():
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(commented_review=review, write_comment_user=request.user)
            serializer = ReivewOnlySerializer(review)
            # 생성 시, 해당 댓글이 달린 게시물의 모든 댓글 출력
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == 'GET':
        return comment_list()
    elif request.method == 'POST':
        return comment_create()


# 대댓글 생성 및 전체 댓글 수정 및 삭제
@api_view(['POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def comment_update_or_delete(request, review_pk, comment_pk):
    # 대댓글 생성 시 : 댓글을 단 게시글 번호, 상위 댓글이 될 번호
    # 수정 및 삭제 시 : 댓글을 단 게시글 번호, 수정/삭제하려는 댓글 번호
    review = get_object_or_404(Review, pk=review_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    def comment_create():
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_super = Comment.objects.get(id=comment_pk)
            serializer.save(commented_review=review, write_comment_user=request.user, super_comment=new_super)

            serializer = ReivewOnlySerializer(review)
            # 생성 시, 해당 댓글이 달린 게시물의 모든 댓글 출력
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def comment_update():
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            serializer = ReivewOnlySerializer(review)
            # 수정 시, 수정된 댓글이 달린 게시물의 모든 댓글 출력
            return Response(serializer.data)

    def comment_delete():
        delete_data = {'content': '삭제된 댓글입니다.'}
        serializer = CommentSerializer(comment, data=delete_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            serializer = ReivewOnlySerializer(review)
            return Response(serializer.data)

            
    if request.method == 'POST':
        return comment_create()
    elif request.method == 'PUT':
        if request.user == comment.write_comment_user:
            return comment_update()
    elif request.method == 'DELETE':
        if request.user == comment.write_comment_user:
            return comment_delete()


# 댓글 좋아요 등록 및 해제
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def comment_like(request, review_pk, comment_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    user = request.user
    if comment.like_comment_users.filter(pk=user.pk).exists():
        comment.like_comment_users.remove(user)
        serializer = ReivewOnlySerializer(review)
        return Response(serializer.data)
    else:
        comment.like_comment_users.add(user)
        serializer = ReivewOnlySerializer(review)
        return Response(serializer.data)


# 댓글 별 좋아요 개수 조회
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
def comment_like_count(request, review_pk, comment_pk):
    comments = Comment.objects.annotate(
        like_comment_users_count = Count('like_comment_users', distinct=True)
    )

    comment = comments.get(pk=comment_pk)
    serializer = CommentLikeSerializer(comment)
    return Response(serializer.data)

# 주제등록
@api_view(['POST'])
@permission_classes([IsAdminUser]) # 관리자(is_staff)만 권한 허용
def question_create(request):
    serializer = QuestionRegisterSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)  


# 주제와 전체 응답 수 조회
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
def question(request, question_pk):
    questions = Question.objects.annotate(
        question_answer_count=Count('question_answer', distinct=True))
        
    question = get_object_or_404(questions, pk=question_pk)
    
    serializer = QuestionSerializer(question)
    return Response(serializer.data)


# 주제와 특정 응답 수 조회
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
def vote(request, question_pk, vote_no):
    # 특정 문제 선택
    questions = Question.objects.filter(pk=question_pk)
    # 특정 응답에 대한 응답 개수 출력
    new_question = questions.filter(vote__vote_answer=vote_no).annotate(
        # distinct는 응답의 개수를 count : 현재 2개로 고정이므로 의미 없음
        new_question_answer_count = Count('vote__vote_answer'),
    )
    serializer = QuestionVoteSerializer(new_question, many=True)
    return Response(serializer.data)

# 투표 등록
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def vote_like(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk)
    # 현재 사용자가 이미 해당 주제에 투표를 했으면 추가하면 안됨
    if Vote.objects.filter(vote_user=request.user,vote_question_id=question_pk).exists():
        data = {
            'content': f'{request.user}님은  이미 해당 주제{question.title}에 투표했습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    else:
        serializer = VotePickSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(vote_question=question, vote_user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
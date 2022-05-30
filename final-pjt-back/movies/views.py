from datetime import date
from django.http import JsonResponse
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import *
from .serializers.movie import *
from .serializers.rate import *
from rest_framework import status
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

movies = Movie.objects.annotate(
        like_movie_users_count=Count('like_movie_users', distinct=True), # 좋아요한 사용자 수
        wish_lists_users_count=Count('wish_lists_users', distinct=True), # 위시리스트에 담은 사용자 수
        review_movie_count=Count('write_movie_review', distinct=True)) # 리뷰글의 수)

User = get_user_model()

# 전체 영화 조회(메인)
# 인증 안해도 조회만 가능
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
def movies_main(request):
    # 가장 최근 개봉한 영화 중, 평점이 높은 순으로 정렬
    # 정렬기준에 따라 쿼리문 수정하여 정렬 가능 !!
    main_movies = movies.filter(release_date__lte=date.today()).order_by('-release_date', '-vote_average')[:30]
    serializer = MovieListSerializer(main_movies, many=True)
    print(main_movies)
    return Response(serializer.data)


# 영화 등록 : 관리자만 가능하게 해야함(관리자 번호 : 1)
@api_view(['POST'])
@permission_classes([IsAdminUser]) # 관리자(is_staff)만 권한 허용
def movie_create(request):
    serializer = MovieRegisterSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # 작성자 입력 변수 주의 !!
        serializer.save(register_manager = request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



# 필터링된 영화 정보
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
def movie_sort(request, sort_num):
    if sort_num == 1: # 관객수(popularity)
        sort_movies = movies.order_by('-popularity')[:30]
    elif sort_num == 2: # 최신순(개봉한 영화만)
        sort_movies = movies.filter(release_date__lte=date.today()).order_by('-release_date')[:30]
    elif sort_num == 3: # 개봉예정작 : 빠른 개봉 순으로
        sort_movies = movies.filter(release_date__gt=date.today()).order_by('release_date')[:30]
    elif sort_num == 4: # 리뷰 많은 순(개봉한 영화만), 최신순
        sort_movies = movies.filter(release_date__lte=date.today()).order_by('-review_movie_count', '-release_date')[:30]
    elif sort_num == 5: # 평점순(vote_average/개봉한 영화)
        sort_movies = movies.filter(release_date__lte=date.today()).order_by('-vote_average') [:30] 
    # 장르 포함
    elif sort_num == 12: # 모험
        sort_movies = movies.filter(genre_check=12).order_by('-release_date')[:30]
    elif sort_num == 14: # 판타지
        sort_movies = movies.filter(genre_check=14).order_by('-release_date')[:30]
    elif sort_num == 16: # 애니메이션
        sort_movies = movies.filter(genre_check=16).order_by('-release_date')[:30]
    elif sort_num == 18: # 드라마
        sort_movies = movies.filter(genre_check=18).order_by('-release_date')[:30]
    elif sort_num == 27: # 공포
        sort_movies = movies.filter(genre_check=27).order_by('-release_date')[:30]
    elif sort_num == 28: # 액션
        sort_movies = movies.filter(genre_check=28).order_by('-release_date')[:30]
    elif sort_num == 35: # 코미디
        sort_movies = movies.filter(genre_check=35).order_by('-release_date')[:30]
    elif sort_num == 36: # 역사
        sort_movies = movies.filter(genre_check=36).order_by('-release_date')[:30]
    elif sort_num == 37: # 서부
        sort_movies = movies.filter(genre_check=37).order_by('-release_date')[:30]
    elif sort_num == 53: # 스릴러
        sort_movies = movies.filter(genre_check=53).order_by('-release_date')[:30]
    elif sort_num == 80: # 범죄
        sort_movies = movies.filter(genre_check=80).order_by('-release_date')[:30]
    elif sort_num == 99: #다큐멘터리
        sort_movies = movies.filter(genre_check=99).order_by('-release_date')[:30]
    elif sort_num == 878: # SF
        sort_movies = movies.filter(genre_check=878).order_by('-release_date')[:30]
    elif sort_num == 9648: # 미스터리
        sort_movies = movies.filter(genre_check=9648).order_by('-release_date')[:30]
    elif sort_num == 10402: # 음악
        sort_movies = movies.filter(genre_check=10402).order_by('-release_date')[:30]
    elif sort_num == 10749: # 로맨스
        sort_movies = movies.filter(genre_check=10749).order_by('-release_date')[:30]
    elif sort_num == 10751: # 가족
        sort_movies = movies.filter(genre_check=10751).order_by('-release_date')[:30]
    elif sort_num == 10752: # 전쟁
        sort_movies = movies.filter(genre_check=10752).order_by('-release_date')[:30]
    elif sort_num == 10770: # TV 영화
        sort_movies = movies.filter(genre_check=10770).order_by('-release_date')[:30]
    serializer = MovieListSerializer(sort_movies, many=True)
    return Response(serializer.data)

    

# 단일 영화 조회
# 인증안해도 조회만 가능
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
def movie_detail(request, movie_pk):
    movie = movies.get(pk=movie_pk)
    serializer = MovieListSerializer(movie)
    return Response(serializer.data)


# 영화별 게시글 조회
@api_view(['GET']) 
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
def movie_review(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    serializer = MovieReviewSerializer(movie)
    return Response(serializer.data)


# 랜덤으로 유사 장르 추천 영화 출력 : 영화 세부 페이지
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
def movie_genre(request, genre_id):
    genre_movie = movies.filter(
        genre_check=genre_id,
        release_date__lte=date.today()).order_by('?')[:3]
    serializer = MovieListSerializer(genre_movie, many=True)
    return Response(serializer.data)


# 영화 수정 및 삭제 : 관리자만 가능하게 해야함(관리자 번호 : 1) 
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAdminUser]) # 관리자(is_staff)만 권한 허용
def movie_update_or_delete(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    def movie_update():
        serializer = MovieUpdateSerializer(movie, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def movie_delete():
        movie.delete()
        data = {
            'delete': f'영화 {movie_pk}번이 삭제되었습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    if request.method == 'PUT':
        if request.user == movie.register_manager:
            return movie_update()
    elif request.method == 'DELETE':
        if request.user == movie.register_manager:
            return movie_delete()


# 로그인한 유저의 평점 등록
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def movie_rate(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    # 현재 사용자가 이미 해당 영화에 평점을 등록했으면 추가하면 안됨
    if Rate.objects.filter(rate_user=request.user, rate_movie_id=movie_pk).exists():
        data = {
            'content' : f'{request.user}님은 이미 해당 영화({movie.title})에 투표했습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    else:
        serializer = RateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # 작성자 입력 변수 주의 !!
            serializer.save(rate_movie=movie, rate_user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

# 평점 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def movie_rate_list(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    serializer = UserRateSerializer(user)
    return Response(serializer.data)


# 로그인한 유저의 평점 수정/삭제
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def movie_rate_update_or_delete(request, movie_pk, rate_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    rate = get_object_or_404(Rate, pk=rate_pk)

    def movie_rate_update():
        serializer = RateSerializer(instance=rate, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def movie_rate_delete():
        rate.delete()
        data = {
            'content': f'영화({movie.title})에 대한 평점({rate.rate_score})이 삭제되었습니다.',
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    if request.method == 'PUT':
        if request.user == rate.rate_user:
            return movie_rate_update()  
    elif request.method == 'DELETE':
        if request.user == rate.rate_user:
            return movie_rate_delete()

# 영화 좋아요 등록 및 해제(좋아요 수까지 출력)
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def movie_like(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user
    # 해제
    if movie.like_movie_users.filter(pk=user.pk).exists():
        movie.like_movie_users.remove(user)
    # 등록
    else:
        movie.like_movie_users.add(user)

    serializer = MovieLikeSerialzer(movie)

    like_movie_register = {
        'id' : serializer.data.get('id'),
        'like_movie_users_count' : movie.like_movie_users.count(),
        'like_movie_users' : serializer.data.get('like_movie_users'),
    }
    return JsonResponse(like_movie_register)


# 영화 위시리스트 등록 및 해제(위시리스트 수까지 출력)
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def movie_wish(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user
    # 해제
    if movie.wish_lists_users.filter(pk=user.pk).exists():
        movie.wish_lists_users.remove(user)
    # 등록
    else:
        movie.wish_lists_users.add(user)
    serializer = MovieWishSerialzer(movie)

    wish_movie_register = {
        'id' : serializer.data.get('id'),
        'wish_lists_users_count' : movie.wish_lists_users.count(),
        'wish_lists_users' : serializer.data.get('wish_lists_users'),
    }
    return JsonResponse(wish_movie_register)



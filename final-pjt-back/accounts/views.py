import json
import random
import datetime
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .serializers.account import *
from movies.serializers.rate import *
from rest_framework import status
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

User = get_user_model()

# 회원가입
# 인증 필요 없이 접근 가능한 영역 : 추후 인증 필요
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = AccountSignUpSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 프로필 정보 조회 및 수정
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def profile_update(request, username):
    Users = get_object_or_404(User, username=username)
    if request.user == User:
        serializer = ProfileSerializer(instance=Users, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            serializer = ProfileSerializer(Users)
            return Response(serializer.data)

# 회원탈퇴
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def user_delete(request):
    request.user.delete()
    data = {
            'content': f'{request.user}님의 탈퇴처리가 완료되었습니다.',
        }
    return Response(data, status=status.HTTP_204_NO_CONTENT)


# 사용자가 좋아요/위시리스트/평점을 준 영화 목록 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def user_movie_list(request, user_pk):
    Users = get_object_or_404(User, pk=user_pk)
    serializer = UserMovieListSerializer(Users)
    user_list = {
        'id' : serializer.data.get('id'),
        'user_rated_movie_count' : Users.user_rated_movie.count(),
        'user_rated_movie' : serializer.data.get('user_rated_movie'),
        'like_movies_count' : Users.like_movies.count(),
        'like_movies' : serializer.data.get('like_movies'),
        'wish_moives_count' : Users.wish_moives.count(),
        'wish_moives' : serializer.data.get('wish_moives'),
    }
    return JsonResponse(user_list)

# 싫어하는 장르 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def hate_genre_list(request, user_pk):
    Users = get_object_or_404(User, pk=user_pk)
    serializer = HateGerneSerializer(Users)
    user_hate_list = {
        'id' : serializer.data.get('id'),
        'username' : serializer.data.get('username'),
        'hate_genres_count' : Users.hate_genres.count(),
        'hate_genres' : serializer.data.get('hate_genres'),
    }
    return JsonResponse(user_hate_list)

# 싫어하는 장르 등록 및 해제
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def hate_genre_update_or_delete(request, user_pk, genre_pk):
    user_genre = get_object_or_404(User, pk=user_pk)
    genre_picks = get_object_or_404(Genre, pk=genre_pk)
    genre = genre_picks.id

    if user_genre.hate_genres.filter(pk=genre_pk).exists():
        user_genre.hate_genres.remove(genre)
    else:
        user_genre.hate_genres.add(genre)

    serializer = HateRegisterSerializer(user_genre)

    user_hate_register = {
        'id' : serializer.data.get('id'),
        'username' : serializer.data.get('username'),
        'hate_genres_count' : user_genre.hate_genres.count(),
        'hate_genres' : serializer.data.get('hate_genres'),
    }
    
    return JsonResponse(user_hate_register)

# 팔로우 등록 및 해제 : 팔로우 수까지
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def follow(request, user_pk):
    # user_pk : 팔로우 하려는 사람의 pk
    follow_user = get_object_or_404(User, pk=user_pk)
    user = request.user
    if follow_user != user:
        if follow_user.followings.filter(pk=user.pk).exists():
            follow_user.followings.remove(user)
            follow = '팔로우' # 현재 버튼을 누르면 발생하는 동작
        else:
            follow_user.followings.add(user)
            follow = '언팔로우' # 현재 버튼을 누르면 발생하는 동작

        serializer = FollowSerializer(follow_user)

        follow_status = {
            'follow' : follow,
            'count' : follow_user.followings.count(), 
            # 팔로워(from_user_id가 팔로우 당한사람 : user_pk)(followings가 팔로우를 한 사람) 목록
            'follow_list' : serializer.data.get('followings'),
            # 팔로잉 수
            'following_count' : follow_user.followers.count(),
        }
    return JsonResponse(follow_status)


# 팔로우 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def follow_list(request, user_pk):
    # user_pk : 나의 pk
    follow_user = get_object_or_404(User, pk=user_pk)
    # user = request.user
    # if follow_user.followings.filter(pk=user.pk).exists():
    #     follow_user.followings.remove(user)
    #     follow = '팔로우' # 현재 버튼을 누르면 발생하는 동작
    # else:
    #     follow_user.followings.add(user)
    #     follow = '언팔로우' # 현재 버튼을 누르면 발생하는 동작

    serializer = FollowSerializer(follow_user)

    follow_status = {
        # 팔로워
        'follower_count' : follow_user.followings.count(), 
        # 팔로워(from_user_id가 팔로우 당한사람 : user_pk)(followings가 팔로우를 한 사람) 목록
        'follow_list' : serializer.data.get('followings'),
        # 팔로잉 수
        'following_count' : follow_user.followers.count(),
    }
    return JsonResponse(follow_status)


# 상대방 프로필 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def user_profile(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    serializer = UserProfileSerializer(user)
    return Response(serializer.data)


# 지역을 고려한 친구 추천
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def user_friend(request, user_pk):# user_pk : 나의 pk
    me = get_object_or_404(User, pk=user_pk)
    # user = request.user # username이 출력
    serializer = UserProfileSerializer(me) # 나의 정보를 추출
    # 연도 추출 : 나의 나이 +-3
    year = int(serializer.data.get('birth_date')[:4])
    first_date = datetime.date(year - 3, 1, 1)
    last_date = datetime.date(year + 3, 12, 31)
    # 나를 제외하고 지역이 같은 사람을 추출
    friends = User.objects.filter(
        region=serializer.data.get('region'),
        birth_date__range=(first_date, last_date)).exclude(username=me)
    serializer = UserProfileSerializer(friends, many=True)
    if friends.exists():
        return Response(serializer.data)
    else:
        data = {
            'content': f'추천 친구가 없습니다.',
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


# 사용자가 좋아요를 한 영화리스트에서 해당 영화와 유사한 영화를 출력
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def user_reco_like(request, user_pk):
    # 콘텐츠 기반 추천 : 사용자가 특정 아이템을 선호하는 경우 그 아이템과 비슷한 콘텐츠를 가진 다른 아이템을 추천해주는 방식
    
    # 1. json 데이터 추출하고 장르 id를 name으로 변경
    movies_json = open('./movies/fixtures/movie_data.json', encoding='UTF8')
    movies_list = json.load(movies_json)
    
    gerne_json = open('./movies/genres.json', encoding='UTF8')
    gerne_list = json.load(gerne_json)


    # 사용자가 싫어하는 장르 id 선택
    Users = get_object_or_404(User, pk=user_pk)
    serializer = HateGerneSerializer(Users)
    genre_lst = serializer.data.get('hate_genres')
    hate_list = []
    if not hate_list:
        for i in range(len(genre_lst)):
            hate_list.append(genre_lst[i]['id'])

    # 싫어하는 장르 제거
    for num in range(len(movies_list)): # 전체 데이터 중 
        if movies_list[num]['model'] == 'movies.movie': # 영화에 해당하는 데이터에서
            data = movies_list[num]['fields'] # 각 필드에서
            for j in range(len(data['genre_check'])): # 장르 리스트를 확인하고
                for k in range(len(gerne_list)): # 장르의 id를 name으로 변경
                    if data['genre_check'][j] == gerne_list[k].get('id'):
                        if not hate_list:
                            # 싫어하는 장르가 있는 경우
                            # 싫어하는 장르는 id를 name으로 바꾸지 않아 데이터에 포함되지 않게 함
                            for p in range(len(genre_lst)):
                                if data['genre_check'][j] == genre_lst[p]:
                                    data['genre_check'][j] == -1
                            else:
                                data['genre_check'][j] = gerne_list[k].get('name')
                        else:
                            data['genre_check'][j] = gerne_list[k].get('name')



    # 2. 데이터 프레임 형태로 변환 : 1739개
    data = movies_list[0]['fields']
    movie_df= pd.DataFrame([data])
    for num in range(1, len(movies_list)):
        if movies_list[num]['model'] == 'movies.movie':
            movie_df_plus= pd.DataFrame([movies_list[num]['fields']])
            movie_df = pd.concat([movie_df, movie_df_plus])
    

    # 가중 평균(wr) : 많은 사람들이 좋은 평점을 준 영화를 찾기 위해 선택(m보다 v가 높아야 의미있는 데이터)
    # wr = (v/(v+m))*R + (m/(v+m))*C
    # v : 개별 영화의 투표 수, m : 평점을 부여하기 위한(순위안에 들어야 하는) 최소 투표 횟수(정하기 나름)
    # R : 개별 영화에 대한 평점, C : 전체 영화에 대한 평균 평점

    # 3. 평점을 부여하기 위한 최소 투표 횟수(m) 구하기
    m = movie_df['vote_count'].quantile(0.01) # 상위 n%에 들기 위해서는 최소 m을 넘어야 하며
    movie_df = movie_df.loc[movie_df['vote_count'] >= m]
    

    # 4. 전체 영화에 대한 평균 평점(C) 구하기
    C = movie_df['vote_average'].mean() # C : 6.632317423806786
    

    # 5. 최종 추천 점수를 계산할 함수
    def weighted_rating(x, m = m, C = C):
        v = x['vote_count'] # 평점 투표 수
        R = x['vote_average'] # 평점
        return ((v/(v+m))*R)+((m/(m+v))*C) # 반환값 : wr(가중 평균)


    # 6. 최종 추천 점수를 movie_df에 score라는 컬럼(axis=1)으로 추가
    movie_df['score'] = movie_df.apply(weighted_rating, axis=1)

    # 7. 최종 데이터 수 확인
    # print(movie_df.shape)

    # 8. 데이터 전처리 : 공백 문자로 word 단위가 구분되는 문자열로 변환
    movie_df['genre_check'] = movie_df['genre_check'].apply(lambda x: " ".join(x))

    
    # 9. 전처리한 데이터를 TF-IDF 방법을 이용해 벡터화
    tfidf_vector = TfidfVectorizer(ngram_range=(1,2))
    tfidf_matrix = tfidf_vector.fit_transform(movie_df['genre_check']).toarray()

    # 10. tf-idf vector를 코사인 유사도를 활용해서 유사도 값을 구함
    cosine_sim = cosine_similarity(tfidf_matrix)
    # 코사인 유사도를 구한 matrix
    cosine_sim_df = pd.DataFrame(cosine_sim, index = movie_df.title, columns = movie_df.title)
    

    # 11. 특정 영화(사용자가 좋아요/평점을 높게 준 영화)와 유사한 영화를 추천해주는 함수
    # 추천 결과를 조회할 영화 제목, 코사인 유사도를 구한 matrix, 영화 데이터
    
    def genre_recommendations(target_title, matrix, items, k=10):
        # 특정 영화의 정보를 추출하여 유사한 코사인 유사도를 가진 정보를 추출
        # 코사인 유사도 중 영화 제목 인덱스에 해당하는 값에서 추천 개수만큼 추출
        recom_idx = matrix.loc[:, target_title].values.reshape(1, -1).argsort()[:, ::-1].flatten()[1:k+1]
        recom_title = items.iloc[recom_idx, :].title.values
        recom_genre = items.iloc[recom_idx, :].genre_check.values
        overview = items.iloc[recom_idx, :].overview.values
        poster_path = items.iloc[recom_idx, :].poster_path.values
        popularity = items.iloc[recom_idx, :].popularity.values
        release_date = items.iloc[recom_idx, :].release_date.values
        score = items.iloc[recom_idx, :].score.values

        result = {
            'title' : recom_title,
            'genre' : recom_genre,
            'overview' : overview,
            'poster_path' : poster_path,
            'popularity' : popularity,
            'release_date' : release_date,
            'score' : score
        }
        return pd.DataFrame(result)

    # =================================== #
    # 사용자가 좋아요한 영화 중, 랜덤으로 1개 선택 #  
    Users = get_object_or_404(User, pk=user_pk)
    serializer = UserMovieListSerializer(Users)
    like_lst = serializer.data.get('like_movies') # 리스트
    if like_lst: # 좋아요한 영화가 있는 경우
        random_list = []
        for i in range(len(like_lst)):
            random_list.append(like_lst[i].get('title'))
        pick_movie = random.choice(random_list)
    else: # 좋아요한 영화가 없는 경우
        pick_movie = Movie.objects.values('title').order_by('?').first().get('title')
    # =================================== #

    reco = genre_recommendations(pick_movie, cosine_sim_df, movie_df)

    result = []
    for l in range(10):
        result.append(
            {
                'title' : reco.iloc[l]['title'],
                'genre' : reco.iloc[l]['genre'],
                'release_date' : reco.iloc[l]['release_date'],
                'poster_path' : reco.iloc[l]['poster_path'],
                'overview' : reco.iloc[l]['overview'],
                'score' : reco.iloc[l]['score'],
            }
        )
    # safe : 전송데이터가 딕셔너리가 아니거나, 
    # 딕셔너리 이외의 객체를 직렬화하려면 False로 설정해야함(기본값 : True)
    return JsonResponse(result, safe=False)



# 사용자가 평점을 준 영화리스트에서 가장 높은 평점을 받은 영화와 유사한 영화를 추천
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def user_reco_rate(request, user_pk):

    movies_json = open('./movies/fixtures/movie_data.json', encoding='UTF8')
    movies_list = json.load(movies_json)
    
    gerne_json = open('./movies/genres.json', encoding='UTF8')
    gerne_list = json.load(gerne_json)

    # 사용자가 싫어하는 장르 id 선택
    Users = get_object_or_404(User, pk=user_pk)
    serializer = HateGerneSerializer(Users)
    genre_lst = serializer.data.get('hate_genres')
    hate_list = []
    if not hate_list:
        for i in range(len(genre_lst)):
            hate_list.append(genre_lst[i]['id'])

    # 싫어하는 장르 제거
    for num in range(len(movies_list)): # 전체 데이터 중 
        if movies_list[num]['model'] == 'movies.movie': # 영화에 해당하는 데이터에서
            data = movies_list[num]['fields'] # 각 필드에서
            for j in range(len(data['genre_check'])): # 장르 리스트를 확인하고
                for k in range(len(gerne_list)): # 장르의 id를 name으로 변경
                    if data['genre_check'][j] == gerne_list[k].get('id'):
                        if not hate_list:
                            # 싫어하는 장르가 있는 경우
                            # 싫어하는 장르는 id를 name으로 바꾸지 않아 데이터에 포함되지 않게 함
                            for p in range(len(genre_lst)):
                                if data['genre_check'][j] == genre_lst[p]:
                                    data['genre_check'][j] == -1
                            else:
                                data['genre_check'][j] = gerne_list[k].get('name')
                        else:
                            data['genre_check'][j] = gerne_list[k].get('name')


    data = movies_list[0]['fields']
    movie_df= pd.DataFrame([data])
    for num in range(1, len(movies_list)):
        if movies_list[num]['model'] == 'movies.movie':
            movie_df_plus= pd.DataFrame([movies_list[num]['fields']])
            movie_df = pd.concat([movie_df, movie_df_plus])
    

    m = movie_df['vote_count'].quantile(0.01) 
    movie_df = movie_df.loc[movie_df['vote_count'] >= m]

    C = movie_df['vote_average'].mean() 

    def weighted_rating(x, m = m, C = C):
        v = x['vote_count'] # 평점 투표 수
        R = x['vote_average'] # 평점
        return ((v/(v+m))*R)+((m/(m+v))*C) # 반환값 : wr(가중 평균)

    movie_df['score'] = movie_df.apply(weighted_rating, axis=1)

    movie_df['genre_check'] = movie_df['genre_check'].apply(lambda x: " ".join(x))

    tfidf_vector = TfidfVectorizer(ngram_range=(1,2))
    tfidf_matrix = tfidf_vector.fit_transform(movie_df['genre_check']).toarray()

    cosine_sim = cosine_similarity(tfidf_matrix)
    cosine_sim_df = pd.DataFrame(cosine_sim, index = movie_df.title, columns = movie_df.title)
    
    def genre_recommendations(target_title, matrix, items, k=10):
        recom_idx = matrix.loc[:, target_title].values.reshape(1, -1).argsort()[:, ::-1].flatten()[1:k+1]
        recom_title = items.iloc[recom_idx, :].title.values
        recom_genre = items.iloc[recom_idx, :].genre_check.values
        overview = items.iloc[recom_idx, :].overview.values
        poster_path = items.iloc[recom_idx, :].poster_path.values
        popularity = items.iloc[recom_idx, :].popularity.values
        release_date = items.iloc[recom_idx, :].release_date.values
        score = items.iloc[recom_idx, :].score.values

        result = {
            'title' : recom_title,
            'genre' : recom_genre,
            'overview' : overview,
            'poster_path' : poster_path,
            'popularity' : popularity,
            'release_date' : release_date,
            'score' : score
        }
        return pd.DataFrame(result)

    # =================================== #
    # 사용자가 평점을 준 영화리스트에서 가장 높은 평덤을 받은 영화와 유사한 영화 추천 #  
    Users = get_object_or_404(User, pk=user_pk)
    serializer = UserRateSerializer(Users)
    rate_lst = serializer.data.get('user_rated')
    if rate_lst: # 평점을 준 영화가 있는 경우
        max_num = 0
        for i in range(len(rate_lst)):
            if rate_lst[i].get('rate_score') >= max_num:
                pick_movie_id =  rate_lst[i].get('rate_movie')
        
        # 영화 id를
        pick_movie_dump = Movie.objects.get(pk=pick_movie_id)
        # dictionary 형태로 변환하여 title을 출력
        pick_movie = pick_movie_dump.__dict__.get('title')

    else: # 평점을 준 영화가 없는 경우, 랜덤 출력
        pick_movie = Movie.objects.values('title').order_by('?').first().get('title')
    # =================================== #

    reco = genre_recommendations(pick_movie, cosine_sim_df, movie_df)

    result = []
    for l in range(10):
        result.append(
            {
                'title' : reco.iloc[l]['title'],
                'genre' : reco.iloc[l]['genre'],
                'release_date' : reco.iloc[l]['release_date'],
                'poster_path' : reco.iloc[l]['poster_path'],
                'overview' : reco.iloc[l]['overview'],
                'score' : reco.iloc[l]['score'],
            }
        )
    # safe : 전송데이터가 딕셔너리가 아니거나, 
    # 딕셔너리 이외의 객체를 직렬화하려면 False로 설정해야함(기본값 : True)
    return JsonResponse(result, safe=False)


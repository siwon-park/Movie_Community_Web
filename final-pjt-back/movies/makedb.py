from asyncio.windows_events import NULL
from contextlib import nullcontext
import requests
import json

TMDB_API_KEY = '17f2fe0cf143650c6716a3c8a00934ac'

def get_movie_datas():
    # 최종 dump 데이터
    total_data = []

    # 장르 데이터
    request_url_gerne = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=ko-KR"
    # 요청한 데이터를 json형태로 변환하여 변수 genres에 저장
    # genres는 딕셔너리 형태의 데이터임
    genres = requests.get(request_url_gerne).json()
    for genre in genres['genres']:
        
        fields = {
            'name': genre['name'],
        }

        data = {
            "model": "movies.genre",
            "pk": genre['id'],
            "fields": fields
        }

        total_data.append(data)

    # 상영 예정 영화 데이터 : 1페이지부터 500페이지까지 (페이지당 20개, 총 10,000개)
    for i in range(1, 500):
        # url 생성
        request_url_up = f"https://api.themoviedb.org/3/movie/upcoming?api_key={TMDB_API_KEY}&language=ko-KR&page={i}"
        # 요청한 데이터를 json형태로 변환하여 변수 movies에 저장
        # movies는 딕셔너리 형태의 데이터임
        movies_up = requests.get(request_url_up).json()
        # 영화 리스트 데이터는 현재 results가 key인 value에 리스트 형태로 저장되어 있음
        for movie_up in movies_up['results']:
            # posterpath와 overview가 없는 값은 가져오지 않음
            if movie_up.get('overview') != '' and movie_up.get('poster_path') != None and movie_up.get('release_date') != None:
            # if movie_up.get('release_date', ''):
                fields = {
                    'title': movie_up['title'],
                    'release_date': movie_up['release_date'],
                    'popularity': movie_up['popularity'],
                    'overview': movie_up['overview'],
                    'vote_average': movie_up['vote_average'],
                    'vote_count' : movie_up['vote_count'],
                    'poster_path': movie_up['poster_path'],
                    'video_url': [],
                    'register_manager' : 1,
                    'genre_check': movie_up['genre_ids'],
                    'like_movie_users' : [],
                    'wish_lists_users' : []
                }

                data = {
                    "model": "movies.movie",
                    "pk": movie_up['id'],
                    "fields": fields
                }

                total_data.append(data)
    

    # 인기 영화 데이터 : 1페이지부터 500페이지까지 (페이지당 20개, 총 10,000개)
    for i in range(1, 500):
        # url 생성
        request_url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=ko-KR&page={i}"
        # 요청한 데이터를 json형태로 변환하여 변수 movies에 저장
        # movies는 딕셔너리 형태의 데이터임
        movies = requests.get(request_url).json()
        # 영화 리스트 데이터는 현재 results가 key인 value에 리스트 형태로 저장되어 있음
        for movie in movies['results']:
            # posterpath와 overview, release_date가 없는 값은 가져오지 않음
            if movie.get('release_date', '') and (movie.get('overview') != '' and movie.get('poster_path') != None and movie.get('release_date') != None):
                fields = {
                    'title': movie['title'],
                    'release_date': movie['release_date'],
                    'popularity': movie['popularity'],
                    'overview': movie['overview'],
                    'vote_average': movie['vote_average'],
                    'vote_count' : movie['vote_count'],
                    'poster_path': movie['poster_path'],
                    'video_url': [],
                    'register_manager' : 1,
                    'genre_check': movie['genre_ids'],
                    'like_movie_users' : [],
                    'wish_lists_users' : []
                }

                data = {
                    "model": "movies.movie",
                    "pk": movie['id'],
                    "fields": fields
                }

                total_data.append(data)
                
    
    # json 파일 생성
    with open("movie_data.json", "w", encoding="utf-8") as w:
        json.dump(total_data, w, indent=2, ensure_ascii=False)

get_movie_datas()
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import MovieSerializer, MovieDetailSerializer, ActorSerializer, GenreSerializer
from .models import Movie, MovieLike, Actor, ActorLike, Genre
from django.http.response import JsonResponse

from django.conf import settings
import requests
from datetime import datetime

import time
time.sleep(0.2)  # 200ms 지연

import random

MOVIE_API_KEY = settings.MOVIE_API_KEY
WEATHER_API_KEY = settings.WEATHER_API_KEY

# 전체 영화 조회
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def movie_list(request):
    url = 'https://api.themoviedb.org/3/movie/popular'
    params = {
        'api_key': MOVIE_API_KEY,
    }
    response = requests.get(url, params=params)
    movies_data = response.json()
    return Response(movies_data)

# 상세 영화 조회
@api_view(['GET'])
def movie_detail(request, movie_pk):
    url = f'https://api.themoviedb.org/3/movie/{movie_pk}'
    params= {
        'api_key': MOVIE_API_KEY,
    }
    response = requests.get(url, params=params)
    movie_detail = response.json()
    serializer = MovieDetailSerializer(movie_detail)
    return Response(serializer.data)

@api_view(['GET'])
def filter_genre(request, genre_id):
    genre_id = request.query_params.get('genre_id')  # GET 요청에서 파라미터 가져오기
    if genre_id and genre_id != 'all':
        movies = Movie.objects.filter(genres__id=genre_id)
    else:
        movies = Movie.objects.all()
    
    # 데이터를 리스트 형태로 변환
    movies_list = movies.values('id', 'title', 'overview', 'release_date')
    return Response({'movies': list(movies_list)})

@api_view(['GET'])
def recommend_weather(request, city_name):
    from rest_framework.response import Response
    from django.conf import settings
    import random

    # 1. OpenWeatherMap API 호출
    weather_url = 'https://api.openweathermap.org/data/2.5/weather'
    weather_params = {
        'q': city_name,
        'appid': settings.WEATHER_API_KEY,
        'units': 'metric',
    }
    weather_response = requests.get(weather_url, params=weather_params)
    if weather_response.status_code != 200:
        return Response({"error": "Failed to fetch weather data."}, status=weather_response.status_code)

    weather_data = weather_response.json()
    weather_state = weather_data['weather'][0]['main']
    temperature = weather_data['main']['temp']

    # 2. TMDB 장르 가져오기
    tmdb_url = "https://api.themoviedb.org/3/genre/movie/list"
    tmdb_params = {
        "api_key": settings.MOVIE_API_KEY,
        "language": "ko-KR"
    }
    tmdb_response = requests.get(tmdb_url, params=tmdb_params)
    if tmdb_response.status_code != 200:
        return Response({"error": "Failed to fetch genres from TMDB."}, status=tmdb_response.status_code)

    tmdb_genres = tmdb_response.json().get("genres", [])

    # 3. 날씨와 매핑된 장르 및 키워드
    weather_mapping = {
        'Clear': {
            'activity': ['Comedy', 'Romance', 'Adventure'],
            'keywords': ['sun', 'bright', 'clear']
        },
        'Rain': {
            'activity': ['Drama', 'Romance'],
            'keywords': ['rain', 'storm', 'wet']
        },
        'Snow': {
            'activity': ['Family', 'Fantasy'],
            'keywords': ['snow', 'cold', 'winter']
        },
        'Thunderstorm': {
            'activity': ['Thriller', 'Horror', 'Crime'],
            'keywords': ['thunder', 'lightning', 'storm']
        },
        'Drizzle': {
            'activity': ['Drama', 'Romance'],
            'keywords': ['drizzle', 'rain']
        },
        'Clouds': {
            'activity': ['Drama', 'Comedy', 'Action'],
            'keywords': ['cloud', 'overcast', 'gray']
        }
    }

    weather_category = weather_mapping.get(weather_state, {
        'activity': ['Drama'],
        'keywords': []
    })

    # TMDB 장르와 매핑
    filtered_genres = [
        genre for genre in tmdb_genres if genre['name'] in weather_category['activity']
    ]
    genre_ids = [genre['id'] for genre in filtered_genres]

    # TMDB API로 영화 검색
    discover_url = "https://api.themoviedb.org/3/discover/movie"
    discover_params = {
        "api_key": settings.MOVIE_API_KEY,
        "language": "ko-KR",
        "sort_by": "popularity.desc",
        "with_genres": ",".join(map(str, genre_ids)),
        "page": 5,
        "region": "KR",
        "include_adult": "false",
    }
    discover_response = requests.get(discover_url, params=discover_params)
    if discover_response.status_code != 200:
        return Response({"error": "Failed to fetch movies from TMDB."}, status=discover_response.status_code)

    movies = discover_response.json().get("results", [])

    # 랜덤으로 영화 선택
    random_movies = random.sample(movies, min(len(movies), 5)) if movies else []

    # TMDB 영화 상세 정보 및 감독/배우 정보 추가
    detailed_movies = []
    for movie in random_movies:
        movie_details_url = f"https://api.themoviedb.org/3/movie/{movie['id']}"
        movie_details_params = {
            "api_key": settings.MOVIE_API_KEY,
            "language": "ko-KR"
        }
        details_response = requests.get(movie_details_url, params=movie_details_params)
        if details_response.status_code == 200:
            details = details_response.json()

            # 배우 및 감독 정보 가져오기
            credits_url = f"https://api.themoviedb.org/3/movie/{movie['id']}/credits"
            credits_response = requests.get(credits_url, params=movie_details_params)
            actors = []
            director = "Unknown"
            if credits_response.status_code == 200:
                credits = credits_response.json()
                # 상위 5명 배우 추가
                actors = [cast['name'] for cast in credits.get('cast', [])[:5]]
                # 감독 필터링
                directors = [crew['name'] for crew in credits.get('crew', []) if crew['job'] == "Director"]
                if directors:
                    director = directors[0]

            detailed_movies.append({
                "id": movie.get("id"),  # id 추가
                "title": details.get("title"),
                "overview": details.get("overview"),
                "release_date": details.get("release_date"),
                "runtime": details.get("runtime", 0),
                "poster_url": f"https://image.tmdb.org/t/p/w500{details.get('poster_path')}" if details.get("poster_path") else None,
                "tagline": details.get("tagline", ""),
                "director": director,
                "vote_average": details.get("vote_average", 0.0),
                "genres": [genre['name'] for genre in details.get("genres", [])],
                "actors": actors
            })

    # 결과 반환
    return Response({
        "city": city_name,
        "temperature": f"{temperature}°C",
        "weather": weather_state,
        "recommended_movies": detailed_movies
    })


# 과거 연도의 오늘 개봉한 영화 추천
def past_release_today(request):
    """
    Fetch up to 1000 movies released on today's month and day using TMDb API
    and filter them by today's month and day, then sort by release year in descending order.
    """
    api_key = settings.MOVIE_API_KEY
    base_url = "https://api.themoviedb.org/3/discover/movie"
    today = datetime.now()

    # 오늘의 월과 일
    # 오늘의 월과 일
    month = today.month
    day = today.day

    # 수집한 영화 데이터를 저장할 리스트
    filtered_movies = []

    # 최대 50페이지까지 순회 (1000개 데이터)
    for page in range(1, 51):  # 1페이지부터 50페이지까지
        params = {
            "api_key": api_key,
            "primary_release_date.gte": f"2000-{month:02d}-{day:02d}",
            "primary_release_date.lte": f"2023-{month:02d}-{day:02d}",
            "region": "KR",  # 대한민국에서 개봉
            "sort_by": "popularity.desc",  # 인기순 정렬
            "page": page,
        }

        response = requests.get(base_url, params=params)

        if response.status_code != 200:
            print(f"Error fetching page {page}: {response.text}")
            break

        data = response.json()

        # 결과에서 월/일 필터링
        for movie in data.get("results", []):
            release_date = movie.get("release_date", None)
            if release_date:
                try:
                    release_date_obj = datetime.strptime(release_date, "%Y-%m-%d")
                    # 월과 일이 오늘과 일치하면 필터링
                    if release_date_obj.month == month and release_date_obj.day == day:
                        # 추가적인 필터링: 개봉 연도도 확인
                        if release_date_obj.year != today.year:  # 과거 연도만 필터링
                            filtered_movies.append(movie)
                        filtered_movies.append(movie)
                except ValueError as e:
                    print(f"Error parsing release_date: {release_date}, error: {e}")

        # 마지막 페이지에 도달하면 중단
        if page >= data.get("total_pages", 1):
            break

        # 1000개 초과 시 중단
        if len(filtered_movies) >= 1000:
            break

    # 1000개 초과 데이터 제거
    filtered_movies = filtered_movies[:1000]

    # 개봉 연도 기준 최신 순으로 정렬
    filtered_movies = sorted(
        filtered_movies,
        key=lambda x: datetime.strptime(x["release_date"], "%Y-%m-%d"),
        reverse=True
    )

    # 결과 반환
    if not filtered_movies:
        return JsonResponse({"movies": [], "message": "No movies found for today's date in history."})

    return JsonResponse({"movies": filtered_movies}, safe=False)

def recommend_random(request):
    """
    Recommend a random movie from movies in the database
    released in South Korea with a rating of 6 or above,
    and original_language in [en, ko, ja, fr].
    """

    # 필터링 조건에 맞는 영화들 조회
    valid_movies = Movie.objects.filter(
        vote_average__gte=6,  # 평점 6 이상
    )

    # 데이터가 없을 경우 처리
    if not valid_movies:
        return JsonResponse({"error": "No valid movies found."}, status=404)

    # 랜덤으로 하나의 영화 추천
    random_movie = random.choice(valid_movies)

    # 영화 정보를 JSON 형태로 반환
    return JsonResponse({
        "recommended_movie": {
            "id": random_movie.id,
            "title": random_movie.title,
            "overview": random_movie.overview,
            "release_date": random_movie.release_date,
            "vote_average": random_movie.vote_average,
            "poster_path": random_movie.poster_url,
        }
    })


# 좋아요 상태 조회 및 토글 API
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 로그인한 사용자만 가능
def toggle_like(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    user = request.user

    # 이미 좋아요를 눌렀는지 확인
    movie_like, created = MovieLike.objects.get_or_create(user=user, movie=movie)

    if not created:
        # 이미 좋아요한 경우 -> 좋아요 취소
        movie_like.delete()
        return Response({"liked": False, "message": "You have unliked this movie."}, status=status.HTTP_200_OK)

    # 좋아요 추가
    return Response({"liked": True, "message": "You have liked this movie."}, status=status.HTTP_200_OK)

# 배우 좋아요 추가 및 삭제
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 로그인한 사용자만 가능
def toggle_like_actor(request, actor_id):
    actor = get_object_or_404(Actor, id=actor_id)  # 배우가 존재하지 않으면 404 반환
    user = request.user

    # 이미 좋아요를 눌렀는지 확인
    actor_like, created = ActorLike.objects.get_or_create(user=user, actor=actor)

    if not created:
        # 이미 좋아요한 경우 -> 좋아요 취소
        actor_like.delete()
        return Response({"liked": False, "message": "You have unliked this actor."}, status=status.HTTP_200_OK)

    # 좋아요 추가
    return Response({"liked": True, "message": "You have liked this actor."}, status=status.HTTP_200_OK)

# 사용자가 좋아요한 영화 목록 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_likes_movie(request):
    user = request.user
    # 사용자가 좋아요한 영화들을 조회 (MovieLike 테이블을 기준으로)
    liked_movies = Movie.objects.filter(movielike__user=user)  # MovieLike를 통해 역참조
    serializer = MovieSerializer(liked_movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 사용자가 좋아요한 배우 목록 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_likes_actor(request):
    user = request.user
    # 사용자가 좋아요한 영화들을 조회 (MovieLike 테이블을 기준으로)
    liked_actors = Actor.objects.filter(actorlike__user=user)
    serializer = ActorSerializer(liked_actors, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 전체 영화 조회
@api_view(['GET'])
def get_genres(request):
    genres = Genre.objects.all()  # Genre 모델에서 모든 장르 가져오기
    serializer = GenreSerializer(genres, many=True)  # 여러 개의 장르를 직렬화
    return Response(serializer.data, status=status.HTTP_200_OK)
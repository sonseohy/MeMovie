import requests
import json

# TMDb API 키 (본인의 키로 변경)
API_KEY = '2609846e505cbcda5f26610c3bad45dd'
BASE_URL = 'https://api.themoviedb.org/3'

# 인기 영화 목록 가져오기
def get_popular_movies():
    all_movies = []
    page = 1
    while len(all_movies) < 100:  # 100개가 될 때까지 계속해서 요청
        url = f'{BASE_URL}/movie/popular?api_key={API_KEY}&page={page}'
        response = requests.get(url)
        results = response.json().get('results', [])
        all_movies.extend(results)
        page += 1
        if len(results) == 0:
            break  # 더 이상 데이터가 없으면 종료
    return all_movies[:100]  # 100개로 자르기

# discover/movie API에서 영화 목록 가져오기
def get_discover_movies():
    all_movies = []
    page = 1
    while len(all_movies) < 1000:  # 1000개가 될 때까지 계속해서 요청
        url = f'{BASE_URL}/discover/movie?api_key={API_KEY}&page={page}&sort_by=popularity.desc'
        response = requests.get(url)
        
        # 응답 상태 확인
        if response.status_code != 200:
            print(f"Error fetching page {page}: {response.text}")
            break
        
        results = response.json().get('results', [])
        all_movies.extend(results)
        page += 1

        # 더 이상 결과가 없으면 종료
        if len(results) == 0:
            break

    return all_movies[:1000]  # 1000개로 자르기


# 장르 목록 가져오기
def get_genres():
    url = f'{BASE_URL}/genre/movie/list?api_key={API_KEY}'
    response = requests.get(url)
    return response.json()['genres']

# 배우 정보 가져오기
def get_actors(movie_id):
    url = f'{BASE_URL}/movie/{movie_id}/credits?api_key={API_KEY}'
    response = requests.get(url)
    return response.json()['cast']

# 감독 정보 가져오기
def get_director(movie_id):
    url = f'{BASE_URL}/movie/{movie_id}/credits?api_key={API_KEY}'
    response = requests.get(url)
    crew = response.json()['crew']
    director = next((member['name'] for member in crew if member['job'] == 'Director'), '')
    return director

# 영화 런타임 가져오기
def get_runtime(movie_id):
    url = f'{BASE_URL}/movie/{movie_id}?api_key={API_KEY}'
    response = requests.get(url)
    return response.json().get('runtime', 0)

# 영화 장르 가져오기 (세부 영화 정보를 통해)
def get_movie_genres(movie_id):
    url = f'{BASE_URL}/movie/{movie_id}?api_key={API_KEY}'
    response = requests.get(url)
    return response.json().get('genres', [])

# 데이터를 Django 모델에 맞는 형식으로 변환하고 JSON 파일로 저장
def create_fixtures(movies, genres):
    genre_map = {genre['name']: genre['id'] for genre in genres}

    genre_fixtures = []
    actor_fixtures = []
    movie_fixtures = []

    # 장르 데이터 삽입
    for genre in genres:
        genre_fixtures.append({
            "model": "movies.genre",
            "pk": genre['id'],
            "fields": {
                "genre_name": genre['name']
            }
        })

    # 영화 데이터 삽입
    for movie in movies:
        movie_id = movie['id']
        actors = get_actors(movie_id)  # 영화 ID를 사용해 배우 정보 가져오기
        director = get_director(movie_id)  # 감독 정보 가져오기
        runtime = get_runtime(movie_id)  # 영화 런타임 정보 가져오기
        genres_list = get_movie_genres(movie_id)  # 세부 정보에서 장르 가져오기

        # 장르 정보가 비어 있지 않은 경우에만 genre_map을 사용하여 ID 가져오기
        genre_ids = [genre['id'] for genre in genres_list if genre['name'] in genre_map]

        # 배우 데이터 삽입
        for actor in actors:
            actor_fixtures.append({
                "model": "movies.actor",
                "pk": actor['id'],
                "fields": {
                    "actor_name": actor['name'],
                    "actor_profile_img": f"https://www.themoviedb.org/t/p/w500{actor['profile_path']}" if actor['profile_path'] else ''
                }
            })

        # 영화 데이터 삽입
        movie_fixtures.append({
            "model": "movies.movie",
            "pk": movie['id'],
            "fields": {
                "title": movie['title'],
                "overview": movie['overview'],
                "release_date": movie['release_date'],
                "runtime": runtime,
                "poster_url": f"https://www.themoviedb.org/t/p/w500{movie['poster_path']}" if movie['poster_path'] else '',
                "tagline": movie.get('tagline', ''),
                "director": director,
                "vote_average": movie['vote_average'],
                "genres": genre_ids,
                "actors": [actor['id'] for actor in actors]
            }
        })

    # 모델별로 각 파일에 저장
    with open('genres_fixtures.json', 'w') as genre_file:
        json.dump(genre_fixtures, genre_file, indent=4)
    
    with open('actors_fixtures.json', 'w') as actor_file:
        json.dump(actor_fixtures, actor_file, indent=4)

    with open('movies_fixtures.json', 'w') as movie_file:
        json.dump(movie_fixtures, movie_file, indent=4)

# TMDb에서 데이터 가져오기
popular_movies = get_popular_movies()  # 인기 영화 100개 가져오기
discover_movies = get_discover_movies()  # discover/movie API에서 영화 100개 가져오기
genres = get_genres()

# 두 데이터를 합쳐서 fixtures 파일 생성
all_movies = popular_movies + discover_movies
create_fixtures(all_movies, genres)

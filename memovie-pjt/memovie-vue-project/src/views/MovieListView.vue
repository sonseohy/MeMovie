<template>
  <div class="movie-page">
    <div class="movie-container">
      <div>
        <h3>{{ accountStore.currentUser }}님이 좋아하는 배우 {{ likeActor }}의 영화를 추천해드립니다.</h3>
        <swiper
          :modules="[Navigation, Pagination, Autoplay]"
          :slides-per-view="5"
          :space-between="10"
          :autoplay="{ delay: 3000, disableOnInteraction: false }"
          navigation
          :pagination="{ clickable: true }"
          loop
        >
          <swiper-slide
            v-for="movie in recommendedMovies"
            :key="movie.id"
            class="movie-slide"
          >
            <div class="movie-card" @click="showMovieDetails(movie.id)">
              <img
                :src="`https://image.tmdb.org/t/p/w500/${movie.poster_path}`"
                :alt="movie.title"
                class="movie-poster"
              />
              <div class="movie-info">
                <p class="movie-title">{{ movie.title || movie.original_title }}</p>
                <p class="movie-release-date">개봉일 {{ movie.release_date }}</p>
                <button
                  class="like-button"
                  :class="{ liked: movieStore.likedMovies.includes(movie.id) }"
                  @click="toggleLike(movie)"
                >
                  <span v-if="movieStore.likedMovies.includes(movie.id)">
                    <i class="fa-solid fa-heart" style="color: #2aa971;"></i>
                  </span>
                  <span v-else>
                    <i class="fa-regular fa-heart"></i>
                  </span>
                </button>
              </div>
            </div>
          </swiper-slide>
        </swiper>
      </div>
      <!-- 인기 영화 -->
      <div v-if="popularMovies.length" class="movie-section">
        <h3>Popular Movies : 인기 영화</h3>
        <swiper
          :modules="[Navigation, Pagination, Autoplay]"
          :slides-per-view="5"
          :space-between="10"
          :autoplay="{ delay: 3000, disableOnInteraction: false }"
          navigation
          :pagination="{ clickable: true }"
          loop
        >
          <swiper-slide
            v-for="movie in popularMovies.slice(0, 10)"
            :key="movie.id"
            class="movie-slide"
          >
            <div class="movie-card" @click="showMovieDetails(movie.id, $event)">
              <img
                :src="`https://image.tmdb.org/t/p/w500/${movie.poster_path}`"
                :alt="movie.title"
                class="movie-poster"
              />
              <div class="movie-info">
                <p class="movie-title">{{ movie.title || movie.original_title }}</p>
                <p class="movie-release-date">개봉일 {{ movie.release_date }}</p>
                <button
                  class="like-button"
                  :class="{ liked: movieStore.likedMovies.includes(movie.id) }"
                  @click="toggleLike(movie, $event)"
                >
                  <span v-if="movieStore.likedMovies.includes(movie.id)">
                    <i class="fa-solid fa-heart" style="color: #2aa971;"></i>
                  </span>
                  <span v-else>
                    <i class="fa-regular fa-heart"></i>
                  </span>
                </button>
              </div>
            </div>
          </swiper-slide>
        </swiper>
      </div>

      <!-- 한국 개봉 예정 영화 -->
      <div v-if="upcomingMovies.length" class="movie-section">
        <h3>Upcoming Movies in Korea : 한국 개봉 예정 영화</h3>
        <swiper
          :modules="[Navigation, Pagination, Autoplay]"
          :slides-per-view="5"
          :space-between="10"
          :autoplay="{ delay: 3000, disableOnInteraction: false }"
          navigation
          :pagination="{ clickable: true }"
          loop
        >
          <swiper-slide
            v-for="movie in upcomingMovies.slice(0, 10)"
            :key="movie.id"
            class="movie-slide"
          >
            <div class="movie-card" @click="showMovieDetails(movie.id, $event)">
              <img
                :src="`https://image.tmdb.org/t/p/w500/${movie.poster_path}`"
                :alt="movie.title"
                class="movie-poster"
              />
              <div class="movie-info">
                <p class="movie-title">{{ movie.title || movie.original_title }}</p>
                <p class="movie-release-date">개봉일 {{ movie.release_date }}</p>
                <button
                  class="like-button"
                  :class="{ liked: movieStore.likedMovies.includes(movie.id) }"
                  @click="toggleLike(movie, $event)"
                >
                  <span v-if="movieStore.likedMovies.includes(movie.id)">
                    <i class="fa-solid fa-heart" style="color: #2aa971;"></i>
                  </span>
                  <span v-else>
                    <i class="fa-regular fa-heart"></i>
                  </span>
                </button>
              </div>
            </div>
          </swiper-slide>
        </swiper>
      </div>

      <!-- 현재 상영 중인 영화 -->
      <div v-if="nowPlayingMovies.length" class="movie-section">
        <h3>Currently Showing Movies : 현재 상영 중인 영화</h3>
        <swiper
          :modules="[Navigation, Pagination, Autoplay]"
          :slides-per-view="5"
          :space-between="10"
          :autoplay="{ delay: 3000, disableOnInteraction: false }"
          navigation
          :pagination="{ clickable: true }"
          loop
        >
          <swiper-slide
            v-for="movie in nowPlayingMovies.slice(0, 10)"
            :key="movie.id"
            class="movie-slide"
          >
            <div class="movie-card" @click="showMovieDetails(movie.id, $event)">
              <img
                :src="`https://image.tmdb.org/t/p/w500/${movie.poster_path}`"
                :alt="movie.title"
                class="movie-poster"
              />
              <div class="movie-info">
                <p class="movie-title">{{ movie.title || movie.original_title }}</p>
                <p class="movie-release-date">개봉일 {{ movie.release_date }}</p>
                <button
                  class="like-button"
                  :class="{ liked: movieStore.likedMovies.includes(movie.id) }"
                  @click="toggleLike(movie, $event)"
                >
                  <span v-if="movieStore.likedMovies.includes(movie.id)">
                    <i class="fa-solid fa-heart" style="color: #2aa971;"></i>
                  </span>
                  <span v-else>
                    <i class="fa-regular fa-heart"></i>
                  </span>
                </button>
              </div>
            </div>
          </swiper-slide>
        </swiper>
      </div>

      <!-- 과거 오늘 개봉한 영화 -->
      <div v-if="pastReleaseMovies.length" class="movie-section">
        <h3>N년전 오늘 개봉한 영화</h3>
        <div class="movie-grid">
          <div v-for="movie in pastReleaseMovies.slice(0, 5)" :key="movie.id" class="movie-card" @click="showMovieDetails(movie.id, $event)">
            <div class="movie-card-content">
              <img :src="`https://image.tmdb.org/t/p/w500/${movie.poster_path}`" :alt="movie.title" />
              <div class="movie-info">
                <p class="movie-title">{{ movie.title || movie.original_title }}</p>
                <p class="movie-release-date">개봉일 {{ movie.release_date }}</p>
                <button class="like-button" :class="{ liked: movie.liked }" @click="toggleLike(movie, $event)">
                  <span v-if="movie.liked"><i class="fa-solid fa-heart" style="color: #2aa971;"></i></span>
                  <span v-else><i class="fa-regular fa-heart"></i></span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 로딩 중 애니메이션 -->
      <div v-if="isLoading" class="loading-container">
        <div class="spinner"></div>
        <p>N년전 오늘 개봉한 영화는...</p>
      </div>
      
      <!-- <div v-if="isLoading" class="loading-container">
        <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGw0MWFpdjM0djA3emVwOGFkZGhjMDRoY24xdm13b25jMDd6b3B0YyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/lJNoBCvQYp7nq/giphy.gif" alt="Loading..." class="loading-gif" />
        <p>영화를 찾고 있습니다...</p>
      </div> -->
      
      <!-- 버튼을 눌러서 과거 영화를 로드 -->
      <button v-if="!isLoading && !isPastReleaseMoviesLoaded" @click="fetchPastReleaseMovies" class="search-button">N년전 오늘 개봉한 영화 보기</button>
    </div>

      <!-- 랜덤 추천 영화 섹션 -->
      <div class="movie-section random-movie-section">
        <h3>오늘의 랜덤 추천 영화</h3>
        <div class="random-movie-card" @click="fetchRandomMovie">
          <div v-if="!randomMovie && !isLoadingRandom" class="placeholder-card">
            <p>?</p>
          </div>
          <div v-else-if="isLoadingRandom" class="loading-container">
            <div class="spinner"></div>
            <p>랜덤 추천 중...</p>
          </div>
          <div v-else class="movie-card-content">
            <img
              :src="`https://image.tmdb.org/t/p/w500/${randomMovie.poster_path}`"
              :alt="randomMovie.title"
            />
            <div class="movie-info">
              <p class="movie-title">{{ randomMovie.title || randomMovie.original_title }}</p>
              <p class="movie-release-date">개봉일 {{ randomMovie.release_date }}</p>
              <button class="like-button" :class="{ liked: randomMovie.liked }" @click="toggleLike(randomMovie, $event)">
                <span v-if="randomMovie.liked"><i class="fa-solid fa-heart" style="color: #2aa971;"></i></span>
                <span v-else><i class="fa-regular fa-heart"></i></span>
              </button>
            </div>
          </div>
        </div>
      </div>
      <!-- 도시 선택 셀렉터 -->
      <div class="weather-section">
        <h3>도시를 선택하세요</h3>
        <select v-model="selectedCity" class="city-selector">
          <option v-for="city in cities" :key="city" :value="city">
            {{ city }}
          </option>
        </select>
        <button @click="fetchWeatherMovies" class="fetch-weather-button">추천 영화 보기</button>
      </div>

      <!-- 날씨별 추천 영화 -->
      <div v-if="weatherMovies.length" class="movie-section">
        <h3>{{ weatherDescription }}</h3> <!-- 메시지 출력 -->
        <swiper
          :modules="[Navigation, Pagination, Autoplay]"
          :slides-per-view="5"
          :space-between="10"
          :autoplay="{ delay: 3000, disableOnInteraction: false }"
          navigation
          :pagination="{ clickable: true }"
          loop
        >
          <swiper-slide
            v-for="movie in weatherMovies.slice(0, 8)"
            :key="movie.id"
            class="movie-slide"
          >
            <div class="movie-card" @click="showMovieDetails(movie.id, $event)">
              <img
                :src="movie.poster_url"
                :alt="movie.title"
                class="movie-poster"
              />
              <div class="movie-info">
                <p class="movie-title">{{ movie.title }}</p>
                <p class="movie-release-date">개봉일 {{ movie.release_date }}</p>
                <p class="movie-genres">장르: {{ movie.genres.join(", ") }}</p>
                <button
                  class="like-button"
                  :class="{ liked: movieStore.likedMovies.includes(movie.id) }"
                  @click="toggleLike(movie, $event)"
                >
                  <span v-if="movieStore.likedMovies.includes(movie.id)">
                    <i class="fa-solid fa-heart" style="color: #2aa971;"></i>
                  </span>
                  <span v-else>
                    <i class="fa-regular fa-heart"></i>
                  </span>
                </button>
              </div>
            </div>
          </swiper-slide>
        </swiper>
      </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useAccountStore } from '@/stores/account';
import { useMovieStore } from '@/stores/movie';
import 'swiper/swiper-bundle.css';
import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import 'swiper/css/autoplay';

// Swiper 모듈 불러오기 //
import { Navigation, Pagination, Autoplay } from 'swiper/modules';


const apiKey = '084c3c6e5b92e9efba1b413f8aa0a03f';

const popularMovies = ref([]);
const nowPlayingMovies = ref([]);
const pastReleaseMovies = ref([]);  // 새로운 데이터 추가
const isPastReleaseMoviesLoaded = ref(false); // 과거 영화 데이터가 로드되었는지 여부를 확인하는 변수
const randomMovie = ref(null); // 랜덤 추천 영화를 저장
const isLoading = ref(false); // 로딩 상태를 관리할 변수
const isLoadingRandom = ref(false); // 랜덤 로딩 상태를 관리할 변수
const upcomingMovies = ref([]); // 한국 개봉 예정 영화

const router = useRouter();
const accountStore = useAccountStore()
const movieStore = useMovieStore()

const cities = ['Seoul', 'Busan', 'Incheon', 'Daegu', 'Daejeon', 'Gwangju', 'Ulsan', 'Suwon', 'Changwon', 'Goyang', 'Yongin', 'Cheongju', 'Jeonju', 'Cheonan', 'Sejong'];
const weatherDescription = ref(''); // 날씨와 도시 기반의 추천 메시지를 저장
const selectedCity = ref(cities[0]);
const weatherMovies = ref([]);
const isLoadingWeatherMovies = ref(false);

const likeActor = ref(null);

// 상태 변수 선언
const recommendedMovies = ref([])

// 영화 데이터를 가져오는 함수
const fetchMovies = async () => {
  try {
    // 인기 영화
    const popularResponse = await axios.get(`https://api.themoviedb.org/3/movie/popular?api_key=${apiKey}&language=ko-KR&page=1`);
    popularMovies.value = popularResponse.data.results;

    // 한국 개봉 예정 영화
    const upcomingResponse = await axios.get(`https://api.themoviedb.org/3/movie/upcoming?api_key=${apiKey}&region=KR&language=ko-KR`);
    upcomingMovies.value = upcomingResponse.data.results;

    // 현재 상영 중인 영화
    const nowPlayingResponse = await axios.get(`https://api.themoviedb.org/3/movie/now_playing?api_key=${apiKey}&language=ko-KR&page=1`);
    nowPlayingMovies.value = nowPlayingResponse.data.results;

  } catch (error) {
    console.error('Error fetching movies:', error);
  }
};

// 과거 오늘 개봉한 영화를 가져오는 함수
const fetchPastReleaseMovies = async () => {
  try {
    isLoading.value = true; // 로딩 시작
    const pastReleaseResponse = await axios.get('http://localhost:8000/api/movies/recommend/pastrelease/');
    
    // 중복 제거: id를 기준으로 Set을 사용하여 필터링
    const uniqueMovies = pastReleaseResponse.data.movies.filter((movie, index, self) =>
      index === self.findIndex((m) => m.id === movie.id)
    );

    pastReleaseMovies.value = uniqueMovies; // 중복 제거된 영화 목록 저장
    isPastReleaseMoviesLoaded.value = true; // 데이터를 로드한 후 버튼 숨기기
    isLoading.value = false; // 로딩 종료
  } catch (error) {
    console.error('Error fetching past release movies:', error);
    isLoading.value = false; // 로딩 종료
  }
};

// 랜덤 영화 데이터를 가져오는 함수
const fetchRandomMovie = async () => {
  try {
    isLoadingRandom.value = true; // 로딩 시작
    const response = await axios.get('http://localhost:8000/api/movies/recommend/random/');
    randomMovie.value = response.data.recommended_movie; // 서버에서 가져온 영화 데이터 저장
    isLoadingRandom.value = false; // 로딩 종료
  } catch (error) {
    console.error('Error fetching random movie:', error.response.data);
    isLoadingRandom.value = false; // 로딩 종료
  }
};


// 날씨별 추천 영화를 가져오는 함수
const fetchWeatherMovies = async () => {
  try {
    isLoadingWeatherMovies.value = true; // 로딩 상태 시작
    const response = await axios.get(`http://localhost:8000/api/movies/recommend/weather/${selectedCity.value}`);
    weatherMovies.value = response.data.recommended_movies; // 서버에서 가져온 추천 영화 데이터 저장

    // 날씨와 도시 기반의 멘트 설정
    weatherDescription.value = `현재 ${response.data.weather} 날씨인 ${selectedCity.value}에 추천하는 영화입니다!`;
  } catch (error) {
    console.error('Error fetching weather-based movies:', error);
  } finally {
    isLoadingWeatherMovies.value = false; // 로딩 상태 종료
  }
};


// 영화 상세 페이지로 이동
const showMovieDetails = (id, event) => {
  console.log('Navigating to MovieDetail with id:', id); // 로그 추가
  router.push({ name: 'MovieDetail', params: { id } });
};

// 좋아요 상태 초기화
const initializeLikes = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/movies/user-likes/movies/', {
      headers: { Authorization: `Token ${accountStore.token}` },
    });
    const likedMovieIds = response.data.map(movie => movie.id);
    movieStore.setLikedMovies(likedMovieIds); // Pinia store의 likedMovies 업데이트
  } catch (error) {
    console.error('Error initializing likes:', error.response?.data || error.message);
  }
};

// 좋아요 상태 토글
const toggleLike = async (movie, event) => {
  event.stopPropagation(); // 클릭 이벤트 전파 방지
  try {
    const response = await axios.post(
      `http://localhost:8000/api/movies/${movie.id}/toggle-like/`,
      {},
      {
        headers: { Authorization: `Token ${accountStore.token}` },
      }
    );

    const isLiked = response.data.liked;
    if (isLiked) {
      movieStore.addLikedMovie(movie.id);
    } else {
      movieStore.removeLikedMovie(movie.id);
    }
  } catch (error) {
    console.error('Error toggling like:', error.response?.data || error.message);
  }
};

const fetchRecommendedMovies = () => {
  // 사용자가 좋아요한 배우 목록을 가져오기
  axios.get('http://127.0.0.1:8000/api/movies/user-likes/actors/', {
    headers: {
      Authorization: `Token ${accountStore.token}`  // 헤더에 인증 토큰 추가
    }
  })
    .then(actorResponse => {
      const likedActors = actorResponse.data;

      if (likedActors.length === 0) {
        console.log("좋아요한 배우가 없습니다.");
        return;
      }

      // 좋아요한 배우 중 랜덤으로 한 명을 선택
      const randomActor = likedActors[Math.floor(Math.random() * likedActors.length)];
      likeActor.value = randomActor.actor_name
      // 선택된 배우의 출연작을 TMDB API에서 가져오기
      axios.get(`https://api.themoviedb.org/3/person/${randomActor.id}/movie_credits`, {
        params: {
          api_key: apiKey,  // TMDB API 키
        }
      })
        .then(tmdbResponse => {
          const movies = tmdbResponse.data.cast;  // 출연작 목록

          // 평점 높은 순으로 정렬 후 상위 8개만 추출
          recommendedMovies.value = movies
            .sort((a, b) => b.vote_average - a.vote_average) // 평점 기준 내림차순 정렬
            .slice(0, 8); // 상위 8개 영화만
        })
        .catch(error => {
          console.error('TMDB API에서 영화 목록을 가져오는 데 실패했습니다.', error.response.data);
        });
    })
    .catch(error => {
      console.error('배우 목록을 가져오는 데 실패했습니다.', error.response.data);
    });
};


onMounted(() => {
  fetchMovies();
  initializeLikes(); // 좋아요 상태 초기화
  fetchRecommendedMovies()
});
</script>

<style scoped>
/* SwiperSlide와 이미지 스타일링 */
.swiper-slide {
  /* width: auto; */
  display: flex;
  justify-content: center;
  align-items: center;
}

.swiper-slide img {
  width: 100%;
  height: auto;
  object-fit: cover; /* 이미지 비율 유지 */
  border-radius: 8px; /* 모서리 둥글게 */
  transition: transform 0.3s ease; /* 확대 효과 */
}

.swiper-slide:hover img {
  transform: scale(1.05); /* 마우스 오버 시 살짝 확대 */
}

.movie-page {
  padding: 100px;
}

.movie-container {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.movie-section {
  margin-bottom: 30px;
}

.movie-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  background-image: url('@/assets/film_long.png'); /* 배경 이미지 설정 */
  background-size: cover; /* 배경 이미지가 그리드 전체를 덮도록 설정 */
  background-position: center;
  padding: 50px 0; /* 위아래 마진 대신 내부 패딩을 추가 */
}

.movie-card {
  width: 100%; /* 슬라이드에 꽉 채우기 */
  height: auto; /* 높이는 자동 */
  cursor: pointer;
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  transition: transform 0.3s ease; /* 마우스 오버 시 크기 변화를 위한 설정 */
  max-width: 200px; /* 슬라이드 크기 제한 */
}

.movie-card-content {
  position: relative;
  width: 100%;
  height: 100%;
}

.movie-card img {
  width: 100%;
  height: 300px;  /* 고정된 높이 지정 */
  object-fit: cover; /* 비율을 유지하면서 채워짐 */
  border-radius: 8px;
  transition: transform 0.3s ease; /* 이미지 크기 변화 */
}

.movie-card:hover img {
  transform: scale(1.1); /* 이미지가 커지는 효과 */
}

.movie-info {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  opacity: 0;
  transition: opacity 0.3s ease;
  font-size: 16px;
  text-align: center;
}

.movie-card:hover .movie-info {
  opacity: 1;
}

.like-button {
  background-color: transparent; /* 배경색을 투명으로 설정 */
  color: white;
  font-size: 20px;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
  transition: transform 0.2s ease-in-out;
}

.like-button.liked i {
  animation: pulse 0.6s ease; /* 클릭 시 펄스 효과 */
}

/* 펄스 애니메이션 */
@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.4); /* 1.4배 커짐 */
  }
  100% {
    transform: scale(1); /* 원래 크기로 돌아옴 */
  }
}

.like-button:hover i {
  transform: scale(1.1); /* 하트 아이콘을 1.2배 키움 */
}

.movie-title {
  font-weight: bold;
}

.movie-release-date {
  font-size: 14px;
}

/* 로딩 스피너 스타일 */
.loading-container {
  display: flex;
  align-items: middle; /* 수직 중앙 정렬 */
  justify-content: center; /* 수평 중앙 정렬 */
  gap: 10px; /* 텍스트와 스피너 사이 간격 */
  font-size: 18px;
  color: black; /* 텍스트 색상 */
}

.spinner {
  border: 4px solid #218d58; /* 투명도 있는 테두리 */
  border-top: 4px solid #ffffff; /* 흰색 상단 테두리 */
  border-radius: 50%; /* 원형 */
  width: 18px; /* 크기 조정 */
  height: 18px; /* 크기 조정 */
  animation: spin 1s linear infinite; /* 회전 애니메이션 */
  margin-top: 4px; /* 살짝 아래로 이동 */
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* .loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.loading-gif {
  width: 100px;
  height: auto;
  border-radius: 10px;
} */

.search-button {
  display: flex;
  justify-content: center; /* 수평 중앙 정렬 */
  align-items: center; /* 수직 중앙 정렬 */
  width: 50%; /* 버튼 크기 */
  max-width: 400px; /* 최대 너비 */
  height: 50px; /* 버튼 높이 */
  margin: 20px auto; /* 위아래 간격 및 가운데 정렬 */
  padding: 0 20px; /* 내부 여백 */
  font-size: 16px; /* 글자 크기 */
  font-weight: bold; /* 글자 두께 */
  color: #fff; /* 글자 색상 */
  background-color: #218d58; /* 구글 블루 */
  border: none; /* 테두리 제거 */
  border-radius: 25px; /* 둥근 모서리 */
  cursor: pointer; /* 마우스 커서 변경 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 그림자 */
  transition: all 0.3s ease; /* 애니메이션 */
}

.search-button:hover {
  background-color: #1a7550; /* 살짝 어두운 블루 */
  transform: translateY(-2px); /* 살짝 위로 이동 */
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2); /* 그림자 강화 */
}

.search-button:active {
  transform: translateY(0); /* 눌릴 때 원래 위치로 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 그림자 약화 */
}

/* 랜덤 추천 영화 카드 스타일 */
.random-movie-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.random-movie-card {
  width: 200px;
  height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 16px;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.random-movie-card:hover {
  transform: scale(1.05); /* 살짝 확대 */
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
}

.placeholder-card {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 64px;
  font-weight: bold;
  color: #999;
  width: 120px;
  height: 120px;
  transition: background-color 0.3s ease;
}

.movie-card-content img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 16px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.spinner {
  border: 4px solid #ccc;
  border-top: 4px solid #218d58;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.weather-section {
  margin-bottom: 30px;
  text-align: center;
}

.city-selector {
  padding: 10px;
  font-size: 16px;
  margin-right: 10px;
}

.fetch-weather-button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #218d58;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.fetch-weather-button:hover {
  background-color: #1a7550;
}

.movie-poster {
  width: 100%; /* 카드의 가로 길이 */
  height: auto; /* 높이는 비율에 맞게 설정 */
  object-fit: cover; /* 이미지 비율 유지 */
  border-radius: 8px;
  margin-bottom: 10px;
  transition: transform 0.3s ease; /* 마우스 오버 시 효과 */
}

.swiper {
    background-image: url('@/assets/film_long.png'); /* 배경 이미지 */
    background-size: cover;
    background-position: center;
    padding: 80px;
    border-radius: 8px;
}

.swiper-slide {
    flex: 0 0 auto; /* 슬라이드가 flexbox 규칙을 따르도록 설정 */
    width: auto; /* 슬라이드 너비 자동 조정 */
    display: flex;
    justify-content: center; /* 중앙 정렬 */
    align-items: center;
    margin: 0; /* 여백 제거 */
}


/* movie-slide 스타일 추가 */
.movie-slide {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px; /* 슬라이드 높이 고정 */
  width: auto; /* 슬라이드 너비를 자동으로 설정 */
  margin: 0; /* 추가 여백 제거 */
}

.movie-slide img {
  max-height: 100%; /* 슬라이드 높이에 맞게 이미지 조정 */
  max-width: 100%; /* 이미지가 너무 넓어지지 않도록 제한 */
  object-fit: cover; /* 비율 유지 */
  border-radius: 8px; /* 모서리 둥글게 */
}

</style>

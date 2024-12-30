<template>
  <div class="container">
    <div class="movie-info">
      <!-- 왼쪽: 포스터 -->
      <div class="poster-box">
        <div class="poster">
          <img
            v-if="movie.poster_path"
            :src="`https://image.tmdb.org/t/p/w500/${movie.poster_path}`"
            alt="Movie Poster"
          />
        </div>
      </div>
      
      <!-- 오른쪽: 영화 정보 -->
      <div class="movie-details">
        <h1 class="movie-title">
          <span class="title-text">{{ movie.title }}</span>
          <span class="release-year">{{ release.year }}</span>
        </h1>

        <div class="movie-stats">
    <div class="star-rating">
      <span 
        v-for="star in 5" 
        :key="star"
        class="star"
        :class="{ active: star <= Math.round(movie.vote_average / 2) }">
        ★
      </span>
      <span><strong>평점:</strong> {{ movie.vote_average }}</span>
    </div>
  </div>


        <p class="release-day"><strong>개봉일:</strong> {{ movie.release_date }}</p>
        <p class="description">{{ movie.overview }}</p>
      </div>
    </div>
    <!-- 가로줄 -->
    <div class="divider"></div>
    
    <!-- 감독과 배우 섹션 -->
    <div class="director-cast">
      <!-- 감독 -->
      <div class="director-box">
        <h5>| 감독</h5>
        <div v-if="director">
          <img
            v-if="director.profile_path"
            :src="actorImageUrl(director.profile_path)"
            alt="Director Image"
            class="director-img"
          />
          <p>{{ director.name }}</p>
        </div>
      </div>

      <!-- 배우들 -->
      <div class="cast">
        <h5>| 배우</h5>
        <div class="cast-list">
          <div
            v-for="actor in cast.slice(0, 5)"
            :key="actor.id"
            class="cast-member"
            @mouseover="toggleHover(actor.id, true)"
            @mouseleave="toggleHover(actor.id, false)"
          >
            <div class="actor-container">
              <img
                :src="actorImageUrl(actor.profile_path)"
                :alt="actor.name"
                class="actor-img"
              />
              <!-- 좋아요 버튼 -->
              <button
                v-if="hoveredActor === actor.id || likedActors.includes(actor.id)"
                class="like-button"
                :class="{ liked: likedActors.includes(actor.id) }"
                @click="toggleLikeActor(actor.id, $event)"
              >
                <span v-if="likedActors.includes(actor.id)">
                  <i class="fa-solid fa-heart" style="color: #e63946;"></i>
                </span>
                <span v-else>
                  <i class="fa-regular fa-heart"></i>
                </span>
              </button>
            </div>
            <p @click="openActorModal(actor.id)" class="name-link">{{ actor.name }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 배우 모달 -->
    <ActorDetail
      v-if="isActorModalVisible"
      :actorId="selectedActorId"
      :isVisible="isActorModalVisible"
      @close="closeActorModal"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';  // useRoute를 사용하여 URL 파라미터를 가져옵니다.
import ActorDetail from '@/components/ActorDetail.vue'
import { useAccountStore } from '@/stores/account';
import { useMovieStore } from '@/stores/movie';

// 라우트의 params에서 영화 id를 가져옵니다
const route = useRoute();
const movieId = route.params.id;
const store = useAccountStore(); // 사용자 상태 가져오기
const movieStore = useMovieStore(); // 영화 스토어 가져오기

// 영화와 관련된 데이터 변수들
const movie = ref({});
const cast = ref([]);
const director = ref({});
const likedActors = ref([]); // 찜한 배우 ID를 저장하는 배열
const hoveredActor = ref(null); // 마우스가 올라간 배우 ID
const isActorModalVisible = ref(false);
const selectedActorId = ref(null);

const API_TOKEN = import.meta.env.VITE_TMDB_API_KEYS;

// API URL들
const movieUrl = `https://api.themoviedb.org/3/movie/${movieId}?api_key=${API_TOKEN}&language=ko`;
const creditsUrl = `https://api.themoviedb.org/3/movie/${movieId}/credits?api_key=${API_TOKEN}&language=ko`;

// 배우 이미지 URL
const actorImageUrl = (path) => `https://image.tmdb.org/t/p/w200${path}`;

// 개봉 연도 계산
const release = computed(() => {
  if (movie.value.release_date) {
    return { year: new Date(movie.value.release_date).getFullYear() };
  }
  return { year: '정보 없음' };
});

// 배우 좋아요 토글 함수
const toggleLikeActor = async (actorId, event) => {
  event.stopPropagation();  // 클릭 이벤트 전파 방지
  try {
    const response = await axios.post(
      `http://localhost:8000/api/movies/${actorId}/toggle-like/actor/`,
      {},
      {
        headers: { Authorization: `Token ${store.token}` },
      }
    );

    const isLiked = response.data.liked;

    // UI 상태를 즉시 반영
    if (isLiked) {
      if (!likedActors.value.includes(actorId)) {
        likedActors.value.push(actorId); // 좋아요 추가
      }
    } else {
      likedActors.value = likedActors.value.filter(id => id !== actorId); // 좋아요 제거
    }

    movieStore.setLikedActors(likedActors.value); // Pinia store 상태 업데이트
  } catch (error) {
    console.error('Error toggling actor like:', error.response?.data || error.message);
  }
};


// 마우스 오버 상태 업데이트
const toggleHover = (actorId, isHovered) => {
  hoveredActor.value = isHovered ? actorId : null;
};

// 영화 정보와 배우 정보 가져오는 함수
const fetchMovieDetails = async () => {
  console.log('Fetching details for movieId:', movieId);
  try {
    // 영화 세부 정보
    const movieResponse = await axios.get(movieUrl);
    movie.value = movieResponse.data;

    // 영화 출연 배우 정보
    const creditsResponse = await axios.get(creditsUrl);
    cast.value = creditsResponse.data.cast;

    // 감독 정보 추출
    const directorData = creditsResponse.data.crew.find(member => member.job === 'Director');
    if (directorData) {
      director.value = {
        name: directorData.name,
        profile_path: directorData.profile_path,
      };
    } else {
      director.value = { name: '정보 없음', profile_path: null };
    }
  } catch (error) {
    console.error('영화 정보를 불러오는 데 실패했습니다:', error);
  }
};

// 배우 프로필 클릭 시 모달 열기
const openActorModal = (actorId) => {
  selectedActorId.value = actorId;
  isActorModalVisible.value = true;
};

// 모달 닫기
const closeActorModal = () => {
  isActorModalVisible.value = false;
};

const fetchLikedActors = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/movies/user-likes/actors/', {
      headers: {
        Authorization: `Token ${store.token}`
      }
    });
    likedActors.value = response.data.map(actor => actor.id);  // 배우 ID만 추출하여 likedActors 상태 업데이트
  } catch (error) {
    console.error('배우 좋아요 목록을 불러오는 데 실패했습니다:', error);
  }
};


// 컴포넌트가 마운트되었을 때 영화 정보 가져오기
onMounted(() => {
  fetchMovieDetails();
  fetchLikedActors();
});
</script>

<style scoped>

/* 평점 표시 부분 */
.movie-stats {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.star-rating {
  display: inline-flex; /* 수평으로 정렬 */
  align-items: center;  /* 아이템을 세로로 중앙 정렬 */
  font-size: 1.2em;
}

.star {
  color: #ccc; /* 기본 별 색상 */
  margin-right: 5px;
  font-size: 1.5em;
  transition: color 0.3s ease;
}

.star.active {
  color: #f5c518; /* 활성화된 별 색상 */
}

.star:hover {
  color: #f5c518; /* 마우스 오버 시 별 색상 */
}

.star-rating span {
  margin-left: 10px; /* 평점 숫자와 별 사이 간격 */
}

h5 {
  font-weight: 500;
}
.container {
  padding-top: 100px;
}

.movie-info {
  display: flex;
  flex-direction: row;
  gap: 20px;
  padding: 20px;
}

.movie-title {
  display: flex; /* 제목과 연도를 같은 줄에 표시 */
  align-items: center; /* 텍스트 정렬 */
  gap: 10px; /* 제목과 연도 사이의 간격 */
  font-size: 2rem; /* 폰트 크기 */
}

.title-text {
  font-weight: bold; /* 제목은 굵게 */
}

.release-year {
  font-weight: bold; /* 제목은 굵게 */
  font-size: 1.5rem; /* 연도는 제목보다 약간 작게 */
  color: #555; /* 연도의 색상 */
  margin-left: 10px; /* 연도와 제목 사이의 여백 */
}


.poster-box {
  margin: 10px 10px;
  border-right: 2px solid #2aa971;
  padding-right: 30px;
}

.poster img {
  flex: 1;
  width: 300px;
  border-radius: 10px;
}

.movie-details {
  flex: 4;
  max-width: 800px;
}

.movie-title {
  display: flex;
  align-items: center;
  gap: 50px; /* 제목과 연도 사이의 여백 */
}

.release-year {
  font-size: 1.2rem;
  color: #555; /* 연도 텍스트 스타일 */
}

.release-day {
  font-size: medium;
  margin-top: 30px;
}


.divider {
  margin-top: 30px;
  margin-bottom: 10px;
  border: none;
  height: 2px;
  border-bottom: 2px solid #2aa971;
}

.director-cast {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: flex-start;
  gap: 50px;
}

.cast-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.actor-container {
  position: relative;
  display: inline-block;
  text-align: center; /* 이름 텍스트 가운데 정렬 */
}

.actor-img,
.director-img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  position: relative; /* 오버레이를 위해 위치 지정 */
  transition: 0.3s ease; /* 마우스 오버 효과 부드럽게 전환 */
}

.actor-container:hover .actor-img::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 1); /* 살짝 어두운 오버레이 */
  border-radius: 50%;
  transition: 0.3s ease; /* 부드러운 전환 */
  z-index: 1; /* 오버레이가 이미지 위에 표시되도록 설정 */
}

.actor-img + p {
  font-size: 0.9rem;
  margin-top: 5px;
  z-index: 2;
  position: relative; /* 이름 텍스트가 이미지 위로 올라오지 않도록 조정 */
}

.like-button {
  position: absolute;
  bottom: 5px;
  left: 50%;
  transform: translateX(-50%);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
  display: none;
  z-index: 2; /* 하트 아이콘이 오버레이 위에 표시되도록 설정 */
  color: #e63946;
  transition: color 0.3s ease;
}

.like-button.liked i {
  color: #e63946;
}

.actor-container:hover .like-button {
  display: block;
}

.actor-container:hover .actor-img {
  filter: brightness(0.85); /* 이미지 어둡게 */
}

.cast {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.cast-member {
  cursor: pointer;
  text-align: center;
}

.name-link {
  margin-top: 10px;
  font-family: 'Inter', sans-serif;
  font-weight: 400;
  font-size: 15px;
  line-height: 15px;
  color: #28353d;
  text-decoration: none;
  transition: color 0.3s ease;
}

.name-link:hover {
  font-weight: 600;
  color: #2AA971;
}


</style>

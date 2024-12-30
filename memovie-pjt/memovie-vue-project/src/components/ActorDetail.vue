<template>
  <div class="container">
  <div v-if="isVisible" class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <button class="close-btn" @click="closeModal">X</button>
      <div class="actor-info">
        <div class="actor-header">
          <img
            v-if="actor.profile_path"
            :src="actorImageUrl(actor.profile_path)"
            alt="Actor Profile"
            class="actor-photo"
          />
          <div class="actor-details">
            <h3>{{ actor.name }}</h3>
            <p><strong>생년월일:</strong> {{ actor.birth_date || '정보 없음' }}</p>
            <p><strong>출생지:</strong> {{ actor.place_of_birth || '정보 없음' }}</p>
          </div>
        </div>

        <div class="actor-movies">
          <h4>출연 영화</h4>
          <div class="movies-list">
            <div
              v-for="movie in filteredMovies" :key="movie.id" class="movie-item"
              @click="goToMovieDetail(movie.id)"
            >
              <!-- 포스터가 있는 경우만 포스터 표시, 없으면 전달받은 기본 포스터 사용 -->
              <img
                v-if="movie.poster_path"
                :src="actorImageUrl(movie.poster_path)"
                alt="Movie Poster"
                class="movie-poster"
              />
              <img
                v-else
                :src="defaultPoster"
                alt="No Poster"
                class="movie-poster"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const props = defineProps({
  actorId: Number,
  isVisible: Boolean,
  defaultPoster: String,  // 부모에서 전달받은 기본 포스터 URL
});

const emit = defineEmits(['close']);
const router = useRouter();

const actor = ref({});
const actorMovies = ref([]);

// 배우 이미지 URL 생성
const actorImageUrl = (path) => `https://image.tmdb.org/t/p/w200${path}`;

const fetchActorDetails = async () => {
  try {
    // 배우 상세 정보
    const actorResponse = await axios.get(`https://api.themoviedb.org/3/person/${props.actorId}?api_key=${import.meta.env.VITE_TMDB_API_KEYS}&language=ko`);
    actor.value = actorResponse.data;

    // 배우가 출연한 영화 리스트
    const movieCreditsResponse = await axios.get(`https://api.themoviedb.org/3/person/${props.actorId}/movie_credits?api_key=${import.meta.env.VITE_TMDB_API_KEYS}&language=ko`);
    actorMovies.value = movieCreditsResponse.data.cast;
  } catch (error) {
    console.error('배우 정보와 출연 영화를 불러오는 데 실패했습니다.', error);
  }
};

// 영화 인기도에 기반하여 "유명한 영화"만 필터링
const filteredMovies = computed(() => {
  return actorMovies.value.filter(movie => movie.popularity > 50); // 예시로 popularity 값이 100 이상인 영화만 필터링
});

const closeModal = () => {
  emit('close');
};

const goToMovieDetail = (movieId) => {
  router.push({ name: 'MovieDetail', params: { id: movieId } });
};

onMounted(() => {
  if (props.isVisible) {
    fetchActorDetails();
  }
});
</script>

<style scoped>
.container{
  margin-top: 100px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  max-width: 800px;
  width: 100%;
  border-radius: 8px;
  position: relative;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

.actor-info {
  display: flex;
  flex-direction: column;
}

.actor-header {
  display: flex;
  margin-bottom: 20px;
}

.actor-photo {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 50%;
  margin-right: 20px;
}

.actor-details {
  display: flex;
  flex-direction: column;
}

.actor-movies {
  margin-top: 20px;
}

.actor-movies h4 {
  font-size: 1.2em;
  margin-bottom: 10px;
}

.movies-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.movie-item {
  cursor: pointer;
  width: 120px;
  height: 180px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.movie-poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 5px;
}
</style>

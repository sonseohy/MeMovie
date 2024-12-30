import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

const API_TOKEN = import.meta.env.VITE_TMDB_API_KEYS

export const useMovieStore = defineStore('movie', () => {
  const likedMovies = ref([]); // 좋아요된 영화 ID 리스트
  const likedActors = ref([]);  // 좋아요된 배우 ID 리스트

  // 좋아요된 영화 관리 함수들
  const setLikedMovies = (movies) => {
    likedMovies.value = movies;
  };

  const addLikedMovie = (movieId) => {
    if (!likedMovies.value.includes(movieId)) {
      likedMovies.value.push(movieId);
    }
  };

  const removeLikedMovie = (movieId) => {
    likedMovies.value = likedMovies.value.filter(id => id !== movieId);
  };

    // 좋아요된 배우 관리 함수들
    const setLikedActors = (actors) => {
      likedActors.value = actors;
    };
  
    const addLikedActor = (actorId) => {
      if (!likedActors.value.includes(actorId)) {
        likedActors.value.push(actorId);
      }
    };
  
    const removeLikedActor = (actorId) => {
      likedActors.value = likedActors.value.filter(id => id !== actorId);
    };

  // 1. 현재 상영중인 영화 리스트 불러오기
  const nowMovies = ref([])
  const getNowMovies = () => {
    axios({
      method:'get',
      url: `https://api.themoviedb.org/3/movie/now_playing`,
      params:{
        api_key: API_TOKEN,
        language:'ko-KR',
        page:1
      },
      headers: {
        accept: "application/json", // JSON 형식 요청
      },
    })
    .then((response) => {
      console.log("API 호출 성공:", response.data);
      nowMovies.value = response.data.results; // ref 데이터 업데이트
    })
    .catch((error) => {
      console.error("API 호출 실패:", error);
    })
  }

  // 2. 영화 검색 상태
  const searchMovies = ref([]); // 검색 결과
  const inputtext = ref(''); // 검색 입력값

  const searchFindMovies = () => {
    if (!inputtext.value.trim()) {
      console.warn('검색어가 비어 있습니다.'); // 검색어가 비어 있으면 경고
      return;
    }
    axios({
      method: 'get',
      url: `https://api.themoviedb.org/3/search/movie`,
      params: {
        query: inputtext.value, // 검색어
        api_key: API_TOKEN,
        language: 'ko-KR',
        include_adult: false,
        page: 1,
      },
      headers: {
        accept: 'application/json',
      },
    })
    .then((response) => {
      console.log('API 호출 성공:', response.data);
      searchMovies.value = response.data.results; // 검색 결과 업데이트
    })
    .catch((error) => {
      console.error('API 호출 실패:', error);
    })
  }

  // Pinia 스토어에서 사용할 데이터와 함수 반환
  return {
    nowMovies,
    getNowMovies,
    searchMovies,
    inputtext,
    searchFindMovies,
    likedMovies,
    setLikedMovies,
    addLikedMovie,
    removeLikedMovie,
    likedActors,
    setLikedActors,
    addLikedActor,
    removeLikedActor,
  }
})
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

// 장고 db와 통신하며 영화 기록하기

export const useRecordStore = defineStore('record', () => {
  // 1. 현재 상영중인 영화 리스트 불러오기
  const recorMovies = ref([])
  const recordMovies = () => {
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
    });
  }

  



  return {
    recorMovies, recordMovies
  }
})
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from '@/stores/account'

export const useCalendarStore = defineStore('calendar', () => {
  const BASE_URL = 'http://127.0.0.1:8000'
  const accountStore = useAccountStore()

  const reviews = ref([]); // 리뷰 데이터를 저장할 변수

 // 리뷰 저장 함수 (Promise 방식으로 구현)
 const submitReview = (payload) => {
  console.log(accountStore)
  return new Promise((resolve, reject) => {
    axios
      .post(`${BASE_URL}/api/calendars/`, payload, {
        headers: {
          Authorization: `Token ${accountStore.token}`, // 사용자 인증 토큰
        },
      })
      .then((response) => {
        console.log('저장 성공:', response.data);

        // 저장된 데이터를 상태에 추가
        reviews.value.push(response.data);

        resolve(response.data); // 성공 시 데이터를 반환
      })
      .catch((error) => {
        console.error('저장 실패:', error.response?.data || error.message);
        reject(error); // 에러를 컴포넌트로 전달
      });
  });
};

// 리뷰 가져오기 함수
const fetchReviews = () => {
  return new Promise((resolve, reject) => {
    axios
      .get(`${BASE_URL}/api/calendars/`, {
        headers: {
          Authorization: `Token ${accountStore.token}`, // 사용자 인증 토큰
        },
      })
      .then((response) => {
        console.log('리뷰 데이터 가져오기 성공:', response.data);
        console.log(accountStore.currentUserId)

        // 내가 작성한 리뷰만 필터링 (review.user는 실제 사용자 ID가 될 가능성 있음)
        const myReviews = response.data.filter(review => review.user === accountStore.currentUserId);
        console.log('내 리뷰', myReviews)
        // 필터링된 데이터 상태에 저장
        reviews.value = myReviews;
        console.log(reviews.value);
        resolve(myReviews); // 성공적으로 가져온 데이터 반환
      })
      .catch((error) => {
        console.error('리뷰 데이터 가져오기 실패:', error.response.data);
        reject(error); // 에러를 컴포넌트로 전달
      });
  });
};



return {
  reviews,
  submitReview,
  fetchReviews,
};
}, { persist: true });
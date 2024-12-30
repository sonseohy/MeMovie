<template>
  <div class="content-container">
    <!-- 사용자 정보 -->
    <div class="user-info-card">
      <div v-if="accountStore.userInfo.profile_picture">
        <img :src="`http://127.0.0.1:8000${accountStore.userInfo.profile_picture}`" alt="Profile" class="profile-image" />
      </div>
      <div v-else>
        <img src="@/assets/profile.png" alt="Profile" class="profile-image" />
      </div>
      <h3 class="username">{{ accountStore.currentUser }}님</h3>
      <p>오늘도 <br> 영화 한 편 어때요? 🎬</p>
      <!-- <p class="user-follow">팔로잉 {{ accountStore.userInfo.followingsCount }} 팔로워 {{ accountStore.userInfo.followersCount }}</p> -->
      <button class="settings-button" @click="goToSetting">
        <i class="fa-solid fa-gear" style="color: #e6e5e5;"></i> 환경설정
      </button>
      <button class="logout-button" @click="logOut">로그아웃</button>
    </div>

  
    <Calendar
      class="calendar-card" @update-reviews="updateReviewCount"
    />


  </div>
</template>

<script setup>
import { useAccountStore } from '@/stores/account';
import Calendar from '@/components/Calendar.vue';
import { ref, watchEffect } from 'vue';
import { useRouter } from 'vue-router';
import axios from "axios";

const router = useRouter();


// 상태 관리
const accountStore = useAccountStore();
const reviewCount = ref(0);

// 프로필 정보 (초기값 설정)
// const user = ref({
//   profileImage: '', // 프로필 이미지 초기값 설정
//   username: '',
//   followingsCount: 0,
//   followersCount: 0
// });


// 프로필 정보 업데이트
const updateUserInfo = (profile) => {
  accountStore.userInfo.value = { ...profile }; // 받아온 프로필 정보를 user에 저장
};


// 로그인된 사용자 정보 확인 (로그인 후 프로필 정보 갱신)
watchEffect(() => {
  if (accountStore.currentUser) {
    axios({
      method: 'GET',
      url: `http://127.0.0.1:8000/api/accounts/profile/${accountStore.currentUser}/`,
    })
      .then((response) => {
        updateUserInfo(response.data);
      })
      .catch((err) => {
        console.error('프로필 정보 요청 실패:', err);
      });
  }
});

// 리뷰 수 업데이트
const updateReviewCount = (count) => {
  reviewCount.value = count;
};

const goToSetting = () => {
  router.push('/Setting')
}

const logOut = () => {
  accountStore.logOut()
}
</script>

<style scoped>
/* 메인 콘텐츠 */
.content-container {
  display: flex;
  width: 100%;
  max-width: 1100px;
  margin: 20px auto; /* 중앙 정렬과 상하 여백 */
  padding-top: 100px;
  gap: 40px;
  position: relative; /* 부모에 상대 위치 지정 */
}


.user-info-card {
  width: 280px;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-bottom: 10px;
}

.username {
  font-size: 18px;
  font-weight: bold;
}

.user-description {
  font-size: 14px;
  color: gray;
}

.user-follow {
  font-size: 14px;
  margin-top: 10px;
}

.settings-button,
.logout-button {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.settings-button {
  background-color: #d1d1d1;
  color: #333;
}

.logout-button {
  background-color: #da6158;
  color: white;
}

.calendar-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  text-align: center;
}

.calendar {
  width: 100%;
}
</style>

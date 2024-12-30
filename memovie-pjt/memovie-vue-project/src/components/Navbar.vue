<template>
  <nav class="navbar">
    <!-- 버튼 -->
    <div class="menu-button-container">
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="offcanvas"
        data-bs-target="#offcanvasNavbar"
        aria-controls="offcanvasNavbar"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
    </div>

    <!-- 오프캔버스 -->
    <div
      class="offcanvas offcanvas-start custom-offcanvas"
      tabindex="-1"
      id="offcanvasNavbar"
      aria-labelledby="offcanvasNavbarLabel"
    >
      <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="offcanvasNavbarLabel">Menu</h5>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="offcanvas"
          aria-label="Close"
        ></button>
      </div>
      <div class="offcanvas-body">
        <!-- 검색 폼 추가 -->
        <!-- <div class="search-container">
          <input
            type="text"
            class="form-control search-input"
            placeholder="Search movie"
            v-model="searchQuery"
          />
          <button class="search-button" @click="findMovie">
            <i class="fa-solid fa-magnifying-glass"></i> 
          </button>
        </div> -->
        <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
          <li class="nav-item">
            <RouterLink :to="{ name: 'MovieList' }" class="nav-link">Recommend</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink :to="{ name: 'Mypage' }" class="nav-link">MyRecord</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink :to="{ name: 'ArticleList' }" class="nav-link">Community</RouterLink>
          </li>
          <li class="nav-item">
            <!-- 로그인 상태에 따라 버튼 변경 -->
            <RouterLink
              v-if="!accountStore.isLogin"
              :to="{ name: 'LogInView' }"
              class="nav-link"
              >Login</RouterLink
            >
            <button
              v-else
              @click="logOut"
              class="nav-link logout-btn"
            >
              Logout
            </button>
            <!-- <MovieChatbot /> -->
          </li>
        </ul>

        <!-- 오프캔버스 UI -->
        <!-- <div class="offcanvas" v-if="showOffcanvas">
          <div class="search-result"> -->
            <!-- 여기에 검색 결과를 동적으로 출력할 수 있습니다 -->
            <!-- <p>검색 결과 내용</p>
          </div>
          <button @click="toggleChatbot">챗봇 열기</button> -->
          <!-- <button @click="closeOffcanvas">오프캔버스를 닫기</button> -->
        <!-- </div> -->

        <!-- 챗봇 컴포넌트 -->
        <!-- <MovieChatbot 
          :isVisible="isChatbotVisible" 
          @update:isVisible="isChatbotVisible = $event" 
          :firstQuestion="firstQuestion"
        /> -->
            
      </div>
    </div>

    <!-- 로고 -->
    <div class="logo-container">
      <RouterLink :to="{ name: 'Main' }">
        <img
          src="@/assets/MeMovie_nav_logo.png"
          alt="Memovie-logo"
          class="nav-logo"
        />
      </RouterLink>
    </div>

    <!-- 링크 -->
    <div class="links-container">
      <RouterLink :to="{ name: 'MovieList' }" class="nav-link">Recommend</RouterLink>
      <RouterLink :to="{ name: 'Mypage' }" class="nav-link">My Record</RouterLink>
      <RouterLink :to="{ name: 'ArticleList' }" class="nav-link">Community</RouterLink>

      <!-- 로그인 상태에 따라 버튼 변경 -->
      <RouterLink
        v-if="!accountStore.isLogin"
        :to="{ name: 'LogInView' }"
        class="nav-link"
        >Login</RouterLink
      >
      <button
        v-else
        @click="logOut"
        class="nav-link logout-btn"
      >
        Logout
      </button>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router';
import { useAccountStore } from "@/stores/account";
import MovieChatbot from '@/components/MovieChatbot.vue';

const accountStore = useAccountStore();
const router = useRouter();

// 상태 정의
const showOffcanvas = ref(true);  // 오프캔버스가 열려 있는지 여부
const isChatbotVisible = ref(false);  // 챗봇의 표시 여부
const searchQuery = ref('');  // 검색 쿼리
const firstQuestion = ref('');  // 첫 번째 질문

// 메소드 정의
const toggleChatbot = () => {
  isChatbotVisible.value = !isChatbotVisible.value;
};

const logOut = () => {
  accountStore.logOut()
}

// 오프캔버스를 닫는 메소드
const closeOffcanvas = () => {
  showOffcanvas.value = false;  // 오프캔버스를 숨김
};

// 검색 기능 메소드
const findMovie = () => {
  if (searchQuery.value.trim() !== '') {
    firstQuestion.value = `You are looking for a movie related to "${searchQuery.value}"?`;  // 첫 질문 설정
    isChatbotVisible.value = true;  // 챗봇 열기
    console.log("Searching for:", searchQuery.value);
    // 여기서 실제 검색 로직을 추가할 수 있습니다.
  } else {
    console.log("검색어를 입력해주세요.");
  }
};
</script>

<style scoped>
/* 스타일은 동일 */
</style>


<style>
/* 네비게이션 바 */
.navbar {
  position: fixed; /* 화면에 고정 */
  top: 20px; /* 상단에 위치 */
  left: 0;
  width: 100%; /* 화면 전체 너비 */
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between; /* 양쪽에 메뉴 버튼과 링크 배치 */
  background: rgba(252, 252, 252, 0.5);
  box-shadow: -4px -4px 4px rgba(0, 0, 0, 0.25),
    4px 4px 4px rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(2px);
  border-radius: 60px;
  padding: 0 30px;
  box-sizing: border-box;
  z-index: 100; /* 항상 위에 표시되도록 z-index 설정 */
}
/* .navbar {
  position: relative; 
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between; 
  background: rgba(252, 252, 252, 0.5);
  box-shadow: -4px -4px 4px rgba(0, 0, 0, 0.25),
    4px 4px 4px rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(2px);
  border-radius: 60px;
  padding: 0 30px;
  box-sizing: border-box;
  z-index: 100;
} */

/* 메뉴 버튼 스타일 */
.menu-button-container {
  position: absolute;
  left: 30px;
}

.menu-button-container .navbar-toggler {
  border: none;
  box-shadow: none;
  outline: none;
  background: transparent;
}

.menu-button-container .navbar-toggler:focus {
  outline: none;
}

/* 로고 항상 가운데 정렬 */
.logo-container {
  position: absolute; /* 절대 위치로 지정 */
  left: 50%; /* 부모의 가로 중심 */
  transform: translateX(-50%); /* 정확히 가운데 정렬 */
}

.nav-logo {
  height: 58px;
}

/* 링크 컨테이너 */
.links-container {
  display: flex;
  align-items: center;
  gap: 20px;
  position: absolute;
  right: 30px;
}

.nav-link {
  font-family: 'Inter', sans-serif;
  font-weight: 400;
  font-size: 15px;
  line-height: 15px;
  color: #28353d;
  text-decoration: none;
  transition: color 0.3s ease;
}

.nav-link:hover {
  font-weight: 600;
  color: #2AA971;
}

.router-link-active {
  font-weight: 600;
  color: #2AA971 !important;
}

/* 오프캔버스 커스터마이징 */
.custom-offcanvas {
  height: 100vh;
  width: 300px;
  background: #ffffff;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  position: fixed;
}

.custom-offcanvas .offcanvas-header {
  border-bottom: 1px solid #ddd;
  padding: 15px;
}

.custom-offcanvas .offcanvas-body {
  flex-grow: 1;
  overflow-y: auto;
  padding: 15px;
}

/* 검색 입력 스타일 */
.search-container {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.search-input {
  border-radius: 30px;
  padding: 10px 15px;
  width: 80%;
  font-size: 14px;
  border: 1px solid #ddd;
  background-color: #f8f9fa;
  box-shadow: none;
}

.search-input:focus {
  border-color: #2AA971;
  box-shadow: 0 0 5px rgba(42, 169, 113, 0.5);
}

.search-button {
  background-color: #2AA971;
  border: none;
  padding: 10px 15px;
  border-radius: 30px;
  color: white;
  font-size: 14px;
  margin-left: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.search-button:hover {
  background-color: #218d58;
}

.search-button i {
  font-size: 16px;
}

/* 네브바에서 검색 결과 보기 */
.search-nav-result {
  margin-top: 50px;
  background-color: #7ff7c3;
}


/* 반응형: 링크 숨기기 */
@media (max-width: 988px) {
  .links-container {
    display: none;
  }
}

.search-result {
  padding: 20px;
}
</style>
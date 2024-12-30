<template>
  <div class="container">
    <div class="left">
      <ul class="menu">
        <li class="line"></li>
        <li><a href="/movies">Recommend</a></li>
        <li><a href="/mypage">Monthly Movie</a></li>
        <li><a href="/community">Community</a></li>
        <li><a href="/movies">Search</a></li>
      </ul>
    </div>
    <div class="center">
      <img class="maintitle" src="@/assets/MainPageimg.png" alt="title">
      <img
        class="cameraimg"
        src="@/assets/moviecam/moviecam.png"
        alt="Camera"
        sizes="(max-width: 479px) 96vw, (max-width: 767px) 98vw, 100vw"
        srcset="
          @/assets/moviecam/moviecam-500w.png 500w,
          @/assets/moviecam/moviecam-800w.png 800w,
          @/assets/moviecam/moviecam-1080w.png 1080w,
          @/assets/moviecam/moviecam-1600w.png 1600w
        "
        loading="lazy"
      />
    </div>
    <div class="right">
      <button @click='MoveToMyPage' class="record-button">+ record memovie</button>
    </div>
  </div>
  <MovieListView/>
</template>

<script setup>
import { useRouter } from 'vue-router'
import MovieListView from './MovieListView.vue';

const router = useRouter()


const MoveToMyPage = () => {
  router.push('/mypage')
}

</script>

<style scoped>
/* 기본 네브바 스타일 */
.navbar {
  position: static; /* 기본적으로 고정되지 않음 */
  width: 100%;
  background-color: #ffffff; /* 네브바 배경 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* 네브바 그림자 */
  z-index: 1000; /* 다른 요소 위에 표시 */
  transition: top 0.3s ease-in-out; /* 고정 시 부드러운 전환 */
}

/* 스크린 크기가 내려갈 경우 네브바 고정 */
@media (max-width: 768px) {
  .navbar {
    position: fixed; /* 상단에 고정 */
    top: 0; /* 화면 상단에 위치 */
    left: 0;
    right: 0;
  }

  /* 콘텐츠가 네브바와 겹치지 않도록 상단 여백 추가 */
  .content-container {
    margin-top: 60px; /* 네브바 높이만큼 여백 */
  }
}


/* 메인 컨테이너 */
.container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  height: 100vh;
}

/* 좌측 메뉴 */
.left {
  flex: 1;
}

.menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.menu li {
  margin: 15px 0;
  border-bottom: 1px solid black; /* 밑줄 추가 */
  padding-bottom: 5px;
}

.menu a {
  text-decoration: none;
  color: black;
  font-size: 18px;
}

/* 중앙 텍스트와 이미지 */
.center {
  flex: 2;
  text-align: center;
  position: relative;
}

.maintitle {
  max-width: 1200px;
}
/* 이미지 스타일 */
.cameraimg {
  width: 100%; /* 반응형 크기 */
  height: auto; /* 비율 유지 */
  display: block; /* 여백 문제 방지 */
}

/* 강조 텍스트 */
.title-highlight {
  color: #2AA971;
  font-weight: bold;
}

/* 오른쪽 버튼 */
.right {
  flex: 1;
  text-align: right;
}

.record-button {
  background: transparent;
  border: 2px solid black;
  padding: 10px 20px;
  border-radius: 20px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.record-button:hover {
  background-color: #2aa971;
  color: white;
}
</style>

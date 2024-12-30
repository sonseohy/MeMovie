<template>
  <div class="container">
    <!-- 좌측 메뉴 -->
    <div class="left">
      <ul class="menu">
        <!-- 메뉴 링크에 'active' 클래스를 동적으로 추가 -->
        <li :class="{ active: currentMenu === 'free' }">
          <a href="#" @click="setMenu('free')">자유게시판</a>
        </li>
        <li :class="{ active: currentMenu === 'myActivities' }">
          <a href="#" @click="setMenu('myActivities')">나의 활동</a>
        </li>
      </ul>
      <button class="write-btn" @click="goToCreate">글 남기기</button>
    </div>

    <!-- 우측 게시글 박스 -->
    <div class="right">
      <ArticleList :filter="filter" />
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import ArticleList from '@/components/ArticleList.vue'
import { useArticleStore } from '@/stores/article'
import { onMounted, ref } from 'vue'
import { useAccountStore } from '@/stores/account'

const router = useRouter();
const store = useArticleStore()
const accountStore = useAccountStore()

// 상태 변수: 현재 선택된 메뉴
const currentMenu = ref('free') // 기본값은 자유게시판

// 필터 변수: 게시글을 필터링하기 위한 값
const filter = ref('')

// 자유게시판 클릭 시 전체 게시글 보기
const setMenu = (menu) => {
  currentMenu.value = menu
  if (menu === 'free') {
    filter.value = ''  // 필터링 없이 전체 게시글 보여주기
  } else if (menu === 'myActivities') {
    filter.value = accountStore.currentUser  // 내가 쓴 게시글만 필터링
  }
}

// 게시글 생성 페이지로 이동
const goToCreate = () => {
  router.push({ name: 'ArticleCreate' })
}

onMounted(() => {
  store.getArticles()
})
</script>

<style scoped>
/* 메인 컨테이너 */
.container {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 40px; /* 상하 패딩 */
  padding-left: 20px; /* 왼쪽 여백 */
  padding-right: 20px; /* 오른쪽 여백 */
  max-width: 1200px; /* 최대 너비 */
  margin-top: 100px; /* 가운데 정렬 */
  height: 100vh;
  box-sizing: border-box; /* 패딩 포함 */
}

/* 좌측 메뉴 */
.left {
  flex: 1; /* 너비 비율: 1 */
  margin-right: 30px; /* 오른쪽 간격 30px */
}

.menu {
  list-style: none;
  padding: 0;
  margin: 0;
  text-align: left !important;
}

.menu li {
  margin: 15px 0;
  border-bottom: 1px solid black;
  padding-bottom: 5px;
}

/* 'active' 클래스를 가진 메뉴 항목에 스타일 적용 */
.menu li.active a {
  font-weight: bold;
  color: #2AA971; /* 활성화된 메뉴의 색상 */
}

.menu a {
  text-decoration: none;
  color: black;
  font-size: 18px;
  transition: color 0.3s ease;
}

.menu a:hover {
  color: #2AA971;
}

.write-btn {
  margin-top: 20px;
  padding: 10px 15px;
  background-color: #2AA971;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.write-btn:hover {
  background-color: #1d8d5a;
}
.right {
  flex: 3;
}
/* 커뮤니티 박스 */
.commu-box {
  flex: 3;
  background: white;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

/* 검색 섹션 */
.search-section {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.search-section label {
  font-size: 16px;
  margin-right: 10px;
}

.search-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
  margin-right: 10px;
}

.search-btn {
  padding: 8px 15px;
  background-color: #2AA971;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.search-btn:hover {
  background-color: #1d8d5a;
}

/* 게시글 */
.post {
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 15px;
}

.post h3 {
  font-size: 20px;
  color: #2AA971;
  margin-bottom: 10px;
}

.post p {
  font-size: 16px;
  line-height: 1.5;
  margin-bottom: 10px;
}

.post-meta {
  font-size: 14px;
  color: #888;
  display: flex;
  justify-content: space-between;
}

/* 페이지네이션 */
.pagination {
  text-align: center;
  margin-top: 20px;
  font-size: 16px;
  color: #333;
}
</style>
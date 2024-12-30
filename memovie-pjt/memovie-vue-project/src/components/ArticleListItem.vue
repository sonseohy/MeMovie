<template>
  <!-- 필터링된 게시글만 표시 -->
  <div v-if="shouldShowArticle && article" class="articles-box">
    <!-- 작성자 프로필 -->
    <div class="user-info-card">
      <div v-if="accountStore.userInfo.profile_picture">
        <img :src="`http://127.0.0.1:8000${accountStore.userInfo.profile_picture}`" alt="Profile" class="profile-image" />
      </div>
      <div v-else>
        <img src="@/assets/profile.png" alt="Profile" class="profile-image" />
      </div>
      <span>작성자 : {{ article.author.username }}</span>
    </div>

    <!-- 게시글 -->
    <div class="aricles-content">
      <RouterLink 
        :to="{ name: 'ArticleDetail', params: { id: article.id } }"  
        class="no-style-link"
        >
        <h5>{{ article.title }}</h5>
      </RouterLink>
      <p>{{ article.content }}</p>
    </div>
    <!-- 게시글 조회수와 좋아요와 작성일 나오는 footer -->
    <div>
      <p class="sub_info">조회수 {{ article.article_views }} &nbsp;&middot;&nbsp; 좋아요 {{ article.like_users.length }} &nbsp;&middot;&nbsp; 작성일 &nbsp;{{ article.created_at }}</p>
    </div>
    <hr>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useAccountStore } from '@/stores/account';
import { computed } from 'vue'

const accountStore = useAccountStore();

const props = defineProps({
  article: Object,
  filter: String // filter prop 추가
})

// 게시글을 보여줄지 여부를 결정하는 computed 변수
const shouldShowArticle = computed(() => {
  // filter가 설정되어 있고, 작성자의 username과 filter가 일치하면 해당 게시글을 보여줌
  if (props.filter) {
    return props.article && props.article.author.username === props.filter
  }
  return props.article != null // article이 null이 아니면 보여줌
})
</script>

<style scoped>
.user-info-card {
  display: inline-flex; /* 수평 배치 */
  align-items: center; /* 수직 중앙 정렬 */
  gap: 10px; /* 이미지와 텍스트 사이 간격 */
}

.profile-image {
  width: 40px; /* 프로필 이미지 크기 */
  height: 40px;
  border-radius: 50%; /* 원형으로 만들기 */
  object-fit: cover; /* 이미지 비율 유지 */
  margin-bottom: 20px;
}

span {
  font-size: 1rem;
}

.aricles-content {
  text-align: left;
}

/* RouterLink의 기본 스타일 제거 */
.no-style-link {
  text-decoration: none;  /* 밑줄 제거 */
  color: inherit;         /* 부모 요소의 텍스트 색상 사용 */
}

/* 제목 스타일 (h5) */
h5 {
  font-size: 24px;         /* 제목의 폰트 크기 */
  font-weight: bold;       /* 제목을 굵게 */
  color: #333;             /* 제목의 텍스트 색상 */
  margin-bottom: 10px;     /* 제목과 본문 사이의 간격 */
  line-height: 1.4;        /* 제목의 줄 높이 */
}

/* 마우스 오버 시 색상 변경 */
h5:hover {
  color: #2AA971;         /* 마우스 오버 시 색상 변경 */
  cursor: pointer;       /* 마우스 오버 시 손 모양 커서 */
  transition: font-weight 0.5s ease;  /* 텍스트 굵기 변화를 부드럽게 하기 위한 트랜지션 */
}

.sub_info {
  text-align: right;
  margin-top: 30px;
  margin-right: 20px;
  color: gray;
  font-size: 15px;
}
</style>
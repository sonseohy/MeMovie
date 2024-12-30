<template>
  <div class=container>
  <div class="box">
    <div v-if="article">
      <h3>제목 : {{ article.title }}</h3>
      <p>내용 : {{ article.content }}</p>
      <p>작성자 : {{ article.author.username }}</p>
      <p>조회수 : {{ article.article_views }}</p>
      <p>작성일 : {{ article.created_at }}</p>
      <p>수정일 : {{ article.updated_at }}</p>
      <p>추천수 : {{ article.like_users_count || 0 }}</p> <!-- like_users_count가 null일 경우 0으로 처리 -->
    </div>

    <!-- 좋아요 버튼, 내가 쓴 게시글이 아닐 때만 보이도록 조건 추가 -->
    <button 
      v-if="article && article.author.username !== login_user" 
      @click="likeArticle" 
      class="like-btn" 
      :class="{ liked: isLiked, 'like-animation': likeAnimation }">
      <i :class="isLiked ? 'fa-solid fa-thumbs-up' : 'fa-regular fa-thumbs-up'"></i>
    </button>

    <!-- 수정 버튼, 내가 쓴 게시글일 때만 보이도록 조건 추가 -->
    <button v-if="article && article.author.username === login_user" @click="edit" class="update-btn">수정</button>

    <!-- 삭제 버튼, 내가 쓴 게시글일 때만 보이도록 조건 추가 -->
    <button v-if="article && article.author.username === login_user" @click="deleteArticle" class="delete-btn">삭제</button>
  </div>
  <CommentCreate />
</div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { useArticleStore } from '@/stores/article'
import { useAccountStore } from '@/stores/account'
import { useRoute, useRouter } from 'vue-router'

import CommentCreate from '@/components/CommentCreate.vue'

const store = useArticleStore()
const account_store = useAccountStore()
const route = useRoute()
const router = useRouter()
const article = ref(null)

// 로그인한 사용자 정보 가져오기
const login_user = account_store.currentUser

// 좋아요 상태 관리
const isLiked = ref(false)

const likeAnimation = ref(false); // 애니메이션 여부

// 게시글 조회 후 좋아요 상태 초기화
onMounted(() => {
  axios({
    method: 'get',
    url: `${store.BASE_URL}/api/articles/${route.params.id}/`,
    headers: {
      Authorization: `Token ${account_store.token}`, // 인증 토큰 추가
    },
  })
    .then((res) => {
      article.value = res.data;
      isLiked.value = res.data.is_liked; // 좋아요 상태 초기화
      likeAnimation.value = false; // 새로고침 시 애니메이션 발생 방지
    })
    .catch((err) => {
      console.log(err);
    });
});


// 삭제 버튼 클릭 시 호출되는 메서드
const deleteArticle = () => {
  store.deleteArticle(route.params.id)  // store에서 삭제 기능 호출
}

// 수정 버튼 클릭 시 호출되는 메서드
const edit = () => {
  router.push({
    name: 'ArticleUpdate',
    params: { id: article.value.id },
    query: { title: article.value.title, content: article.value.content }
  })
}

// 좋아요 버튼 클릭 시 호출되는 메서드
const likeArticle = () => {
  axios({
    method: 'post',
    url: `${store.BASE_URL}/api/articles/${route.params.id}/like/`,
    headers: {
      Authorization: `Token ${account_store.token}`, // 인증 토큰 추가
    },
  })
    .then((res) => {
      isLiked.value = res.data.is_liked; // 서버 응답으로 상태 갱신
      // 좋아요가 새로 추가될 때만 애니메이션 활성화
      if (res.data.is_liked) {
        likeAnimation.value = true;
        setTimeout(() => {
          likeAnimation.value = false; // 애니메이션 해제
        }, 600); // 애니메이션 지속 시간
      }
      article.value.like_users_count = res.data.like_users_count; // 추천 수 업데이트
    })
    .catch((err) => {
      console.error(err.response.data);
    });
};

</script>

<style scoped>

.box {
  background: white;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.delete-btn {
  background-color: black;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 20px;
}

.delete-btn:hover {
  background-color: #d9383b;
}

.update-btn {
  background-color: #218d58;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 20px;
}

.update-btn:hover {
  background-color: #1a7550;
}

.like-btn {
  background-color: transparent; /* 배경색을 없앰 */
  color: #4caf50; /* 기본 색 */
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 20px;
  transition: color 0.3s; /* 색상 변경을 부드럽게 */
}

.like-btn.liked {
  color: #218d58; /* 좋아요 상태일 때 색상 */
}

.like-btn:hover {
  color: #1a7550; /* 호버 시 색상 */
}

.like-btn i {
  font-size: 1.5em; /* 아이콘 크기 */
  transition: transform 0.3s ease; /* 애니메이션을 적용할 때 부드럽게 변화 */
}

/* 좋아요 버튼이 클릭되었을 때 하트 애니메이션 */
.like-btn.like-animation i {
  animation: heart-pulse 0.6s ease-out;
}

/* 하트 아이콘이 커지면서 애니메이션 */
@keyframes heart-pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.4); /* 클릭 시 크기가 커짐 */
  }
  100% {
    transform: scale(1); /* 원래 크기로 돌아옴 */
  }
}
</style>

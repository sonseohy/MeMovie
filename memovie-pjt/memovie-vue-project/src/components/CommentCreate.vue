<template>
  <!-- 댓글 작성 폼 -->
  <div class="comment-form">
    <textarea v-model="newCommentContent" placeholder="댓글을 작성하세요."></textarea>
    <button @click="submitComment">댓글 작성</button>
  </div>
  <div class="box">
    <!-- 댓글 목록 -->
    <h4>댓글 목록</h4>
    <hr>
    <div v-if="comments.length">
      <div v-for="comment in comments" :key="comment.id">
        <p>{{ comment.content }}</p>
        <p style="text-align: right;">작성자 : {{ comment.user.username }}</p>
        <hr>
      </div>
    </div>
    <p v-else><b>아직 작성된 댓글이 없습니다.</b></p>
    
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useArticleStore } from '@/stores/article'
import { useAccountStore } from '@/stores/account'
import { useRoute } from 'vue-router'

const store = useArticleStore()
const accountstore = useAccountStore()
const route = useRoute()

// 상태 관리
const comments = ref([]) // 댓글 목록
const newCommentContent = ref('') // 새 댓글 내용
const isCommentFormVisible = ref(false) // 댓글 작성 폼 표시 여부

// 댓글 목록 가져오기
const fetchComments = () => {
  axios({
    method: 'get',
    url: `${store.BASE_URL}/api/articles/${route.params.id}/comments/`
  })
    .then((res) => {
      comments.value = res.data
    })
    .catch((err) => {
      console.error('댓글을 가져오는 데 실패했습니다.', err.response.data)
    })
}

// 댓글 작성하기
const submitComment = () => {
  if (!newCommentContent.value) {
    alert('댓글 내용을 입력해주세요.')
    return
  }

  axios({
    method: 'post',
    url: `${store.BASE_URL}/api/articles/${route.params.id}/comments/`,
    headers: {
      Authorization: `Token ${accountstore.token}`, // 사용자 인증 토큰 추가
    },
    data: {
      content: newCommentContent.value
    }
  })
    .then((res) => {
      // 댓글을 성공적으로 추가한 후, 댓글 목록 갱신
      comments.value.push(res.data)
      newCommentContent.value = '' // 입력 폼 초기화
      isCommentFormVisible.value = false // 폼 숨기기
    })
    .catch((err) => {
      console.log('댓글을 작성하는 데 실패했습니다.', err.response.data)
    })
}

// 댓글 작성 폼 토글
const toggleCommentForm = () => {
  isCommentFormVisible.value = !isCommentFormVisible.value
}

onMounted(() => {
  fetchComments() // 페이지가 로드되면 댓글 목록을 불러옴
})
</script>

<style scoped>
.box {
  background: #fafafa;
  border-radius: 10px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  padding: 20px;
  width: 100%;
  margin: 0 auto;
}

h4 {
  font-size: 22px;
  font-weight: 600;
  color: #333;
  margin-bottom: 15px;
}

textarea {
  width: 100%;
  height: 100px;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-sizing: border-box;
  margin-bottom: 10px;
  resize: none;
}

button {
  padding: 12px 20px;
  background-color: #218d58;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 100%;
}

button:hover {
  background-color: #1a7550;
}

p {
  color: #666;
  font-size: 14px;
}

button {
  margin-top: 10px;
}

button:hover {
  background-color: #1a7550;
}

button {
  margin-top: 15px;
  padding: 10px 25px;
  background-color: #218d58;
  color: white;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #1a7550;
}
</style>

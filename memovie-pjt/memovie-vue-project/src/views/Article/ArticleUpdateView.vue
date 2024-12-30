<template>
  <div class="box">
    <h1>Article Update</h1>
    <form @submit.prevent="updateArticle">
      <div class="form-group">
        <label for="title">제목 :</label>
        <input type="text" id="title" v-model.trim="title" class="input-field">
      </div>
      <div class="form-group">
        <label for="content">내용 :</label>
        <textarea id="content" v-model.trim="content" class="textarea-field"></textarea>
      </div>
      <input type="submit" value="수정" class="submit-btn">
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useArticleStore } from '@/stores/article'
import { useAccountStore } from '@/stores/account'
import axios from 'axios'

const title = ref('')
const content = ref('')
const store = useArticleStore()
const accountstore = useAccountStore()
const route = useRoute()

// 컴포넌트가 마운트되었을 때, 수정할 게시글의 데이터를 가져와서 폼에 채운다
onMounted(() => {
  if (route.params.id) {
    // 게시글 ID가 있다면 수정 모드로 진입
    axios.get(`${store.BASE_URL}/api/articles/${route.params.id}/`, {
      headers: {
        Authorization: `Token ${accountstore.token}`, // 인증 토큰 포함
      }
    })
      .then((res) => {
        title.value = res.data.title
        content.value = res.data.content
      })
      .catch((err) => {
        console.log(err)
      })
  }
})

const updateArticle = function () {
  const payload = {
    title: title.value,
    content: content.value
  }
  
  store.updateArticle(route.params.id, payload)
}

</script>

<style scoped>
.box {
  background: white;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

h1 {
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 8px;
}

.input-field, .textarea-field {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-sizing: border-box;
}

.textarea-field {
  height: 200px;
  resize: none; /* 사용자가 크기 조절을 못하게 설정 */
  overflow-y: auto; /* 내용이 많으면 스크롤이 생기게 함 */
}

.submit-btn {
  background-color: #218d58;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  width: 100%;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-btn:hover {
  background-color: #1a7550;
}
</style>
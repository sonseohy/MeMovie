<template>
  <div class="container">
  <div class="box">
    <h1>게시글 작성</h1>
    <form @submit.prevent="createArticle">
      <div class="form-group">
        <label for="title">제목 :</label>
        <input type="text" id="title" v-model.trim="title" class="input-field">
      </div>
      <div class="form-group">
        <label for="content">내용 :</label>
        <textarea id="content" v-model.trim="content" class="textarea-field"></textarea>
      </div>
      <input type="submit" value="작성" class="submit-btn">
    </form>
  </div>
</div>
</template>

<script setup>
import { ref } from 'vue'
import { useArticleStore } from '@/stores/article'

const title = ref(null)
const content = ref(null)
const store = useArticleStore()

const createArticle = function () {
  const payload = {
    title: title.value,
    content: content.value
  }
  store.createArticle(payload)
}
</script>

<style scoped>

.container{
  margin-top: 100px;
}
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
  font-weight: 300;
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

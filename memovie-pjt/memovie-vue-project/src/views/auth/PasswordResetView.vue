<template>
  <div>
    <h2>비밀번호 리셋</h2>
    <form @submit.prevent="resetPassword">
      <input v-model="email" type="email" placeholder="이메일 주소" required />
      <button type="submit">비밀번호 리셋 요청</button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'

export default {
  setup() {
    const email = ref('')

    const resetPassword = async () => {
      try {
        await axios.post('http://localhost:8000/auth/password/reset/', {
          email: email.value,
        })
        alert('비밀번호 리셋 이메일이 발송되었습니다.')
      } catch (error) {
        console.error(error)
        alert('이메일을 확인해주세요.')
      }
    }

    return {
      email,
      resetPassword,
    }
  },
}
</script>


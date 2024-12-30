<template>
  <div class="signup-container">
    <div class="signup-box">
      <!-- 상단 제목 -->
      <div class="signup-welcome-section">
        <h1 class="welcome">반가워요 :)</h1>
        <h2 class="sign-in-title">같이 메무비 하실래요?💕</h2>
        <p class="subtitle">Memo + Movie = Me + Movie <br>메무비에서 유익한 기록 생활을 해보아요;)</p>
      </div>

      <!-- 회원가입 폼 -->
      <form @submit.prevent="signUp" class="signup-form">
        <!-- Username -->
        <div class="signup-form-group">
          <label for="username" class="signup-form-label">User name</label>
          <input type="text" id="username" v-model.trim="username" class="signup-form-input" placeholder="Enter your user name">
        </div>

        <!-- Email -->
        <div class="signup-form-group">
          <label for="email" class="signup-form-label">Email</label>
          <input type="email" id="email" v-model.trim="email" class="signup-form-input" placeholder="Enter your email">
        </div>

        <!-- Password -->
        <div class="signup-form-group">
          <label for="password1" class="signup-form-label">Password</label>
          <input type="password" id="password1" v-model.trim="password1" class="signup-form-input" placeholder="Enter your password">
        </div>

        <!-- Confirm Password -->
        <div class="signup-form-group">
          <label for="password2" class="signup-form-label">Confirm Password</label>
          <input type="password" id="password2" v-model.trim="password2" class="signup-form-input" placeholder="Confirm your password">
        </div>

        <!-- Submit 버튼 -->
        <div class="signup-form-group">
          <button type="submit" class="signup-submit-button">Register</button>
        </div>
      </form>

      <!-- 하단 링크 -->
      <p class="signup-already-account">
        Already have an account? <RouterLink :to="{ name: 'LogInView' }" class="signup-login-link">Login</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/account'

const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const email = ref(null)

const store = useAccountStore()

const signUp = function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    email: email.value,
  }
  store.signUp(payload)
}
</script>

<style scoped>
body {
  font-family: "Inter", sans-serif;
}

/* 제목 스타일 */
.welcome {
  font-family: "Inter", sans-serif;
  font-optical-sizing: auto;
  font-weight: 600; /* 굵게 설정 */
  font-style: normal;
}

.sign-in-title {
  font-family: "Inter", sans-serif;
  font-optical-sizing: auto;
  font-weight: 500; /* 굵게 설정 */
  font-style: normal;
}

.subtitle {
  font-family: "Inter", sans-serif;
  font-weight: 400;
  font-size: 16px;
  line-height: 24px;
  color: #000000;
  margin-bottom: 30px;
}

/* 전체 컨테이너 */
.signup-container {
  display: flex;
  justify-content: right;
  margin-right: 200px;
  align-items: center;
  height: 100vh;
  background-color: #f8f8f8;
  background-image: url('@/assets/loginback2.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

/* 회원가입 박스 */
.signup-box {
  width: 505px;
  background: #ffffff;
  border: 0.5px solid #878787;
  box-shadow: 0px 4px 64px rgba(0, 0, 0, 0.05);
  border-radius: 10px;
  padding: 30px;
  box-sizing: border-box;
}

/* 상단 섹션 */
.signup-welcome-title {
  font-family: 'Poppins', sans-serif;
  font-size: 25px;
  font-weight: 300;
  color: #000000;
}

.signup-sign-up-title {
  font-family: 'Poppins', sans-serif;
  font-size: 31px;
  font-weight: 500;
  color: #000000;
  margin: 10px 0;
}

.signup-description {
  font-family: 'Poppins', sans-serif;
  font-size: 16px;
  font-weight: 400;
  color: #000000;
}

/* 폼 섹션 */
.signup-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.signup-form-group {
  display: flex;
  flex-direction: column;
}

.signup-form-label {
  font-family: 'Poppins', sans-serif;
  font-size: 16px;
  font-weight: 400;
  color: #000000;
}

.signup-form-input {
  padding: 10px;
  font-family: 'Poppins', sans-serif;
  font-size: 14px;
  font-weight: 300;
  color: #282828;
  border: 0.6px solid #282828;
  border-radius: 6px;
  box-sizing: border-box;
}

.signup-form-input::placeholder {
  color: #ABABAB;
}

/* 버튼 */
.signup-submit-button {
  padding: 15px;
  background: #000000;
  color: #FFFFFF;
  font-family: 'Poppins', sans-serif;
  font-size: 16px;
  font-weight: 500;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.signup-submit-button:hover {
  background: #333333;
}

/* 하단 링크 */
.signup-already-account {
  text-align: center;
  margin-top: 20px;
  font-family: 'Poppins', sans-serif;
  font-size: 16px;
  font-weight: 300;
  color: #7D7D7D;
}

.signup-login-link {
  color: #000000;
  text-decoration: none;
  font-weight: 500;
}

.signup-login-link:hover {
  text-decoration: underline;
}
</style>

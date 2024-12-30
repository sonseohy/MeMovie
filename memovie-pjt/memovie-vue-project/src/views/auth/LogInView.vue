<template>
  <div class="login-container">
    <div class="login-box">
      <h1 class="welcome">안녕하세요 :)</h1>
      <h3 class="sign-in-title">로그인으로 함께해요</h3>
      <p class="subtitle">Memo + Movie = Me + Movie <br>메무비에서 유익한 기록 생활을 해보아요;)</p>

      <form @submit.prevent="logIn" class="login-form">
        <div class="form-group">
          <label for="username" class="label">User name</label>
          <input
            type="text"
            id="username"
            v-model.trim="username"
            placeholder="Enter your user name"
            class="input"
            @input="saveUsername"
          />
        </div>

        <div class="form-group">
          <label for="password" class="label">Password</label>
          <div class="password-container">
            <input
              :type="showPassword ? 'text' : 'password'"
              id="password"
              v-model.trim="password"
              placeholder="Enter your Password"
              class="input"
            />
            <span
              class="toggle-password"
              @click="togglePassword"
              title="Show/Hide Password"
            >
              👀
            </span>
          </div>
        </div>

        <div class="form-options">
          <label class="remember-me">
            <input type="checkbox" v-model="rememberMe" @change="saveUsername" />
            Remember me
          </label>
          <RouterLink :to="{ name: 'PasswordResetView' }" class="forgot-password"
            >Forgot Password?</RouterLink
          >
        </div>

        <button type="submit" class="login-button">Log In</button>
      </form>

      <p class="register-link">
        Don’t have an Account? <RouterLink :to="{ name: 'SignUpView' }">Register</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAccountStore } from "@/stores/account";

const username = ref(localStorage.getItem("savedUsername") || "");
const password = ref(null);
const showPassword = ref(false);
const rememberMe = ref(false);

const store = useAccountStore();

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value,
  };
  store.logIn(payload);
};

const togglePassword = () => {
  showPassword.value = !showPassword.value;
};

const saveUsername = () => {
  if (rememberMe.value && username.value) {
    localStorage.setItem("savedUsername", username.value);
  } else {
    localStorage.removeItem("savedUsername");
  }
};

onMounted(() => {
  const savedUsername = localStorage.getItem('savedUsername');
  if (savedUsername) {
    username.value = savedUsername; // 저장된 username을 불러옴
    rememberMe.value = true; // 체크박스를 활성화
    console.log('초기 username 설정:', username.value);
  } else {
    console.log('저장된 username 없음');
  }
});
</script>
<style scope>
body {
  font-family: "Inter", sans-serif;
}

/* 전체 컨테이너 */
.login-container {
  display: flex;
  justify-content: right;
  height: 18px;
  margin-right: 200px;
  align-items: center;
  height: 100vh;
  background-color: #f8f8f8;
  background-image: url('@/assets/loginback2.png'); /* 이미지 경로 설정 */
  background-size: cover; /* 이미지 크기를 컨테이너에 맞게 */
  background-position: center; /* 이미지를 중앙에 정렬 */
  background-repeat: no-repeat; /* 이미지를 반복하지 않음 */
}


/* 로그인 박스 */
.login-box {
  position: relative;
  font-weight: 400;
  width: 505px;
  height: 650x;   /* 로그인 박스  길이 조절*/
  background: #ffffff;
  border: 0.5px solid #878787;
  box-shadow: 0px 4px 64px rgba(0, 0, 0, 0.05);
  border-radius: 10px;
  padding: 30px;
  box-sizing: border-box;
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

/* 폼 스타일 */
.login-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 20px;
}

.label {
  display: block;
  font-family: 'Poppins', sans-serif;
  font-weight: 400;
  font-size: 16px;
  line-height: 24px;
  color: #000000;
  margin-bottom: 8px;
}

.input {
  width: 100%;
  height: 40px;
  border: 0.6px solid #282828;
  border-radius: 6px;
  padding: 10px;
  font-family: 'Poppins', sans-serif;
  font-size: 14px;
  color: #000000;
  box-sizing: border-box;
}

/* 옵션 스타일 */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.remember-me {
  font-family: 'Poppins', sans-serif;
  font-size: 12px;
  color: #000000;
}

.forgot-password {
  font-family: 'Poppins', sans-serif;
  font-size: 12px;
  color: #4D4D4D;
  text-decoration: none;
}

/* 로그인 버튼 */
.login-button {
  width: 100%;
  height: 50px;
  background: #000000;
  color: #ffffff;
  font-family: 'Poppins', sans-serif;
  font-weight: 500;
  font-size: 16px;
  line-height: 24px;
  text-align: center;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

/* 하단 링크 */
.register-link {
  font-family: 'Poppins', sans-serif;
  font-size: 16px;
  font-weight: 300;
  text-align: center;
  margin-top: 20px;
  color: #7d7d7d;
}

.register-link a {
  color: #0000ff;
  text-decoration: none;
}

/* 비밀번호 관련 */
.password-container {
  display: flex;
  align-items: center;
  position: relative;
}

.toggle-password {
  cursor: pointer;
  position: absolute;
  right: 10px;
  font-size: 18px;
  user-select: none;
}
</style>

<template>
  <div class="container">
    <div class="profile-edit">
      <div class="sidebar">
        <img :src="user.profileImage" alt="Profile Image" class="profile-image" />
        <h2>{{ accountStore.currentUser }}</h2>
        <!-- <p>팔로잉 {{ user.following }} 팔로워 {{ user.followers }}</p> -->
        <div class="selected-genres">
          <p>선호 장르 | {{ selectedGenreNames.length > 0 ? selectedGenreNames.join(', ') : '선택된 장르 없음' }}</p>
        </div>
        <div class="actions">
          <button @click="handleLogout">로그아웃</button>
        </div>
      </div>

      <div class="form-container">
        <h3>회원 정보 수정</h3>
        <!-- 프로필 사진 수정 폼 -->
        <div class="profile-image-upload">
          <!-- <div> -->
            <input type="file" @change="onFileChange" />
            <button @click="uploadImage">이미지 업로드</button>
            <!-- <img v-if="imageUrl" :src="imageUrl" alt="프로필 이미지" />
          </div> -->
          <div v-if="uploadedImageUrl">
            <p>업로드된 이미지:</p>
            <img :src="uploadedImageUrl" alt="Profile Image" width="150" />
          </div>
        </div>

        <!-- 개인정보 수정 폼 -->
        <form @submit.prevent="saveProfile">
          <div class="form-group"> 
            <label for="lastName">Last Name / 이름</label>
            <input v-model="form.lastName" id="lastName" type="text" />
          </div>
          <div class="form-group">
            <label for="firstName">First Name / 성</label>
            <input v-model="form.firstName" id="firstName" type="text" />
          </div>
          <div class="form-group">
            <label for="password">password / 비밀번호 변경</label>
            <input v-model="form.password" id="password" type="text" />
            <input type="submit" value="비밀번호 수정">
          </div>
          <div class="form-group">
            <label for="email">Email / 이메일</label>
            <input v-model="form.email" id="email" type="email" />
          </div>
          <!-- 영화 장르 선택 폼 -->
          <div class="form-group">
            <label>Favorite Genres / 좋아하는 장르</label>
            <div class="genres-checkbox-group">
              <div v-for="genre in genres" :key="genre.id" class="checkbox-item">
                <input
                  type="checkbox"
                  :value="genre.id"
                  v-model="selectedGenres"
                  :id="`genre-${genre.id}`"
                />
                <label :for="`genre-${genre.id}`">{{ genre.genre_name }}</label>
              </div>
            </div>
          </div>
          <div class="form-group">
            <label for="aboutMe">About Me / 자기소개</label>
            <textarea v-model="form.aboutMe" id="aboutMe"></textarea>
          </div>
          <div class="form-actions">
            <button type="button" @click="cancelEdit" class="cancel-btn">CANCEL</button>
            <button type="submit" class="save-btn">SAVE</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useAccountStore } from "@/stores/account";
import axios from "axios";

// Pinia store 사용
const accountstore = useAccountStore()

const selectedFile = ref(null); // 선택된 파일을 저장하는 변수
const uploadedImageUrl = ref(null); // 업로드된 이미지 URL

// 선택한 장르
const selectedGenres = ref([]); // 선택된 장르의 ID 저장
const genres = ref([]); // DB에서 가져온 장르 목록

// DB에서 장르 가져오기
const fetchGenres = async () => {
  try {
    const response = await axios.get("http://localhost:8000/api/movies/genres/");
    console.log(response.data)
    genres.value = response.data; // [{ id: 1, name: "액션" }, { id: 2, name: "코미디" }, ...]
  } catch (error) {
    console.error("장르 데이터를 가져오는 중 오류가 발생했습니다:", error);
  }
};

// 페이지 로드 시 장르 데이터 가져오기
onMounted(() => {
  fetchGenres();
});

const selectedGenreNames = computed(() => {
  return selectedGenres.value
    .map(id => {
      const genre = genres.value.find(g => g.id === id);
      return genre ? genre.genre_name : null;
    })
    .filter(name => name);
});


// 파일 선택 시 호출되는 함수
const onFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    selectedFile.value = file;
    // 이미지 미리보기 (선택된 파일이 이미지일 경우)
    uploadedImageUrl.value = URL.createObjectURL(file);
  }
};


// 개인정보 수정 관련
const accountStore = useAccountStore();

const router = useRouter();

const user = ref({
  profileImage: "https://via.placeholder.com/150",
  movieCount: 115,
  following: 3,
  followers: 10,
});

const form = ref({
  firstName: "",
  lastName: "",
  password:"",
  email: "",
  aboutMe: "",
});

const saveProfile = async () => {
  
  try {
    const updatedProfile = {
      firstName: form.value.firstName,
      lastName: form.value.lastName,
      password: form.value.password,
      email: form.value.email,
      aboutMe: form.value.aboutMe,
      image: selectedFile.value,
      favorite_genres: selectedGenres.value, // 선택한 장르 저장
    };
    console.log(form.value)
    console.log(selectedGenres.value)
    accountStore.updateProfile(updatedProfile);
    alert("프로필 저장 완료!");
  } catch (error) {
    alert("프로필 저장 중 오류가 발생했습니다.");
    console.error(error);
  }
};

const cancelEdit = () => {
  alert("수정을 취소했습니다.");
  form.firstName = "";
  form.lastName = "";
  form.password = "";
  form.email = "";
  form.aboutMe = "";
  selectedGenres.value = [];
};


const handleLogout = async () => {
  try {
    await accountStore.logOut();
    alert("로그아웃 완료!");
    console
  } catch (error) {
    alert("로그아웃 중 오류가 발생했습니다.");
    console.error(error);
  }
};

</script>

<style scoped>
.container{
  padding-top: 100px;
}

.genres-checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 5px;
  
}


.checkbox-item input {
  margin-right: 5px;
}

.selected-genres {
  margin-top: 10px;
  color: #218d58;
}

.profile-image-upload {
  max-width: 500px;
  text-align: left;
  font-weight: bold;
}

input[type="file"] {
  margin-bottom: 10px;
}

button:disabled {
  background-color: #ccc;
}

.profile-edit {
  display: flex;
  padding: 20px;
  flex-wrap: wrap; /* 작은 화면에서 자동 줄바꿈 */
}

.sidebar {
  width: 20%;
  margin-right: 30px;
  text-align: center;
  border-right: 2px solid #2AA971; 
  flex-shrink: 0;
}

.profile-image {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  margin-bottom: 10px;
}

.actions button {
  display: block;
  margin: 10px auto;
  padding: 10px 20px;
  border: none;
  background: #eee;
  cursor: pointer;
}

.form-container {
  width: 70%;
  padding: 20px;
}

h3 {
  font-size: 1.5rem;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.form-actions button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.save-btn {
  background-color: #218d58;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 20px;
}

.save-btn:hover {
  background-color: #1a7550;
}

.cancel-btn {
  background-color: black;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 20px;
}

.cancel-btn:hover {
  background-color: #333333 ;
}

/* 반응형 스타일 */
@media (max-width: 992px) {
  .profile-edit {
    flex-direction: column; /* 화면이 작아지면 세로 정렬 */
    padding: 10px;
  }

  .sidebar {
    width: 100%;
    margin: 0 0 20px 0; /* 하단에 간격 추가 */
    border-right: none;
    border-bottom: 2px solid #2AA971; /* 구분선 위치 변경 */
  }

  .form-container {
    width: 100%; /* 화면 크기에 맞게 너비 조정 */
    padding: 10px;
  }

  h3 {
    font-size: 1.25rem; /* 제목 크기 축소 */
  }
}

@media (max-width: 768px) {
  .profile-image {
    width: 100px; /* 프로필 이미지 크기 축소 */
    height: 100px;
  }

  .form-group input,
  .form-group textarea {
    font-size: 14px; /* 입력 필드 글꼴 크기 축소 */
  }

  .save-btn,
  .cancel-btn {
    font-size: 14px;
    padding: 8px 15px;
  }

  .actions button {
    padding: 8px 15px;
    font-size: 14px;
  }
}

@media (max-width: 576px) {
  .profile-edit {
    padding: 5px;
  }

  .profile-image {
    width: 80px;
    height: 80px;
  }

  .form-group label {
    font-size: 14px;
  }

  .form-group input,
  .form-group textarea {
    font-size: 12px;
  }

  .save-btn,
  .cancel-btn {
    font-size: 12px;
    padding: 6px 10px;
  }
}

.checkbox-item {
  display: flex;
  align-items: center; /* 체크박스와 글씨를 수직 중앙 정렬 */
  gap: 5px; /* 체크박스와 글씨 사이 간격 */
}

.checkbox-item input {
  vertical-align: middle; /* 체크박스를 텍스트와 동일한 라인에 정렬 */
}

.checkbox-item label {
  font-size: 16px; /* 글씨 크기 */
  color: #333; /* 글씨 색상 */
  font-weight: 500; /* 글씨 두께 */
  cursor: pointer; /* 마우스를 올리면 커서가 손 모양으로 변경 */
  transition: color 0.3s ease; /* 색상 전환 효과 */
}

.checkbox-item input:checked + label {
  color: #218d58; /* 체크된 항목 색상 */
}

/* 체크박스를 hover할 때 색상 변화 */
.checkbox-item label:hover {
  color: #2aa971; /* 마우스를 올렸을 때 글씨 색상 */
}


</style>

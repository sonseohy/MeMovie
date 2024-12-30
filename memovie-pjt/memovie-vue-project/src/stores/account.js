import { ref, computed } from "vue";
import { defineStore } from "pinia";
import router from "@/router";
import axios from "axios";

export const useAccountStore = defineStore(
  "account",
  () => {
    const BASE_URL = "http://127.0.0.1:8000";

    const token = ref(null);
    const currentUser = ref(null);
    const currentUserId = ref(null);
    const userInfo = ref(null)

    const isLogin = computed(() => {
      if (token.value === null) {
        return false
      } else {
        return true
      }
    })
  
  // 회원가입 요청 액션
  const signUp = function (payload) {
    const { username, password1, password2, email } = payload

    axios({
      method: 'post',
      url: `${BASE_URL}/accounts/signup/`,
      data: {
        username, password1, password2, email
      }
    })
      .then((response) => {
        console.log(response)
        console.log('회원가입 성공')
        // 회원가입 성공시 로그인 페이지로 이동
        router.push({ name: "LogInView" })
      })
      .catch((error) => {
        console.error(error.response.data)
      })
  }

  // 로그인 요청 액션
  const logIn = function (payload) {
    const { username, password } = payload
    axios({
      method: 'post',
      url: `${BASE_URL}/accounts/login/`,
      data: {
        username : username , 
        password : password
      }
    })
      .then((res) => {
        currentUser.value = payload.username
        token.value = res.data.key
        console.log('http://127.0.0.1:8000/api/accounts/profile/${currentUser.value}/')
        // 로그인 후 프로필 정보 요청 (GET 요청은 params로 데이터 전송)
        axios({
          method: 'GET',
          url: `http://127.0.0.1:8000/api/accounts/profile/${currentUser.value}/`,
          params: {
            username: username, // username을 쿼리 파라미터로 전달
          }
        })
          .then((response) => {
            // 프로필 데이터 받아오기
            userInfo.value = response.data; // 받아온 데이터로 useInfo 갱신
            console.log('프로필 정보:', userInfo.value);
            currentUserId.value = userInfo.value.id
            router.push({ name: 'Main' })        
          })
          .catch((err) => {
            console.error('프로필 정보 요청 실패:', err.response.data);
          });
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // [추가기능] 로그아웃
  const logOut = function () {
    console.log('123')
    axios({
      method: 'post',
      url: `${BASE_URL}/accounts/logout/`,
    })
      .then((res) => {
        console.log(res.data)
        token.value = null
        currentUser.value = null

        // Pinia 상태 초기화
        const accountStore = useAccountStore();  // account store
        accountStore.$reset();  // Pinia store 초기화 (상태를 리셋)

        const movieStore = useMovieStore();  // movie store
        movieStore.$reset();  // Pinia store 초기화

        const articleStore = useArticleStore();  // account store
        articleStore.$reset();  // Pinia store 초기화 (상태를 리셋)

        const calendarStore = useCalendarStore();  // movie store
        calendarStore.$reset();  // Pinia store 초기화

        // localStorage.removeItem('pinia')

        console.log('로그아웃')
        router.push({ name: 'Main' })
      })
      .catch((err) => {
        console.log(err)
      })     
  }

    // 비밀번호 리셋 요청 메서드
    const resetPassword = async (email) => {
      try {
        await axios.post(`${BASE_URL}/accounts/reset-password/`, { email });
        alert("비밀번호 재설정 이메일이 전송되었습니다!");
      } catch (error) {
        console.error("비밀번호 재설정 실패:", error.response.data);
        alert("비밀번호 재설정 중 오류가 발생했습니다.");
      }
    };

    // 사용자 프로필 정보 업데이트 함수

    const updateProfile = (form) => {
      console.log(2, form);
      
      const requestBody = {
        first_name: form.firstName,
        last_name: form.lastName,
        email: form.email,
        profile_picture: form.image,
        aboutMe: form.aboutMe,
        genres: Object.values(form.favorite_genres), // genres 배열로 변환
      };
    
      console.log("Request Body:", requestBody);
    

    
      axios({
        method: 'put',
        url: `http://127.0.0.1:8000/api/accounts/profile/${currentUser.value}/`,
        data: requestBody,
        headers: {      
          Authorization: `Token ${token.value}`, // Token 인증 사용
          'Content-Type': 'multipart/form-data',
        }
      })
      .then((response) => {
        if (response && response.data) {
          console.log('결과', response.data)
          userInfo.value = response.data; // 받아온 데이터로 useInfo 갱신
          // userInfo.value.profileImage = `http://127.0.0.1:8000${uploadedImageUrl}`;  // 프로필 이미지 URL을 갱신
          alert("이미지 업로드 성공!");
        }
      })
      .catch((error) => {
        console.error('Error:', error);
        if (error.response) {
          console.error("서버 오류:", error.response.data);
          alert("이미지 업로드 실패: " + error.response.data.error);
        } else if (error.request) {
          console.error("응답 없음:", error.request);
          alert("서버 응답이 없습니다. 네트워크 오류를 확인하세요.");
        } else {
          console.error("오류 발생:", error.message);
          alert("이미지 업로드 중 오류가 발생했습니다.");
        }
      });
    };

    // const updateProfile = async (profileData) => {
    //   try {
    //     const response = await axios.put(
    //       `${BASE_URL}/accounts/profile/`,
    //       profileData,
    //       {
    //         headers: {
    //           Authorization: `Token ${token.value}`,
    //         },
    //       }
    //     );
    //     console.log("프로필 업데이트 성공:", response.data);
    //     return response.data; // 업데이트된 프로필 반환
    //   } catch (error) {
    //     console.error("프로필 업데이트 실패:", error.response?.data || error);
    //     throw new Error("프로필 업데이트 중 오류 발생");
    //   }
    // };

    // // 프로필 이미지 업로드 함수
    // const uploadProfileImage = async (file) => {
    //   const formData = new FormData();
    //   formData.append("profile_picture", file);

    //   try {
    //     const response = await axios.post(
    //       `${BASE_URL}/accounts/upload-profile-image/`,
    //       formData,
    //       {
    //         headers: {
    //           Authorization: `Token ${token.value}`,
    //           "Content-Type": "multipart/form-data",
    //         },
    //       }
    //     );
    //     console.log("프로필 이미지 업로드 성공:", response.data);
    //     return response.data.imageUrl; // 업로드된 이미지 URL 반환
    //   } catch (error) {
    //     console.error("프로필 이미지 업로드 실패:", error.response?.data || error);
    //     throw new Error("프로필 이미지 업로드 중 오류 발생");
    //   }
    // };

    // 현재 사용자 정보 가져오기 함수
    const fetchCurrentUser = async () => {
      try {
        const response = await axios.get(`${BASE_URL}/accounts/current-user/`, {
          headers: {
            Authorization: `Token ${token.value}`,
          },
        });
        currentUser.value = response.data; // 서버에서 받은 사용자 데이터 저장
        console.log("현재 사용자 정보 가져오기 성공:", response.data);
      } catch (error) {
        console.error("현재 사용자 정보 가져오기 실패:", error.response?.data || error);
        throw new Error("현재 사용자 정보를 가져오는 중 오류 발생");
      }
    };

    return {
      BASE_URL,
      token,
      currentUser,
      currentUserId,
      isLogin,
      signUp,
      logIn,
      logOut,
      resetPassword,
      updateProfile,
      // uploadProfileImage,
      fetchCurrentUser,
      userInfo
    };
  },
  { persist: true }
);
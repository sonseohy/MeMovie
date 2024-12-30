<template>
  <!-- FullCalender가 아닌 calendar 사용 -->
  <div class="calendar">
    <!-- FullCalendar 사용 -->
    <div id="calendar"></div>

    <!-- 모달 (영화 기록 작성) -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <!-- 닫기 버튼 -->
        <button class="close-button" @click="closeModal">×</button>

        <!-- 모달 내용 -->
        <h2>영화 기록</h2>
        <p>선택한 날짜: {{ selectedDate }}</p>

        <!-- 영화 제목 입력 폼 -->
        <div class="form-group">
          <label for="title">영화 제목</label><br>
          <div class="movie-input-container">
            <input
              type="text"
              id="title"
              v-model="title"
              placeholder="영화 제목을 검색하세요"
              @input="searchMovies"
            />
            <!-- 선택된 영화 포스터 -->
            <div class="selected-poster">
              <img
                v-if="selectedMoviePoster"
                :src="`https://image.tmdb.org/t/p/w200${selectedMoviePoster}`"
                alt="선택된 영화 포스터"
              />
            </div>
          </div>
          <!-- 검색 결과 -->
          <ul v-if="searchResults.length > 0" class="search-results">
            <li
              v-for="(movie, index) in searchResults"
              :key="index"
              @click="selectMovie(movie)"
              class="movie-item"
            >
              {{ movie.title }}
            </li>
          </ul>
        </div>

        <!-- 영화 내용 입력 폼 -->
        <div class="form-group">
          <label for="content">영화 내용</label><br>
          <textarea id="content" 
            v-model="content" 
            placeholder="영화에 대한 내용을 작성하세요"
          ></textarea>
        </div>

        <!-- 별점 -->
        <div class="star-rating">
          <span 
            v-for="star in 5" 
            :key="star" 
            @click="setRating(star)" 
            class="star" 
            :class="{ active: rating >= star }">
            ★
          </span>
        </div>

        <!-- 작성 완료 버튼 -->
        <button @click="submitReview" class="submit-button">작성 완료</button>
      </div>
    </div>

    <!-- 영화 기록 내용 보기 모달 -->
    <div v-if="showContentModal" class="modal-overlay" @click="closeContentModal">
      <div class="modal-content" @click.stop>
        <!-- 닫기 버튼 -->
        <button class="close-button" @click="closeContentModal">×</button>

        <!-- 영화 기록 내용 -->
        <h2>영화 기록</h2>
        <!-- 여러 개의 영화 기록을 나열 -->
        <div class="review-item" v-for="(review, index) in selectedReviews" :key="index">
          <!-- 영화 포스터 -->
          <div class="poster-container">
            <img
              v-if="review.poster_url"
              :src="`https://image.tmdb.org/t/p/w200${review.poster_url}`"
              alt="영화 포스터"
              class="movie-poster"
            />
            <div v-else class="no-poster">포스터 없음</div>
          </div>

          <!-- 영화 정보 -->
          <div class="review-info">
            <p><strong>영화 제목:</strong> {{ review.title }}</p>
            <p><strong>영화 내용:</strong> {{ review.content }}</p>
          <!-- 별점 표시 -->
          <div class="star-rating">
            <span 
              v-for="star in 5" 
              :key="star"
              class="star"
              :class="{ active: review.rating >= star }">
              ★
            </span>
          </div>
        </div>
          
          <!-- 구분선 (hr 태그 추가) -->
          <hr v-if="index < selectedReviews.length - 1" />
        </div>

        <!-- 추가 작성하기 버튼 -->
        <button @click="addNewReview" class="add-review-button">+</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';  // axios 임포트
import { useCalendarStore } from '@/stores/calendar';
import { useAccountStore } from '@/stores/account';
import bootstrapPlugin from '@fullcalendar/bootstrap';

// 리뷰 데이터 관리
const reviews = ref([]);

// 모달 상태 관리
const showModal = ref(false);
const showContentModal = ref(false);
const selectedDate = ref('');
const title = ref('');
const content = ref('');
const rating = ref(0);  // 별점 초기화 0으로 설정
const selectedReviews = ref([]); // 선택된 리뷰들 (배열로 저장)
const searchResults = ref([]); // 검색된 영화 목록
const selectedMovieId = ref(null); // 선택된 영화의 ID 저장

const store = useCalendarStore()
const accountStore = useAccountStore()
const apiKey = import.meta.env.VITE_TMDB_API_KEYS

const currentUser = accountStore.currentUser;

// 리뷰 개수 변화를 감지하고 부모로 전달
const emit = defineEmits(['update-reviews']);
watch(
  () => reviews.value.length,
  (newCount) => {
    emit('update-reviews', newCount);
  },
);


// 모달 열기
const openModal = (date) => {
  selectedDate.value = date; // 선택된 날짜 설정
  title.value = ""; // 제목 초기화
  content.value = ""; // 내용 초기화
  rating.value = 0; // 별점 초기화
  selectedMoviePoster.value = ""; // 포스터 초기화
  searchResults.value = []; // 검색 결과 초기화
  showModal.value = true; // 모달 열기
};

// 모달 닫기
const closeModal = () => {
  showModal.value = false;
};

// 영화 기록 내용 보기 모달 열기
const openContentModal = (date) => {
  // 해당 날짜에 작성된 영화 기록이 있으면 내용 모달 표시
  selectedReviews.value = store.reviews.filter(r => r.created_date === date);
  console.log('여기', selectedReviews.value)
  showContentModal.value = true;
};

// 영화 기록 내용 보기 모달 닫기
const closeContentModal = () => {
  showContentModal.value = false;
};

// 별점 설정 함수
const setRating = (star) => {
  rating.value = star;
};


// 작성 완료 함수 (Store 호출)
const submitReview = async () => {
  if (title.value && content.value && selectedMovieId.value) {
    try {
      const payload = {
        title: title.value,
        content: content.value,
        rating: rating.value,
        movie: selectedMovieId.value, // 영화 ID 추가
        poster_url: selectedMoviePoster.value ? `https://image.tmdb.org/t/p/w200${selectedMoviePoster.value}` : "", // 포스터 URL 추가
        created_date: selectedDate.value,
      };

      // Store의 submitReview 호출
      await store.submitReview(payload);

      // 이벤트 추가
      calendar.addEvent({
        title: payload.title,
        start: payload.created_date,
        description: `내용: ${payload.content}, 별점: ${payload.rating} ★`,
        extendedProps: {
          poster: payload.poster_url,
        },
      });

      // 초기화 및 모달 닫기
      title.value = '';
      content.value = '';
      rating.value = 0;
      selectedMovieId.value = null;
      selectedMoviePoster.value = '';
      searchResults.value = [];
      closeModal();
    } catch (error) {
      console.error('저장 실패:', error.message);
      alert('저장에 실패했습니다. 다시 시도해주세요.');
    }
  } else {
    alert('영화 제목과 내용을 입력하고 영화를 선택해 주세요.');
  }
};


// FullCalendar 설정
let calendar = null;

onMounted(async () => {
  const calendarEI = document.getElementById('calendar');
  
  // FullCalendar 초기화
  calendar = new FullCalendar.Calendar(calendarEI, {
    plugins: [bootstrapPlugin],
    themeSystem: 'bootstrap',
    headerToolbar: {
      left: 'prev today',
      center: 'title',
      right: 'next',
    },
    initialView: 'dayGridMonth',
    selectable: true,
    buttonText: {
      prev: '<i class="fas fa-chevron-left"></i>',
      next: '<i class="fas fa-chevron-right"></i>',
      today: 'Today',
    },
    customButtons: {
      today: {
        text: 'Today',
        click: function () {
          calendar.today();
        },
      },
      prev: {
        click: function () {
          calendar.prev();
        },
      },
      next: {
        click: function () {
          calendar.next();
        },
      },
    },
    eventBackgroundColor: 'transparent', // 이벤트 배경 투명하게 설정
    eventBorderColor: 'transparent',     // 이벤트 테두리 투명하게 설정
    events: [],  // 초기에는 빈 배열로 설정
    eventContent: (arg) => {
      const posterUrl = arg.event.extendedProps.poster || '';
      
      const truncatedTitle =
        arg.event.title.length > 4
          ? arg.event.title.substring(0, 4) + "..."
          : arg.event.title;

      return {
        html: `
          <div class="event-content">
            ${
              posterUrl
                ? `<img src="${posterUrl}" alt="Poster" class="event-poster" />`
                : `<div class="event-title">${truncatedTitle}</div>`
            }
          </div>
        `,
      };
    },
    dateClick: function (info) {
      selectedDate.value = info.dateStr;
      const review = store.reviews.filter(r => r.created_date === info.dateStr);
      console.log(review)
      if (review.length > 0) {
        openContentModal(info.dateStr);
      } else {
        openModal(info.dateStr);
      }
    },
  });
  
  // Calendar 렌더링
  calendar.render();

  // 데이터가 로딩된 후에 리뷰 데이터 가져오기
  await store.fetchReviews();  // 리뷰 데이터를 가져옵니다.
  
  console.log('Fetched Reviews:', store.reviews); // 데이터 확인

  // 데이터가 로딩된 후에 events 업데이트
  calendar.addEventSource({
    events: store.reviews.map(review => ({
      title: review.title,
      start: review.created_date,
      description: `내용: ${review.content}, 별점: ${review.rating} ★`,
      extendedProps: {
        poster: review.poster_url,
      },
    })),
  });
});

// 새로운 영화 기록 작성하기
const addNewReview = () => {
  closeContentModal();  // 기록 내용 모달 닫기
  openModal(selectedDate.value);  // 새로운 작성 모달 열기
};

// 상태 변수
const selectedMoviePoster = ref(""); // 선택된 영화의 포스터

// 영화 검색 함수 (TMDB API)
const searchMovies = async () => {
  if (title.value.trim().length > 1) {
    try {
      const response = await axios.get(`https://api.themoviedb.org/3/search/movie`, {
        params: {
          api_key: apiKey,
          query: title.value,
          language: "ko-KR",
        },
      });
      console.log("검색된 영화 목록:", response.data.results); // 검색 결과 확인
      searchResults.value = response.data.results;
    } catch (error) {
      console.error("영화 검색에 실패했습니다:", error);
      searchResults.value = [];
    }
  } else {
    searchResults.value = [];
  }
};

// 영화 선택 시 제목 및 포스터 설정
const selectMovie = (movie) => {
  title.value = movie.title; // 제목 설정
  selectedMoviePoster.value = movie.poster_path || ""; // 포스터 설정
  selectedMovieId.value = movie.id; // 선택한 영화 ID 저장
  searchResults.value = []; // 검색 결과 숨김
};

</script>



<style>
.fc-toolbar {
  display: flex;
  justify-content: space-between; /* 좌/우 정렬 */
  align-items: center;
}

.fc-toolbar-chunk {
  display: flex;
  align-items: center;
}

.fc-toolbar-chunk:first-child {
  justify-content: flex-start; /* 왼쪽 정렬 */
}

.fc-toolbar-chunk:last-child {
  justify-content: flex-end; /* 오른쪽 정렬 */
}

.fc-today-button {
  margin: 0 10px; /* 여유 공간 추가 */
  background-color: #2AA971 !important;
  border: none !important;
  color: white !important;
  border-radius: 8px;
  width: 80px;
  height: 40px;
}

/* FullCalendar Bootstrap prev/next 버튼 색상 수정 */
.fc-prev-button, .fc-next-button {
  background-color: #2AA971 !important; /* 녹색 배경 */
  border: none !important; /* 테두리 제거 */
  color: white !important; /* 화이트 글자/아이콘 */
  border-radius: 50% !important; /* 동그란 모양 */
  width: 40px; /* 버튼 크기 */
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.fc-prev-button:hover, .fc-next-button:hover, .fc-today-button:hover {
  background-color: #229A5F !important; /* 호버 시 어두운 녹색 */
  color: #ffffff !important; /* 화이트 글자/아이콘 유지 */
}


/* 가운데 제목 스타일 */
.fc-toolbar-title {
  font-family: 'Caveat', cursive; /* 필기체 폰트 */
  font-size: 24px;
  font-weight: bold;
  color: #000000;
  text-align: center;
  /* text-justify: center; */
}

/* 달력 테두리(줄) 제거 */
.fc-daygrid-day, .fc-col-header-cell {
  border: none !important;
}

/* 요일 텍스트 스타일 변경 */
.fc-col-header-cell {
  font-family: 'Inter', sans-serif; /* 요일에 사용할 폰트 */
  font-weight: 500 !important; /* Medium (500) 폰트 설정 */
  font-size: 14px; /* 적당한 크기로 조정 */
  color: #333; /* 기본 텍스트 색상 */
  text-transform: capitalize; /* 첫 글자 대문자로 표시 (선택 사항) */
}

/* 일반 날짜 스타일 (폰트 변경) */
.fc-daygrid-day-number {
  font-family: 'Inter', sans-serif;
  font-weight: 400; /* Regular 폰트 */
  font-size: 14px;
  color: #555; /* 기본 텍스트 색상 */
}

/* 오늘 날짜 배경 색상 제거 및 강조 */
.fc-day-today {
  background-color: transparent !important; /* 오늘 날짜 배경 제거 */
  color: #2AA971; /* 강조된 색상 */
  font-weight: 600; /* 살짝 강조 */
}

/* 선택한 날짜 강조 */
.fc-daygrid-day.fc-daygrid-day-selected {
  background-color: rgba(42, 169, 113, 0.1); /* 옅은 녹색 배경 */
}


/* 모달 배경 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

/* 모달 창 */
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  position: relative;
  width: 90vw;
  height: 80vh;
  max-width: 800px;
  max-height: 600px;
  overflow: auto;
}

/* 닫기 버튼 */
.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 40px;
  font-weight: bold;
  color: #333;
  cursor: pointer;
}

.close-button:hover {
  color: #2AA971;
}

/* Form group */
.form-group {
  margin-bottom: 20px;
  width: 100%;
}

.form-group label {
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 16px;
  color: #000000;
}

/* 영화 제목(input) 폼 크기 수정 */
.form-group input {
  width: 100%;
  padding: 12px;
  margin-top: 8px;
  border: 1px solid #E0E0E0;
  border-radius: 8px;
  font-size: 14px;
  max-width: 100%; /* 100%로 너비 설정 */
  box-sizing: border-box;
}

/* 영화 내용(textarea) 폼 크기 수정 및 고정 */
.form-group textarea {
  width: 100%;
  padding: 12px;
  margin-top: 8px;
  border: 1px solid #E0E0E0;
  border-radius: 8px;
  font-size: 14px;
  max-width: 100%; /* 100%로 너비 설정 */
  height: 150px;    /* 높이 설정 */
  box-sizing: border-box;
  resize: none;     /* 사용자 크기 조정 비활성화 */
  overflow-y: auto; /* 내용이 길어지면 스크롤 */
}

/* 검색 결과 */
.search-results {
  list-style: none;
  padding: 0;
  margin-top: 5px;
  border-top: 1px solid #E0E0E0;
  max-height: 200px;
  overflow-y: auto;
}

.search-results li {
  padding: 8px;
  cursor: pointer;
}

.search-results li:hover {
  background-color: #F0F0F0;
}

/* 영화 내용(textarea) 폼 크기 수정 및 고정 */
.form-group textarea {
  width: 100%;
  padding: 12px;
  margin-top: 8px;
  border: 1px solid #E0E0E0;
  border-radius: 8px;
  font-size: 14px;
  max-width: 100%; /* 100%로 너비 설정 */
  height: 150px;    /* 높이 설정 */
  box-sizing: border-box;
  resize: none;     /* 사용자 크기 조정 비활성화 */
  overflow-y: auto; /* 내용이 길어지면 스크롤 */
}

/* Star rating */
.star-rating {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

.star {
  font-size: 30px;
  cursor: pointer;
  color: #D9D9D9;
}

.star.active {
  color: #2AA971;
}

/* Submit button */
.submit-button {
  width: 100%;
  padding: 12px;
  background: #2AA971;
  border-radius: 60px;
  font-family: 'Poppins', sans-serif;
  font-weight: 600;
  font-size: 16px;
  color: #FFFFFF;
  border: none;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #229A5F;
}

/* 영화 입력 컨테이너 */
.movie-input-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* 선택된 영화 포스터 */
.selected-poster img {
  width: 120px;
  height: 180px;
  border-radius: 5px;
  object-fit: cover;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 영화 기록 내용 */
.review-item {
  display: flex;
  align-items: center; /* 수직 중앙 정렬 */
  margin-bottom: 20px; /* 간격 */
}

/* 영화 포스터 */
.poster-container {
  width: 100px; /* 포스터의 너비 */
  height: 150px; /* 포스터의 높이 */
  margin-right: 20px; /* 이미지와 텍스트 사이의 간격 */
}

/* 영화 포스터 이미지 */
.movie-poster {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 비율 유지하며 꽉 채우기 */
  border-radius: 5px;
}

/* 포스터가 없을 때 */
.no-poster {
  width: 100%;
  height: 100%;
  background-color: #e0e0e0;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #777;
  border-radius: 5px;
}

/* 영화 정보 (제목, 내용, 별점) */
.review-info {
  flex: 1; /* 나머지 공간을 차지 */
  text-align: left; /* 텍스트 왼쪽 정렬 */
}

.review-info p {
  margin: 5px 0;
}

.star-rating {
  display: flex;
  margin-top: 10px;
}


/* 모달 창 내에서 추가 작성하기 버튼을 오른쪽 아래에 고정 */
.modal-content {
  position: relative; /* 모달을 기준으로 위치 설정 */
  background: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  width: 90vw;
  height: 80vh;
  max-width: 800px;
  max-height: 600px;
  overflow: auto; /* 스크롤 가능하게 설정 */
}

/* 추가 작성하기 버튼 */
.add-review-button {
  position: absolute; /* 모달 창 내에서 고정 위치 설정 */
  bottom: 20px;         /* 모달 창 하단에서 20px */
  right: 20px;          /* 모달 창 오른쪽에서 20px */
  width: 50px;          /* 버튼 크기 */
  height: 50px;         /* 버튼 크기 */
  background-color: #2AA971; /* 버튼 색상 */
  color: white;         /* 글씨 색상 */
  border-radius: 50%;   /* 동그란 모양 */
  font-size: 30px;      /* + 기호 크기 */
  display: flex;        /* Flexbox로 중앙 정렬 */
  justify-content: center; /* 수평 중앙 정렬 */
  align-items: center;  /* 수직 중앙 정렬 */
  border: none;         /* 테두리 제거 */
  cursor: pointer;      /* 커서 포인터로 변경 */
  z-index: 2000;        /* 모달보다 위에 표시되도록 설정 */
}

.add-review-button:hover {
  background-color: #229A5F; /* 버튼 호버 시 색상 */
}

.event-poster {
  width: 100%; /* 셀 전체를 채우도록 */
  height: 100%;
  object-fit: cover;
  border-radius: 5px; /* 모서리를 둥글게 */
}

.event-content {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden; /* 내용이 넘치지 않도록 */
}

.event-title {
  font-size: 14px;
  font-weight: bold;
  color: #333;
  text-align: center;
  padding: 10px;
  word-wrap: break-word; /* 긴 제목 줄바꿈 처리 */
  background-color: #f0f0f0; /* 배경색 설정 */
  border-radius: 5px; /* 모서리 둥글게 */
  height: 100%; /* 칸 전체를 채우도록 설정 */
  display: flex; /* 중앙 정렬을 위해 flex 사용 */
  justify-content: center; /* 수평 중앙 정렬 */
  align-items: center; /* 수직 중앙 정렬 */
  overflow: hidden; /* 내용이 넘칠 경우 숨김 */
  text-overflow: ellipsis; /* 긴 제목은 줄임표(...) 처리 */
  white-space: nowrap; /* 한 줄로 유지 */
  box-sizing: border-box; /* 패딩 포함 크기 계산 */
}

/* 날짜 셀에 상대 위치 설정 */
.fc-daygrid-day {
  position: relative !important;
}

/* 기존 이벤트 점 숨기기 */
.fc-daygrid-event-dot {
  display: none !important;
}

/* 이벤트 텍스트 숨기기 */
.fc-event-title {
  display: none !important;
}

/* 이벤트 시간 숨기기 */
.fc-event-time {
  display: none !important;
}
</style>

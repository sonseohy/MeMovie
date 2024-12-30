<template>
  <!-- 검색 섹션 -->
  <!-- <div class="search-section">
    <label for="search-input">게시글 검색하기:</label>
    <input
      id="search-input"
      type="text"
      class="search-input"
      placeholder="검색어를 입력하세요."
    />
    <button class="search-btn">입력</button>
  </div> -->
  <!-- <hr> -->
  <div class="commu-box">
    <!-- 게시글 목록 -->
    <div v-if="filteredArticles.length > 0" v-for="article in filteredArticles" :key="article.id" class="post">
      <ArticleListItem :article="article" :filter="filter" />
    </div>

    <!-- '내 활동'에서 게시글이 없을 경우 문구 표시 -->
    <div v-else>
      <p v-if="filter && filteredArticles.length === 0">아직 작성한 글이 없습니다.</p>
    </div>
    <!-- 페이지네이션 -->
    <div>
      <span>&lt; 1 / 2 &gt;</span>
    </div>
</div>
</template>

<script setup>
import ArticleListItem from '@/components/ArticleListItem.vue'
import { useArticleStore } from '@/stores/article'
import { defineProps, computed } from 'vue'

const store = useArticleStore()

// 'filter' prop을 받아 전달
const props = defineProps({
  filter: {
    type: String,
    required: false,
    default: '',
  }
})

// 필터링된 게시글 목록
const filteredArticles = computed(() => {
  // store.articles가 비어있는 경우, 빈 배열 반환
  const articles = store.articles || []

  if (!props.filter) {
    return articles // 필터가 없다면 전체 게시글 반환
  }
  
  // 'filter' 값이 작성자의 이름과 일치하는 게시글만 반환
  return articles.filter(article => article.author.username === props.filter)
})
</script>

<style scoped>

/* 커뮤니티 박스 */
.commu-box {
flex: 3;
background: white;
border-radius: 10px;
box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
padding: 20px;
}

/* 검색 섹션 */
.search-section {
display: flex;
align-items: center;
/* margin-bottom: 20px; */
padding: 0 50px;
} 

.search-section label {
font-size: 16px;
margin-right: 10px;
}

.search-input {
flex: 1;
padding: 8px 12px;
border: 1px solid #ddd;
border-radius: 5px;
font-size: 14px;
margin-right: 10px;
}

.search-btn {
padding: 8px 15px;
background-color: #2AA971;
color: white;
border: none;
border-radius: 5px;
cursor: pointer;
}

.search-btn:hover {
background-color: #1d8d5a;
}

/* 게시글 */
.post {
margin-bottom: 20px;
/* border-bottom: 1px solid #ddd; */
padding-bottom: 15px;
}

.post h3 {
font-size: 20px;
color: #2AA971;
margin-bottom: 10px;
}

.post p {
font-size: 16px;
line-height: 1.5;
margin-bottom: 10px;
}

.post-meta {
font-size: 14px;
color: #888;
display: flex;
justify-content: space-between;
}

/* '내 활동'에서 글이 없을 경우 문구 스타일 */
p {
  text-align: center;
  font-size: 18px;
  color: #888;
  margin-top: 20px;
}

</style>
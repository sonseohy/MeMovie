import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import router from '@/router'
import axios from 'axios'
import { useAccountStore } from '@/stores/account'

export const useArticleStore = defineStore('article', () => {
  const BASE_URL = 'http://127.0.0.1:8000'
  const articles = ref([])

  const accountStore = useAccountStore()

  // DRF로 전체 게시글 요청을 보내고 응답을 받아 articles에 저장하는 함수
  const getArticles = function () {
    axios({
      method: 'get',
      url: `${BASE_URL}/api/articles/`,
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
      .then((res) => {
        // console.log(res.data)
        articles.value = res.data
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // DRF로 게시글 생성 요청을 보내는 함수
  const createArticle = function (payload) {
    axios({
      method: 'post',
      url: `${BASE_URL}/api/articles/`,
      headers: {
        Authorization: `Token ${accountStore.token}`, // 인증 토큰 추가
      },
      data: {
        title: payload.title,
        content: payload.content
      }
    })
      .then((response) => {
        // console.log('게시글 작성 성공')
        router.push({ name: 'ArticleList' })
      })
      .catch((error) => {
        console.error('게시글 작성 실패:', error.response.data)
      })
  }

  // 게시글 삭제 함수
  const deleteArticle = function (articleId) {
    const confirmation = confirm("정말로 이 게시글을 삭제하시겠습니까?")
    if (!confirmation) return

    axios({
      method: 'delete',
      url: `${BASE_URL}/api/articles/${articleId}/`,
      headers: {
        Authorization: `Token ${accountStore.token}`, // 인증 토큰 추가
      },
    })
      .then(() => {
        alert("게시글이 삭제되었습니다.")
        router.push({ name: 'ArticleList' })  // 게시글 목록 페이지로 이동
      })
      .catch((err) => {
        if (err.response && err.response.status === 403) {
          // 권한이 없으면 경고 메시지 표시
          alert("이 게시글을 삭제할 권한이 없습니다.");
        } else {
          alert("게시글 삭제에 실패했습니다.");
          console.error('게시글 삭제 실패:', err.response.data)
        }
      })
  }

  // 게시글 수정 함수
  const updateArticle = function(articleId, payload) {
    console.log('토큰:', accountStore.token);
    axios({
      method: 'put',
      url: `${BASE_URL}/api/articles/${articleId}/`,
      headers: {
        Authorization: `Token ${accountStore.token}`, // 인증 토큰 추가
      },
      data: payload
    })
      .then((response) => {
        // 수정 완료 후 해당 게시글 상세 페이지로 이동
        // 수정된 게시글의 ID를 사용하여 상세 페이지로 이동
        router.push({ name: 'ArticleDetail', params: { id: articleId } })
      })
      .catch((error) => {
        if (error.response && error.response.status === 403) {
          alert("이 게시글을 수정할 권한이 없습니다.");
        } else {
          alert("게시글 수정에 실패했습니다.");
          console.error('게시글 수정 실패:', error.response.data)
        }
      })
  }


  return {
    BASE_URL,
    getArticles,
    createArticle,
    deleteArticle,
    updateArticle,
    articles,
  }
})
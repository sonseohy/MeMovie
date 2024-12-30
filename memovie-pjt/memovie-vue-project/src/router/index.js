import { createRouter, createWebHistory } from 'vue-router'
import MainView from '@/views/MainView.vue'
import MovieListView from '@/views/MovieListView.vue'
import ArticleListView from '@/views/Article/ArticleListView.vue'
import LogInView from '@/views/auth/LogInView.vue'
import SignUpView from '@/views/auth/SignUpView.vue'
import PasswordResetView from '@/views/auth/PasswordResetView.vue'
import SettingView from '@/views/auth/SettingView.vue'

import { useAccountStore } from '@/stores/account'
import MyPageView from '@/views/MyPageView.vue'
import ArticleCreateView from '@/views/Article/ArticleCreateView.vue'
import ArticleDetailView from '@/views/Article/ArticleDetailView.vue'
import ArticleUpdateView from '@/views/Article/ArticleUpdateView.vue'
import MovieDetailView from '@/views/MovieDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // 메인페이지
    {
      path: '/',
      name: 'Main',
      component: MainView
    },
    // 영화 추천 관련
    {
      path: '/movies',
      name: 'MovieList',
      component: MovieListView
    },
    // 영화 상세 정보 페이지
    {
      path: '/movie/:id',
      name: 'MovieDetail',
      component: MovieDetailView
    },
    // 회원가입 및 로그인 관련
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'LogInView',
      component: LogInView
    },
    {
      path: '/password/reset',
      name: 'PasswordResetView',
      component: PasswordResetView
    },
    // 게시글 전체 조회
    {
      path: '/community',
      name: 'ArticleList',
      component: ArticleListView
    },
    // 게시글 생성
    {
      path: '/community/create',
      name: 'ArticleCreate',
      component: ArticleCreateView
    },
    // 게시글 상세
    {
      path: '/community/:id',
      name: 'ArticleDetail',
      component: ArticleDetailView
    },
    // 게시글 수정
    {
      path: '/community/:id/edit',
      name: 'ArticleUpdate',
      component: ArticleUpdateView
    },
    // 마이 페이지 및 기록 관련
    {
      path: '/mypage',
      name: 'Mypage',
      component: MyPageView,
    },
    {
      path: '/Setting',
      name: 'Setting',
      component: SettingView,
    },
  ],
})

router.beforeEach((to, from) => {
  const store = useAccountStore()

  // 만약 이동하는 목적지가 커뮤니티 페이지면서 현재 로그인 상태가 아니라면 로그인 페이지로 보냄
  if (to.name === 'CommunityList' && !store.isLogin) {
    window.alert('로그인이 필요합니다.')
    return { name: 'LogInView' }
  }

   // 만약 이동하는 목적지가 먼슬리 무비 페이지면서 현재 로그인 상태가 아니라면 로그인 페이지로 보냄
  if (to.name === 'Mypage' && !store.isLogin) {
    window.alert('로그인이 필요합니다.')
    return { name: 'LogInView' }
  }

  // 만약 로그인 사용자가 회원가입 또는 로그인 페이지로 이동하려고 하면 메인 페이지로 보냄
  if ((to.name === 'SignUpView' || to.name === 'LogInView') && (store.isLogin)) {
    window.alert('이미 로그인 되어있습니다.')
    return { name: 'Main'}
  }
})

export default router

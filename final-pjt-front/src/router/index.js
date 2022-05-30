import Vue from 'vue'
import VueRouter from 'vue-router'

// 메인 페이지(movies)
import HomeView from '@/views/Movies/HomeView'

// 프로필, 로그인(account)
import LoginFormView from '@/views/Accounts/LoginFormView'
import ProfilePage from '@/views/Profile/ProfilePage'
import PersonalProfileEdit from '@/views/Profile/PersonalProfileEdit'
import PasswordChange from '@/views/Profile/PasswordChange'
import PasswordFind from '@/views/Profile/PasswordFind'
import PersonalProfile from '@/views/Profile/PersonalProfile'

// 리뷰, 댓글(community)
import CommunityView from '@/views/Community/CommunityView'
import ReviewNewView from '@/views/Community/ReviewNewView'
import ReviewDetailView from '@/views/Community/ReviewDetailView.vue'
import ReviewEditView from '@/views/Community/ReviewEditView'

// 에러 페이지
import NotFound404 from '@/components/Accounts/NotFound404.vue'

// 어드민 페이지
import AdminPage from '@/views/Admin/AdminPage.vue'
import MovieCreation from '@/views/Admin/MovieCreation.vue'


Vue.use(VueRouter)

const routes = [
  // 메인 홈
  {
    path: '/',
    name: 'HomeView',
    component: HomeView
  },
  // 어드민 페이지(테스트 중)
  {
    path: '/adminpage',
    name: 'AdminPage',
    component: AdminPage
  },
  // 자기자신 프로필
  {
    path: '/profile',
    name: 'ProfilePage',
    component: ProfilePage
  },
  // 프로필 수정
  {
    path: '/profile/edit',
    name: 'PersonalProfileEdit',
    component: PersonalProfileEdit
  },
  // 상대방 프로필
  {
    path: '/profile/:userId',
    name: 'PersonalProfile',
    component: PersonalProfile
  },
  // 비밀번호 변경
  {
    path: '/password/change',
    name: 'PasswordChange',
    component: PasswordChange
  },
  // 비밀번호 찾기
  {
    path: '/password/find',
    name: 'PasswordFind',
    component: PasswordFind
  },
  // 로그인
  {
    path: '/login',
    name: 'LoginFormView',
    component: LoginFormView
  },
  // 커뮤니티 메인(전체 게시글 조회)
  {
    path: '/community',
    name: 'CommunityView',
    component: CommunityView
  },
  // 게시글 생성
  {
    path: '/new',
    name: 'reviewNew',
    component: ReviewNewView
  },
  // 개별 게시글 조회
  {
    path: '/reviews/:reviewId',
    name: 'review',
    component: ReviewDetailView
  },
  // 개별 게시글 수정
  {
    path: '/reviews/:reviewId/edit',
    name: 'reviewEdit',
    component: ReviewEditView
  },
  // 영화 생성
  {
    path: '/moviecreation',
    name: 'MovieCreation',
    component: MovieCreation
  },
  // 404 Not Found Error
  {
    path: '/errors/404NotFound',
    name: 'NotFound404',
    component: NotFound404
  },
  // 404 redirect
  {
    path: '*',
    redirect: '/errors/404NotFound'
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router

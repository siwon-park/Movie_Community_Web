import router from '@/router'
import axios from 'axios'
import drf from '@/api/drf'

export default {
  // namespaced: true,
  // 모든 state는 직접 접근하지 않고 getters를 통해서만 접근
  state: {
    token: localStorage.getItem('token') || '', // 토큰이 있으면 가져오고 아니면 ''
    currentUser: {},
    profile: {},
    authError: null,
    movieList: {},
    hateGenres: {},
    followers: {},
    recommendFriends: {},
    likeRecommendMovies: {},
    rateRecommendMovies: {},
  },

  getters: {
    isLoggedIn: state => !!state.token,
    currentUser: state => state.currentUser,
    profile: state => state.profile,
    authError: state => state.authError,
    authHeader: state => ({ Authorization: `Token ${state.token}` }),
    movieList: state => state.movieList,
    hateGenres: state => state.hateGenres,
    followers: state => state.followers,
    recommendFriends: state => state.recommendFriends,
    likeRecommendMovies: state => state.likeRecommendMovies,
    rateRecommendMovies: state => state.rateRecommendMovies,
  },

  mutations: {
    SET_TOKEN: (state, token) => state.token = token,
    SET_CURRENT_USER: (state, user) => state.currentUser = user,
    SET_PROFILE: (state, profile) => state.profile = profile,
    SET_AUTH_ERROR: (state, error) => state.authError = error,
    FETCH_PERONAL_MOVIELIST: (state, movie_list) => state.movieList = movie_list,
    FETCH_HATE_GENRE: (state, hate_genres) => state.hateGenres = hate_genres,
    FOLLOW_USER: (state, follow_user) => state.followers = follow_user,
    FETCH_RECOMMEND_FRIEND: (state, recommend_friends) => state.recommendFriends = recommend_friends,
    FETCH_LIKE_RECOMMEND_MOVIES: (state, like_recommend_movies) => state.likeRecommendMovies = like_recommend_movies,
    FETCH_RATE_RECOMMEND_MOVIES: (state, rate_recommend_movies) => state.rateRecommendMovies = rate_recommend_movies,
  },

  actions: {
    // state.token 추가 
    saveToken({ commit }, token) {
      commit('SET_TOKEN', token)
      localStorage.setItem('token', token) // localStorage에 token 추가
    },

    // state.token 삭제
    removeToken({ commit }) {
      commit('SET_TOKEN', '')
      localStorage.setItem('token', '') // localStorage에 token 추가
    },

    // 로그인
    login({ commit, dispatch }, credentials) {
      axios({
        url: drf.accounts.login(),
        method: 'post',
        data: credentials,
      })
      .then(res => {  // 로그인 성공 시 응답 토큰 저장/사용자 정보 받기
        const token = res.data.key
        dispatch('saveToken', token)
        dispatch('fetchCurrentUser')
        router.push({ name: 'HomeView' }) // 홈으로 이동
      })
      .catch(err => { // 실패하면 에러 정보를 저장
        console.error(err.response.data)
        commit('SET_AUTH_ERROR', err.response.data)
      })
    },

    // 회원가입
    signup({ commit, dispatch }, credentials) {
      axios({
        url: drf.accounts.signup(),
        method: 'post',
        data: credentials,
      })
      .then(res => { // 성공하면 응답 토큰 저장/현재사용자 정보 받기
        const token = res.data.key
        dispatch('saveToken', token)
        dispatch('fetchCurrentUser')
        router.push({ name: 'HomeView' }) // 홈으로 이동
      })
      .catch(err => {  // 실패하면 에러 정보를 저장
        console.error(err.response.data)
        commit('SET_AUTH_ERROR', err.response.data)
      })
    },

    // 로그 아웃
    logout({ getters, dispatch }) {
      axios({
        url: drf.accounts.logout(),
        method: 'post',
        headers: getters.authHeader,
      })
      .then(() => { // 성공하면 토큰 삭제/사용자 알람
        dispatch('removeToken')
        alert('성공적으로 로그아웃되셨습니다')
        localStorage.removeItem('vuex') // 로그아웃 시 vuex 저장정보 삭제
        router.push({ name: 'LoginFormView' }) // 로그인 페이지로 이동
      })
      .catch(err => {
        console.error(err.response)
      })
    },
    
    // 회원탈퇴
    signout({getters}) {
      if (confirm('정말 탈퇴하시겠습니까?')){
        axios({
          url: drf.accounts.deletemember(),
          method: 'post',
          headers: getters.authHeader,
        })
        .then(() => {
          localStorage.removeItem('vuex')
          alert('성공적으로 회원탈퇴 처리되었습니다.')
          router.push({ name: 'LoginFormView' })
        })
        .catch(err => {
          console.error(err.response)
        })
      }
    },

    // 현재 사용자 정보 가져오기 / 프로필 조회(GET)
    fetchCurrentUser({ commit, getters, dispatch }) {
      if (getters.isLoggedIn) {
        axios({
          url: drf.accounts.currentUserInfo(),
          method: 'get',
          headers: getters.authHeader,
        }) // 올바른 토큰이면 사용자 정보를 가져오기
        .then(res => commit('SET_CURRENT_USER', res.data)) // 정보 저장
        .catch(err => { // 아니라면 기존 토큰을 삭제하고 로그인 페이지로 이동
          if (err.response.status === 401) {
            dispatch('removeToken')
            router.push({ name: 'LoginFormView' })
          } 
        })
      } else {
        alert('로그인이 필요한 서비스입니다')
        router.push({ name: 'LoginFormView' })
      }
    },

    // 다른 유저 프로필 가져오기
    fetchProfile({ commit, getters }, userId ) {
      axios({
        url: drf.accounts.profile(userId),
        method: 'get',
        headers: getters.authHeader,
      })
        .then(res => {
          commit('SET_PROFILE', res.data)
        })
        .catch(err => {
          if (err.response.status === 404) {
            router.push({ name: 'NotFound404' })
          }
        })
    },

    // 프로필 정보 수정(put)
    updateProfile({ commit, getters }, {username, sex, region}) {
      const userdata = {
        username: username,
        sex: sex,
        region: region,
      } 
      if (getters.isLoggedIn) {
        axios({
          url: drf.accounts.currentUserInfo(),
          method: 'put',
          data: userdata,
          headers: getters.authHeader,
        })
        .then(res => {
          commit('SET_CURRENT_USER', res.data)
          router.push({ name: 'ProfilePage' }) // 프로필 페이지로 이동
        })
        .catch(err => {
          console.error(err)
        })
      }
    },

    // // 비밀번호 변경
    changePassword({ commit, getters }, {password1, password2}) {
      const passwordData =  {
        new_password1: password1,
        new_password2: password2,
      }
      if (getters.isLoggedIn) {
        axios({
          url: drf.accounts.changepassword(),
          method: 'post',
          data: passwordData,
          headers: getters.authHeader,
        })
        .then(res => {
          commit('SET_CURRENT_USER', res.data)
          router.push({ name: 'ProfilePage' }) // 프로필 페이지로 이동
        })
        .catch(err => {
          console.error(err)
        })
      }
    },

    // 비밀번호 찾기 사전 확인
    findPassword({commit}, {e_mail}) {
      axios({
        url: "http://localhost:8000/account/password/reset/",
        method: 'post',
        data: {email: e_mail},
      })
      .then(() =>{
        alert('가입하신 메일주소로 비밀번호 변경 url을 발송하였습니다.')
        commit()
        router.push({ name: 'LoginFormView' })
      })
      .catch(err => {
        console.error(err.response)
      })
    },

    // 개인 영화 정보 받아오기
    fetchPersonalMovieList({ commit, getters }, userId) {
      axios({
        url: drf.accounts.personalmovielist(userId),
        method: 'get',
        headers: getters.authHeader,
      })
      .then(res => {
        commit('FETCH_PERONAL_MOVIELIST', res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },

    // 싫어하는 장르 조회
    fetchHateGenre({commit, getters}, userId) {
      axios({
        url: drf.accounts.personalhatemovie(userId),
        method: 'get',
        headers: getters.authHeader,
      })
      .then(res => {
        commit("FETCH_HATE_GENRE", res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },

    // 싫어하는 장르 체크/해제
    hateGenresPick({commit, getters}, {userId, genreId}) {
      axios({
        url: drf.accounts.personalhatemovieupdate(userId, genreId),
        method: 'post',
        headers: getters.authHeader,
      })
      .then(res => {
        commit("FETCH_HATE_GENRE", res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },

    // 유저 팔로우(userId는 현재 유저가 X)
    followUser({ commit, getters }, userId) {
      axios({
        url: drf.accounts.personalfollow(userId),
        method: 'post',
        headers: getters.authHeader,
      })
      .then(res =>{
        commit("FOLLOW_USER", res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },
    
    // 추천 친구 조회
    fetchRecommendFriend({ commit, getters }, userId) {
      axios({
        url: drf.accounts.friendreco(userId),
        method: 'get',
        headers: getters.authHeader,
      })
      .then(res => {
        commit("FETCH_RECOMMEND_FRIEND", res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },

    // 좋아요 기반 영화 추천
    fetchLikeRecommendMovies({ commit, getters }, userId) {
      axios({
        url: drf.accounts.recolike(userId),
        method: 'get',
        headers: getters.authHeader,
      })
      .then(res => {
        commit("FETCH_LIKE_RECOMMEND_MOVIES", res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },

    // 평점 기반 영화 추천
    fetchRateRecommendMovies({ commit, getters }, userId) {
      axios({
        url: drf.accounts.recorate(userId),
        method: 'get',
        headers: getters.authHeader,
      })
      .then(res => {
        commit("FETCH_RATE_RECOMMEND_MOVIES", res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },

  }
}

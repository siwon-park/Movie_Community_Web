import axios from 'axios'
import drf from '@/api/drf'

export default {
  state: {
    mainMovies: {},
    subMovies: {},
    movieReivews: {},
    recommendMovies: [],
    movieRate: {},
    movieLike: {
      like_movie_users: [],
    },
    movieDetail: {},
    movieWish: {},
    customMovie: {},
    rateList: {},
  },

  getters: {
    mainMovies(state) {
      return state.mainMovies
    },
    subMovies(state) {
      return state.subMovies
    },
    movieReivews(state) {
      return state.movieReivews
    },
    recommendMovies(state) {
      return state.recommendMovies
    },
    movieRate(state) {
      return state.movieRate
    },
    movieLike(state) {
      return state.movieLike
    },
    movieDetail(state) {
      return state.movieDetail
    },
    movieWish(state) {
      return state.movieWish
    },
    customMovie(state) {
      return state.customMovie
    },
    rateList(state) {
      return state.rateList
    }
  },

  mutations: {
    MAIN_MOVIE_LOAD(state, main_data) {
      state.mainMovies = main_data
    },
    SUB_MOVIE_LOAD(state, sub_data) {
      state.subMovies = sub_data
    },
    MOVIE_REVIEW_LOAD(state, review_data) {
      state.movieReivews = review_data
    },
    RECOMMEND_MOVIE_LOAD(state, recommend_data) {
      state.recommendMovies = recommend_data
    },
    RATE_MOVIE(state, rate_data) {
      state.movieRate = rate_data
    },
    RERATE_MOVIE(state, rerate_data){
      state.movieRate = rerate_data
    },
    LIKE_MOVIE(state, like_data) {
      state.movieLike = like_data
    },
    MOVIE_DETAIL(state, movieDetail) {
      state.movieDetail = movieDetail
    },
    WISH_MOVIE(state, movieWish) {
      state.movieWish = movieWish
    },
    SET_MOVIE(state, movieData) {
      state.customMovie = movieData
    },
    FETCH_RATE(state, rateList) {
      state.rateList = rateList
    }
  },

  actions: {
    // 메인 페이지 상단 영화 조회 요청
    main_movie_load({ commit }) {
      axios({
        url: drf.movies.movies_main(),
        method: 'get',
      })
      .then(res => {
        commit('MAIN_MOVIE_LOAD', res.data)
      })
      .catch(err => {
        console.err(err)
      })
    },

    // 하단 영화 조회
    sub_movie_load({ commit }, sort_num) {
        axios({
          url: drf.movies.movies_sub(sort_num),
          method: 'get',
        })
        .then(res => {
          commit('SUB_MOVIE_LOAD', res.data)
        })
        .catch(err => {
          console.err(err)
        })
    },

    // 영화별 리뷰 게시글 조회
    fetchMovieReviews({commit}, movieId) {
      axios({
        url: drf.movies.movie_reviews(movieId),
        method: 'get',
      })
      .then(res => {
        commit('MOVIE_REVIEW_LOAD', res.data)
      })
      .catch(err => {
        console.err(err)
      })
    },

    // 추천 영화 조회
    fetchRecommendMovie({ commit }, genreId) {
      axios({
        url: drf.movies.movie_recommend(genreId),
        method: 'get',
      })
      .then(res => {
        commit('RECOMMEND_MOVIE_LOAD', res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },

    // 영화 상세 정보 조회
    fetchMovieDetail({ commit }, movieId) {
      axios({
        url: drf.movies.movie_detail(movieId),
        method: 'get',
      })
      .then(res => {
        commit('MOVIE_DETAIL', res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },

    // 영화 평점 조회
    fetchRate({ commit }, userId) {
      axios({
        url: drf.movies.movie_rate_list(userId),
        method: 'get',
        headers: { Authorization: `Token ${localStorage.getItem('token')}` },
      })
      .then(res => {
        commit("FETCH_RATE", res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },

    // 영화 평점 입력(로그인한 유저만)
    rateMovie({ commit }, {movieId, rate_score}) {
      const rating = {
        rate_score: rate_score,
      }
      // console.log(`Token ${localStorage.getItem('token')}`)
      axios({
        url: drf.movies.movie_rate(movieId),
        method: 'post',
        data: rating,
        headers: { Authorization: `Token ${localStorage.getItem('token')}` },
      })
      .then(res => {
        commit("RATE_MOVIE", res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },

    // 영화 평점 수정/삭제
    reRateMovie({ commit }, { movieId, rateId, rate_score }) {
      const rating = {
        rate_score: rate_score,
      }
      axios({
        url: drf.movies.movie_rate_update(movieId, rateId),
        method: 'put',
        data: rating,
        headers: { Authorization: `Token ${localStorage.getItem('token')}` },
      })
      .then(res => {
        commit("RERATE_MOVIE", res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },

    // 영화 좋아요
    likeMovie({ commit }, movieId) {
      axios({
        url: drf.movies.movie_like(movieId),
        method: 'post',
        headers: { Authorization: `Token ${localStorage.getItem('token')}` },
      })
      .then(res => {
        commit("LIKE_MOVIE", res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },

    // 영화 위시리스트
    wishMovie({ commit }, movieId) {
      axios({
        url: drf.movies.movie_wish(movieId),
        method: 'post',
        headers: { Authorization: `Token ${localStorage.getItem('token')}` },
      })
      .then(res => {
        commit("WISH_MOVIE", res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },

    // 영화 생성(관리자)
    createMovie({ commit }) {
      axios({
        url: drf.movies.movie_create(),
        method: 'post',
        headers: { Authorization: `Token ${localStorage.getItem('token')}` },
      })
      .then(res => {
        commit("SET_MOVIE", res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },

    // 영화 수정(관리자) // 데이터 삽입 필요
    updateMovie({ commit }, movieId) {
      axios({
        url: drf.movies.movie_edit(movieId),
        data: {},
        method: 'put',
        headers: { Authorization: `Token ${localStorage.getItem('token')}` },
      })
      .then(res => {
        commit("SET_MOVIE", res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },

    // 영화 삭제
    deleteMovie({ commit }, movieId) {
      axios({
        url: drf.movies.movie_edit(movieId),
        method: 'delete',
        headers: { Authorization: `Token ${localStorage.getItem('token')}` },
      })
      .then(() => {
        commit("SET_MOVIE", {})
        // 다른곳으로 라우팅 필요(커스텀 영화 조회 페이지 등)
      })
      .catch(err => {
        console.error(err)
      })
    },

  },
}

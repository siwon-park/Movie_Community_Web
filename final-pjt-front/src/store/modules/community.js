import axios from 'axios'
import drf from '@/api/drf'
import router from '@/router'

import _ from 'lodash'

export default {
  state: {
    reviews: [],
    review: {},
    comments: [],
    like_count: 0,
    sortedReviews: {},
    vsQuestion: {},
    questionResult: {},
    questionDetailResult: {},
    questionAnswer: {},
  },

  getters: {
    reviews: state => state.reviews,
    review: state => state.review,
    isAuthor: (state, getters) => {
      return state.review.write_review_user?.username === getters.currentUser.username
    },
    isReview: state => !_.isEmpty(state.review),
    comments: state => state.comments,
    like_count: state => state.like_count,
    sortedReviews: state => state.sortedReviews,
    vsQuestion: state => state.vsQuestion,
    questionResult: state => state.questionResult,
    questionDetailResult: state => state.questionDetailResult,
    questionAnswer: state => state.questionAnswer,
  },

  mutations: {
    SET_REVIEWS: (state, reviews) => state.reviews = reviews,
    SET_REVIEW: (state, review) => state.review = review,
    SET_REVIEW_COMMENTS: (state, comments) => (state.review.comments = comments),
    SET_COMMENTS: (state, comments) => (state.comments = comments),
    ADD_COMMENTS(state, comments) {
      state.comments = []
      state.comments = comments
    },
    LIKE_COUNT: (state, data) => (state.like_count = data.like_review_users?.length),
    FETCH_SORTED_REVIEWS: (state, sorted_data) => (state.sortedReviews = sorted_data),
    CREATE_QUESTION: (state, vs_data) => (state.vsQuestion = vs_data),
    FETCH_QUESTION_RESULT: (state, ret_data) => (state.questionResult = ret_data),
    FETCH_DETAIL_QUESTION_RESULT: (state, detail_data) => (state.questionDetailResult = detail_data),
    VOTE_QUESTION: (state, pick_data) => (state.questionAnswer = pick_data)
  },

  actions: {
    // 전체 게시글 목록 조회
    fetchReviews({ commit, getters }) {
      axios({
        url: drf.community.reviews(),
        method: 'get',
        headers: getters.authHeader,
      })
      .then(res => commit('SET_REVIEWS', res.data))
      .catch(err => {
        console.error(err.response)
        alert('로그인이 필요한 서비스입니다')
        router.push({ name: 'LoginFormView' })
      })
    },

    // 단일 리뷰(게시글) 조회 => 에러 404
    fetchReview({ commit, getters }, reviewId) {
      axios({
        url: drf.community.review(reviewId),
        method: 'get',
        headers: getters.authHeader,
      })
        .then(res => commit('SET_REVIEW', res.data))
        .catch(err => {
          console.error(err.response)
          if (err.response.status === 404) {
            router.push({ name: 'NotFound404' })
          }
        })
    },

    // 리뷰(게시글) 생성(영화 선택 X)
    createReview({ commit, getters }, review) {
      axios({
        url: drf.community.reviews(),
        method: 'post',
        data: review,
        headers: getters.authHeader,
      })
        .then(res => {
          commit('SET_REVIEW', res.data)
          router.push({
            name: 'review',
            params: { reviewId: getters.review.id }
          })
        })
    },

    // 리뷰(게시글) 생성(영화를 선택)
    createMovieReview({ commit, getters }, {movieId, review}) {
      axios({
        url: drf.community.movie_review(movieId),
        method: 'post',
        data: review,
        headers: getters.authHeader,
      })
      .then(res => {
        commit("SET_REVIEW", res.data)
        router.push({
          name: 'review',
          params: { reviewId: getters.review.id }
        })
      })
      .catch(err => {
        console.error(err)
      })
    },

    // 리뷰(게시글) 수정
    updateReview({ commit, getters }, { id, title, content}) {
      axios({
        url: drf.community.review(id),
        method: 'put',
        data: { title, content },
        headers: getters.authHeader,
      })
      .then(res => {
        commit('SET_REVIEW', res.data)
        router.push({
          name: 'review',
          params: { reviewId: getters.review.id }
        })
      })
    },

    // 리뷰(게시글) 삭제
    deleteReview({ commit, getters }, reviewId) {
      if (confirm('정말 삭제하시겠습니까?')) {
        axios({
          url: drf.community.review(reviewId),
          method: 'delete',
          headers: getters.authHeader,
        })
        .then(() => {
          commit('SET_REVIEW', {})
          router.push({ name: 'CommunityView' })
        })
        .catch(err => console.error(err.response))
      }
    },

    // 좋아요
    likeReview({ commit, getters }, reviewId) {
      axios({
        url: drf.community.like_review(reviewId),
        method: 'post',
        headers: getters.authHeader,
      })
      .then(res => {
        commit('LIKE_COUNT', res.data)
      })
      .catch(err => console.error(err))
    },

////////////////////// 댓글 부분 //////////////////////////////
    // 댓글 조회
    fetchComments({ commit, getters }, reviewId) {
      axios({
        url: drf.community.comments(reviewId),
        method: 'get',
        headers: getters.authHeader,
      })
      .then(res => commit('SET_COMMENTS', res.data))
      .catch(err => console.error(err.response))
    },

    // 댓글 생성
		createComment({ commit, getters }, { reviewId, content }) {
      const comment = { content }
      axios({
        url: drf.community.comments(reviewId),
        method: 'post',
        data: comment,
        headers: getters.authHeader,
      })
      .then(res => {
        commit('SET_REVIEW_COMMENTS', res.data)
      })
      .catch(err => console.error(err.response))
    },
    
    // 댓글 수정
    updateComment({ commit, getters }, { reviewId, commentId, content }) {
      const comment = { content }
      axios({
        url: drf.community.comment(reviewId, commentId),
        method: 'put',
        data: comment,
        headers: getters.authHeader,
      })
      .then(res => {
        commit('SET_REVIEW_COMMENTS', res.data)
      })
      .catch(err => console.error(err.response))
    },

    // 댓글 삭제
    deleteComment({ commit, getters }, { reviewId, commentId }) {
      if (confirm('정말 삭제하시겠습니까?')) {
        axios({
          url: drf.community.comment(reviewId, commentId),
          method: 'delete',
          data: {},
          headers: getters.authHeader,
        })
          .then(res => {
            commit('SET_REVIEW_COMMENTS', res.data)
          })
          .catch(err => console.error(err.response))
      }
    },

    // 대댓글 생성
    createCommentToComment({ commit, getters }, { reviewId, content, superCommentId }) {
      const commentToComment = {content}
      axios({
        url: drf.community.comment(reviewId, superCommentId),
        method: 'post',
        data: commentToComment,
        headers: getters.authHeader,        
      })
      .then(res => {
        commit("ADD_COMMENTS", res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },

    // 대댓글 수정
    updateCommentToComment({ commit, getters }, { reviewId, content, superCommentId }) {
      const commentToComment = {content}
      axios({
        url: drf.community.comment(reviewId, superCommentId),
        method: 'put',
        data: commentToComment,
        headers: getters.authHeader,        
      })
      .then(res => {
        commit("SET_COMMENTS", res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },

    // 대댓글 삭제
    deleteCommentToComment({ commit, getters }, { reviewId, content, superCommentId }) {
      const commentToComment = {content}
      axios({
        url: drf.community.comment(reviewId, superCommentId),
        method: 'put',
        data: commentToComment,
        headers: getters.authHeader,        
      })
      .then(res => {
        commit("SET_COMMENTS", res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },

    // 댓글 좋아요
    likeComment({ commit, getters }, { reviewId, currentUserId, commentId }) {
      axios({
        url: drf.community.like_comment(reviewId, commentId),
        method: 'post',
        data: currentUserId,
        headers: getters.authHeader,
      })
      .then(res => {
        commit("SET_COMMENTS", res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },

    // 필터링된 전체 게시글 정보(최신순, 좋아요, 댓글 많은 순)
    fetchSortedReviews({commit, getters}, sort_num) {
      axios({
        url: drf.community.reviews_sort(sort_num),
        method: 'get',
        headers: getters.authHeader,
      })
      .then(res => {
        commit("FETCH_SORTED_REVIEWS", res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },
    ///////////////////////게시판 추가 기능 A vs B ////////////////////////
    // 주제 생성
    createQuestion({ commit, getters }, AvsB) {
      const topic = {
        title: AvsB,
      }
      axios({
        url: drf.community.question_create(),
        method: 'post',
        data: topic,
        headers: getters.authHeader,
      })
      .then(res => {
        commit("CREATE_QUESTION", res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },

    // 특정 주제에 대한 전체 응답 수 조회
    fetchQuestionResult({ commit, getters }, questId) {
      axios({
        url: drf.community.question_fetch(questId),
        method: 'get',
        headers: getters.authHeader,
      })
      .then(res => {
        commit("FETCH_QUESTION_RESULT", res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },

    // 개별 응답(T/F) 조회(0이면 F, 1이면 T)
    fetchDetailQuestionResult({ commit, getters }, {questId, voteId}) {
      axios({
        url: drf.community.question_vote(questId, voteId),
        method: 'get',
        headers: getters.authHeader,
      })
      .then(res => {
        commit("FETCH_DETAIL_QUESTION_RESULT", res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },

    // 주제에 투표
    voteQuestion({ commit, getters }, {questId, choice}) {
      const pick = {
        vote_answer: choice
      }
      axios({
        url: drf.community.question_like(questId),
        method: 'post',
        data: pick,
        headers: getters.authHeader,
      })
      .then(res => {
        commit("VOTE_QUESTION", res.data)
      })
      .catch(err => {
        console.error(err)
      })
    },
  },
}

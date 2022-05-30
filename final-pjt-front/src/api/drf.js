const HOST = 'http://localhost:8000/'

const ACCOUNTS = 'accounts/'
const MOVIES = 'movies/'
const REVIEWS = 'community/'
const COMMENTS = 'comment/'

export default {
  // account(로그인/회원가입/프로필) 관련 경로
  accounts: {
    // 로그인
    login: () => HOST + 'account/' + 'login/',
    // 로그아웃
    logout: () => HOST + 'account/' + 'logout/',
    // 회원가입
    signup: () => HOST + 'account/' + 'signup/',
    // 현재 user 정보(Token으로 판별) => 
    currentUserInfo: () => HOST + 'account/' + 'user/',
    // 비밀번호 변경
    changepassword: () => HOST + 'account/' + 'password/change/',
    // 회원탈퇴
    deletemember: () => HOST + ACCOUNTS + 'delete/',
    // 프로필 조회
    profile: userId => HOST + ACCOUNTS + `${userId}/profile/`,
    // 사용자의 영화 리스트 조회
    personalmovielist: userId => HOST + ACCOUNTS + `${userId}/list/`,
    // 사용자의 싫어요 장르 조회
    personalhatemovie: userId => HOST + ACCOUNTS + `${userId}/hate_genre/`,
    // 사용자의 싫어요 장르 등록 및 해제
    personalhatemovieupdate: (userId, genreId) => HOST + ACCOUNTS + `${userId}/hate_genre/${genreId}/`,
    // 팔로우 등록 및 해제
    personalfollow: userId => HOST + ACCOUNTS + `${userId}/follow/`,
    // 친구 추천
    friendreco: userId => HOST + ACCOUNTS + `${userId}/friend/`,
    // 좋아요 기반 영화 추천
    recolike: userId => HOST + ACCOUNTS + `${userId}/reco_like/`,
    // 평점 기반 영화 추천
    recorate: userId => HOST + ACCOUNTS + `${userId}/reco_rate/`,

  },
  // 영화(메인페이지, movies) 관련 경로
  // 영화 생성/수정/삭제 데이터 제작 필요
  movies: {
    // 메인 페이지 상단 영화 조회 경로
    movies_main: () => HOST + MOVIES,
    // 메인 페이지 하단 서브 영화 조회 경로
    movies_sub: sort_num => HOST + MOVIES + `${sort_num}/sort/`,
    // 영화 상세 조회(데이터 출력용)
    movie_detail: movie_id => HOST + MOVIES + `${movie_id}/`,
    // 영화별 리뷰 게시글 조회
    movie_reviews: movie_id => HOST + MOVIES + `${movie_id}/review/`,
    // 추천 영화 조회
    movie_recommend: genre_id => HOST + MOVIES + `${genre_id}/genre/`,
    // 평점 조회
    movie_rate_list: userId => HOST + MOVIES + `${userId}/rate_list/`,
    // 영화 평점 매기기
    movie_rate: movie_id => HOST + MOVIES + `${movie_id}/rate/`,
    // 영화 평점 매기기 수정 및 삭제
    movie_rate_update: (movieId, rateId) => HOST + MOVIES + `${movieId}/rate/${rateId}/`,
    // 영화 좋아요 누르기
    movie_like: movie_id => HOST + MOVIES + `${movie_id}/like/`,
    // 영화 위시리스트 추가/삭제
    movie_wish: movie_id => HOST + MOVIES + `${movie_id}/wish/`,
    // 영화 생성(관리자)
    movie_create: () => HOST + MOVIES + 'create/',
    // 영화 수정&삭제(관리자)
    movie_edit: movie_id => HOST + MOVIES + `${movie_id}/edit/`,
  },
  // 커뮤니티(리뷰/댓글, community) 관련 경로
  community: {
    // 전체 review 조회 / 생성(영화를 선택하지 않은 review)
    reviews: () => HOST + REVIEWS,
    // 영화를 선택한 review 생성
    movie_review: movieId => HOST + REVIEWS + `${movieId}/review/`,
    // 필터링된 게시글 정보(최신순, 좋아요, 댓글 많은 순)
    reviews_sort: sort_num => HOST + REVIEWS + `${sort_num}/sort/`,
    // 단일 review 조회
    review: reviewId => HOST + REVIEWS + `${reviewId}/`,
    // review 좋아요
    like_review: reviewId => HOST + REVIEWS + `${reviewId}/` + 'like/',
    // 전체 comment 조회 및 생성(영화 선택 X)
    comments: reviewId => HOST + REVIEWS + `${reviewId}/` + COMMENTS,
    // 대댓글 생성 및 전체 댓글 수정 및 삭제
    comment: (reviewId, superCommentId) => HOST + REVIEWS + `${reviewId}/` + COMMENTS + `${superCommentId}/`,
    // 댓글 좋아요 등록 및 해제
    like_comment: (reviewId, commentId) => HOST + REVIEWS + `${reviewId}/` + 'like/' + `${commentId}/`,
    // 댓글별 좋아요 개수 조회

    // 게시판 A vs B 주제 생성(관리자)
    question_create: () => HOST + REVIEWS + 'question/',
    // 주제와 전체 응답 수 조회
    question_fetch: questId => HOST + REVIEWS + `${questId}/question/`,
    // 주제와 특정 응답 수 조회
    question_vote: (questId, voteId) => HOST + REVIEWS + `${questId}/vote/${voteId}/`,
    // 투표(의견) 등록
    question_like: questId => HOST + REVIEWS + `${questId}/vote/like/`,

  },

}

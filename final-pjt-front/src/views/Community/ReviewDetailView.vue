<template>
  <div style="margin-left: 25%; margin-right: 25%;">
    <div style="margin-bottom: 80px;"></div>
    <div>
      <div class="oneline" style="margin-bottom: 5px;">
        <div>No.{{ review.id }} </div>
        <div v-if="review.write_review_movie">{{ review.write_review_movie.title }}</div>
      </div>
      <div style="margin-bottom: 35px;">
        <div class="title">{{ review.title }}</div>
        <div style="margin-top: 5px;">{{ review.write_review_user.username }}</div>
      </div>
      <div>
        <div style = "font-size: 25px; margin-bottom: 30px;">{{ review.content }}</div>
        <div style="font-size: 12px; color:grey;">
          <div class="d-flex justify-content-end">created : {{ review.updated_at }}</div>
          <div class="d-flex justify-content-end">updated : {{ review.created_at }}</div>
        </div>
        <div class="icon d-flex justify-content-between" style="font-size:18px; margin-top: 15px; margin-bottom: 15px;">
          <div>
            <div class="speech" data-tooltip="Like">
              <div class="heart" @click="like_review(reviewId)">💟{{ likeCount }}</div>
            </div>
            <div class="comment icon"> 💬{{ review.comment_count }}</div>
          </div>
          <button class="back-button" @click="goBack">뒤로가기</button>
        </div>
      </div>
    </div>

    <div>
      <div v-if="isAuthor">
        <div class="d-flex justify-content-end" style="font-size:20px">
          <router-link class="link" :to="{ name: 'reviewEdit', params: { reviewId } }">
            <button style="margin-right:4px; margin-left:4px; height: 30px;">Edit</button>
          </router-link>
          <button class="link" style="margin-left:4px;" @click="deleteReview(reviewId)">Delete</button>
        </div>
      </div>
    </div>
    <br>
    <!-- Comment UI -->
    <CommentList :comments="comments.reply_comments"></CommentList>
    <!-- 뒤로가기 버튼 -->
  </div>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex'
  import CommentList from '@/components/Community/CommentList.vue'
  import router from '@/router'

  export default {
    name: 'ReviewDetailView',
    components: { 
      CommentList
    },
    data() {
      return {
        reviewId: this.$route.params.reviewId,
        test_toggle: true,
        likes: 0,
      }
    },
    computed: {
      ...mapGetters(['isAuthor', 'review', 'comments', 'like_count', 'movieDetail']),
      likeCount() {
        return this.review.like_count
      },

    },
    
    methods: {
      ...mapActions([
        'fetchReview',
        'likeReview',
        'deleteReview',
        'fetchComments',
        'fetchMovieDetail',
      ]),
      like_review(reviewId) {
        this.fetchReview(this.reviewId)
        this.likeReview(reviewId)
        this.fetchReview(this.reviewId)
        this.review.like_count = this.likeCount
      },
      // 뒤로가기
      goBack() {
        router.push({ name: 'CommunityView' }) 
      },
    },

    created() {
      this.fetchReview(this.reviewId)
      this.fetchMovieDetail(this.review.write_review_movie?.id)
    },
    mounted() {
      this.fetchComments(this.reviewId)
      this.fetchComments(this.reviewId)
    }
  }
</script>

<style scoped>
  .oneline div{
    display: inline;
    color: #e92964;
    font-size: 20px;
    font-weight: bolder;
  }
  
  .title{
    font-weight: bold;
    font-size: 30px;
  }

  .icon div{
    display: inline;
  }

  /* 마우스 오버 시, 손모양 */
  .heart{
    cursor:pointer;
  }

  /* 좋아요 이모티콘 */
  .speech{
    position: relative;
    display: inline-flex;
  }

  .speech::before,
  .speech::after{
    content: '';
    position: absolute;
    left: 50%;
    transform: translate(-50%, 3px);
    visibility: hidden;
    transition: transform .5s;
  }

  .speech::before{
    top: -10px;
    border: 5px solid transparent;
    border-top: 5px solid #fff;
  }

  .speech::after{
    content: attr(data-tooltip);
    top: -27px;
    padding: 2px 5px;
    border-radius: 4px;
    color: #fff;
    font-size: 15px;
    background-color: #e92964;
  }
  .speech:hover::before,
  .speech:hover::after{
    transform: translate(-65%, 0);
    visibility: visible;
  }

/* 게시글 수정, 삭제 버튼 */
  .link{
    position: relative;
    color : black;
    text-decoration: none;
    z-index: 1;
    padding: 0 .2rem;
    transition: color .2s;
  }

  .link::after{
    content:'';
    z-index: -1;
    position: absolute;
    inset: 99% 0 0 0;
    background: #e92964;
    transition: inset .2s;
  }

  .link:hover{
    color: white;
  }

  .link:hover::after{
    inset: 0 0 0 0;
  }

  /* 뒤로가기 버튼 */
    .back-button {
    background-color: #E92964;
    box-shadow: #BC41AB 4px 4px 0px;
    border-radius: 8px;
    transition: transform 200ms, box-shadow 200ms;
    color : #fff;
    width : 100px;
    height: 45px;
  }

  .back-button:active{
    transform: translateY(4px) translateX(4px);
    box-shadow: #BC41AB 0px 0px 0px;
  }
  </style>

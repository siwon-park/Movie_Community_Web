<template>
  <div :style="commentMargin">
    <div class="comment-to-comment">
      <div>
        <div class="d-flex justify-content-between" style="margin-bottom: 2%;">
          <div style="margin-bottom:10px; font-size: 18px">{{commentToComment.content}}</div>
            <div class="d-flex justify-content-end">
              <button class="link" style="margin-right: 6px; height: 30px;" v-if="isAliveComment" @click="openCommentForm1">대댓글 작성하기</button>
              <form v-if="value===1" @submit.prevent="writeComment">
                <label for="comment"></label>
                <input type="text" style="border: 1px solid #e92964;" id="comment" v-model="content" required>
                <button class="link" style="height: 30px; margin-right: 7px; margin-left: 6px; margin-bottom: 9px;">작성</button>
              </form>
              <div>
                <button class="link" v-if="currentUser.id === commentToComment.write_comment_user && isAliveComment" @click="openCommentForm2" style="margin-right: 6px; height: 30px;" >수정</button>
                <button class="link" v-if="currentUser.id === commentToComment.write_comment_user && isAliveComment" @click="deleteComment" style="height: 30px;" >삭제</button>
              </div>
              <div>
                <div v-if="openToggle">
                  <form v-if="value===2" @submit.prevent="updateComment">
                    <label for="comment"></label>
                    <input type="text" style="border: 1px solid #e92964; margin-left: 8px; margin-right: 8px;" id="comment" v-model="awContent" required>
                    <button class="link" style="width: 35px; height: 30px;">등록</button>
                  </form>
                </div>
              </div>
            </div>
        </div>
        <div class="d-flex justify-content-between">
          <div class="speech" data-tooltip="Like">
            <div @click="pressLike" class="heart" >💟{{ commentToComment.like_comment_users.length }}</div>
          </div>
          <div style="font-size: 12px; color:grey;">
            <div class="d-flex justify-content-end">created : {{ commentToComment.created_at}}</div>
            <div class="d-flex justify-content-end">updated : {{ commentToComment.updated_at }}</div>
          </div>
        </div>
      </div>
    </div>
      <!-- 대댓글 및 좋아요 출력/누르기 -->
    <hr class="line">
    <!-- 대댓글이 있으면 출력 -->
    <div v-if="hasComment">
      <CommentToComment
      v-for="comment in commentToComment.commented"
      :key="comment.id"
      :commentToComment="comment"
      :spacing="spacing + 20"></CommentToComment>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
export default {
  name: "CommentToComment",
  data() {
    return {
      openToggle: false,
      content: '', // 현재 쓸 내용
      value: 0,
      awContent: '', // aw;aleardywritten
    }
  },
  props: {
    commentToComment:{
      type: Object,
    },
    spacing: {
      type: Number,
      default: 0
    },
  },
  computed: {
    ...mapGetters(['currentUser']),
    // 자식 댓글이 있는지 확인 => 컴포넌트 간 재귀 호출을 멈추기 위함
    hasComment() {
      return this.commentToComment.commented && this.commentToComment.commented.length > 0
    },
    commentMargin() {
      return {
        'margin-left': `${this.spacing}px`
      }
    },
    isAliveComment() {
      if (this.commentToComment.content === "삭제된 댓글입니다.") {
        return false // 삭제되었으면 false로 하여 v-if에서 출력하게 하지 않음
      }
      return true
    }
  },
  methods: {
    ...mapActions(['createCommentToComment', 'updateCommentToComment', 'deleteCommentToComment', 'likeComment']),
    // 대댓글 작성 폼 오픈
    openCommentForm1() {
      this.openToggle = !this.openToggle
      this.value = 1
    },
    // 대댓글 수정 폼 오픈
    openCommentForm2() {
      this.openToggle = !this.openToggle
      this.value = 2
      this.awContent = this.commentToComment.content
    },
    // 대댓글 작성 호출 함수
    writeComment() {
      // console.log(this.commentToComment)
      // // const comment_to_comment = this.content
      // const comment_object = {
      //   commented: [],
      //   content: this.content,
      // }
      // // console.log(typeof(comment_object))
      // console.log(this.commentToComment.commented)
      // this.commentToComment.commented.push(comment_object)
      // console.log(this.commentToComment.commented_review, this.commentToComment.id)
      this.createCommentToComment({ reviewId: this.commentToComment.commented_review, content: this.content, superCommentId: this.commentToComment.id})
      this.content = ''
    },
    updateComment() {
      this.updateCommentToComment({ reviewId: this.commentToComment.commented_review, content: this.awContent, superCommentId: this.commentToComment.id})  
    },
    deleteComment() {
      this.updateCommentToComment({ reviewId: this.commentToComment.commented_review, content: "삭제된 댓글입니다.", superCommentId: this.commentToComment.id})  
    },
    pressLike() {
      this.likeComment({ reviewId: this.commentToComment.commented_review, currentUserId: this.currentUser.pk, commentId: this.commentToComment.id})
    },
  },
}
</script>

<style>
  /* 마우스 오버 시, 손모양 */
  .heart{
    cursor:pointer;
  }

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

  /* 좋아요 이모티콘 */
  .speech{
    position: relative;
    display: inline-flex;
  }

  /* .speech div{
    background: radial-gradient(circle at 30% 107%, #fdf497 0%, #fdf497 5%,
    #fd5949 45%, #d6249f 60%, #285AEB 90% );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

  } */

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
    /* 높이 */
    top: -22px;
    padding: 2px 5px;
    border-radius: 4px;
    color: #fff;
    font-size: 12px;
    background-color: #e92964;
  }
  .speech:hover::before,
  .speech:hover::after{
    transform: translate(-60%, 0);
    visibility: visible;
  }

</style>
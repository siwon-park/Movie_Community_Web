<template>
  <div class="comment-list-item">
    <div>
      <div class="d-flex justify-content-between" style="margin-bottom: 2%;">
        <div style="margin-bottom:10px; font-size: 20px" v-if="!isEditing">{{ payload.content }}</div><!-- 댓글 출력 -->        
        <div v-if="isAliveComment" class="d-flex justify-content-end">
          <button class="link" style="margin-right: 6px; height: 30px;" @click=openCommentForm>댓글 작성하기</button> <!--클릭하면 작성버튼 띄움-->
          <!-- 답글 작성 칸 -->
          <button v-if="openToggle">
            <input type="text" style="border: 1px solid #e92964;" v-model="writtenContent" required>
            <button class="link" style="height: 30px; margin-right: 7px; margin-left: 6px; margin-bottom: 9px;" @click="writeComment()">작성</button>
          </button>
          <div class="d-flex" v-if="currentUser.id === comment.write_comment_user && !isEditing">
            <button class="link" style="width: 35px; height: 30px; margin-right: 10px;" @click="switchIsEditing">수정</button>
            <button class="link" style="width: 35px; height: 30px;" @click="deleteBtn">삭제</button>
          </div>
          <button style="padding-bottom: 10px;" v-if="isEditing">
            <input type="text" style="border: 1px solid #e92964;"  v-model="payload.content">
            <button class="link" style="margin-left: 6px; margin-right: 6px; width: 35px; height: 30px;" @click="onUpdate" @keyup.enter="onUpdate">등록</button>
            <button class="link" style="width: 35px; height: 30px;" @click="switchIsEditing">취소</button>
          </button>
        </div>
      </div>
      <!-- 대댓글 작성-->
      <div class="d-flex justify-content-between">
        <div class="speech" data-tooltip="Like">
          <div class="heart" @click="pressLike">💟{{ this.comment.like_comment_users.length }}</div><!-- 좋아요 누르기 -->
        </div>
        <div style="font-size: 12px; color:grey;">
          <div class="d-flex justify-content-end">created : {{ comment.created_at}}</div>
          <div class="d-flex justify-content-end">updated : {{ comment.updated_at }}</div>
        </div>
      </div>
      <hr>
    </div>
    <!-- 대댓글 출력 -->
    <CommentToComment
    v-for="commentToComment in this.comment.commented"
    :key="commentToComment.id"
    :commentToComment="commentToComment"
    >
    </CommentToComment>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import CommentToComment from './CommentToComment.vue'

export default {
  name: 'CommentListItem',
  components: {
    CommentToComment,
  },
  props: { comment: Object },
  data() {
    return {
      isEditing: false,
      payload: {
        reviewId: this.comment.commented_review,
        commentId: this.comment.id,
        content: this.comment.content
      },
      isEmpty: (this.comment.commented.length === 0),
      openToggle: false,
      writtenContent: '',
    }
  },
  computed: {
    ...mapGetters(['currentUser']),
    isAliveComment() {
      if (this.comment.content === '삭제된 댓글입니다.') {
        return false // 삭제되었으면 false로 하여 v-if에서 출력하게 하지 않음
      }
      return true
    },

  },
  methods: {
    ...mapActions(['updateComment', 'deleteComment', 'createCommentToComment', 'likeComment', 'fetchComments']),
    switchIsEditing() {
      this.isEditing = !this.isEditing
    },
    // 댓글 업데이트를 위한 함수
    onUpdate() {
      this.updateComment(this.payload)
      this.isEditing = false
      this.fetchComments(this.comment.commented_review)
    },
    // 대댓글 작성 폼을 열기 위한 토글링 함수
    openCommentForm() {
      this.openToggle = !this.openToggle
    },
    // 대댓글 작성 함수
    writeComment() {
      this.createCommentToComment({ reviewId: this.comment.commented_review, content: this.writtenContent, superCommentId: this.comment.id})
      this.writtenContent = ''
      alert('댓글이 등록되었습니다.')
      this.fetchComments(this.comment.commented_review)
      this.fetchComments(this.comment.commented_review)
    },
    // 댓글 삭제
    deleteBtn() {
      this.deleteComment(this.payload)
      this.payload.content = '삭제된 댓글입니다.'
      this.fetchComments(this.comment.commented_review)
      this.fetchComments(this.comment.commented_review)
    },
    // 댓글 좋아요 누르기
    pressLike() {
      // 현재 유저의 아이디와 글 번호, 댓글번호 넘겨주기
      this.likeComment({ reviewId: this.comment.commented_review, currentUserId: this.currentUser.pk, commentId: this.comment.id})
    },
  },

}
</script>

<style scoped>
  .oneline{
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
    /* 높이 */
    top: -23px;
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
</style>
<template>
  <form @submit.prevent="onSubmit" class="comment-list-form" style="margin-right: 0px;margin-left: 35px;">
    <label for="comment"></label>
    <input type="text" style="margin-right: 10px;" size="38" placeholder="여러분의 소중한 댓글을 입력해주세요" id="comment" v-model="content" required>
    <button class="link" style="height: 30px;" @click="onSubmit">등록</button>
  </form>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'CommentListForm',
  data() {
    return {
      content: ''
    }
  },
  computed: {
    ...mapGetters(['review']),
  },
  methods: {
    ...mapActions(['createComment', 'fetchComments']),
    onSubmit() {
      alert("댓글이 등록되었습니다.")
      this.createComment({ reviewId: this.review.id, content: this.content })
      this.content = ''
      this.fetchComments(this.review.id)
      this.fetchComments(this.review.id)
    }
  }
}
</script>

<style>
  .comment-list-form {
    border: 1px solid #BC41AB;
    margin: 1rem;
    padding: 1rem;
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
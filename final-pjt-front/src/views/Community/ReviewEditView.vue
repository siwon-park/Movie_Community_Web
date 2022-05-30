<template>
  <div style="margin-left: 25%; margin-right: 25%;">
    <h1 class="title" style="margin-top: 74px; font-size: 60px; font-weight: 500;margin-bottom: 35px; text-align:center;">Community Club 글 수정</h1>
    <ReviewForm v-if="isReview" :review="review" action="update"></ReviewForm>
  </div>
</template>

<script>
import ReviewForm from '@/components/Community/ReviewForm.vue'
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'ReviewEditView',
  components: { 
    ReviewForm 
  },
  computed: {
    ...mapGetters(['review', 'isReview',])
  },
  methods: {
    ...mapActions(['fetchReview'])
  },
  created() {
    this.fetchReview(this.$route.params.reviewId)
  },
}
</script>

<style scoped>
  .title{
    text-shadow: red 0 0, cyan 0 0;
    transition: text-shadow 200ms;
    letter-spacing: 2px !important;
    font-family: 'Do Hyeon', sans-serif;
  } 

  .title:hover{
    text-shadow: red -4px 0 0, cyan 4px 0 0;
  }
</style>

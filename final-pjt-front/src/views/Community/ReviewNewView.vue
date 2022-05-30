<template>
  <div style="margin-left: 25%; margin-right: 25%;">
    <h1 class="title" style="margin-top: 74px; font-size: 60px; font-weight: 500; margin-bottom: 35px; text-align:center;">Community Club 글쓰기</h1>
    <ReviewForm :review="review" action="create"></ReviewForm>
  </div>
</template>

<script>
  import ReviewForm from '@/components/Community/ReviewForm.vue'
  export default {
    name: 'ReviewNewView',
    components: { ReviewForm },
    data() {
      return {
        review: {
          pk: null,
          title: '',
          content: '',
        }
      }
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

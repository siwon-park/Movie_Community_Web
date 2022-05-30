<template>
  <v-app>
    <v-main>
      <v-container fluid>
        <div style="margin-left: 25%; margin-right: 25%;">
          <div class="title">Community Club</div>
        </div>
        <div>
          <OneVsOne></OneVsOne>
        </div>
        <ReviewListView></ReviewListView>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import ReviewListView from '@/views/Community/ReviewListView.vue'
import OneVsOne from '@/views/Community/OneVsOne.vue'

export default {
  name: 'CommunityView',
  components: {
    ReviewListView,
    OneVsOne,
  }
}
</script> 

<style scoped>

  .v-application .title{
    line-height: 170px !important;
    font-size: 90px !important;
    text-align: center;
  } 

   .title{
    text-shadow: red 0 0, cyan 0 0;
    transition: text-shadow 200ms;

  }
  .title:hover{
    text-shadow: red -6px 0 0, cyan 6px 0 0;
  }

</style>
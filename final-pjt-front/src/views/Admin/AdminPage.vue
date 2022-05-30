<template>
<div>
  <div class="container-fluid">
    <h1>관리자 페이지</h1>
    <button class="btn btn-primary" @click="goEdit">영화 생성</button>
  </div>
  <div>
    <CreatedMovieList></CreatedMovieList>
  </div>
</div>
</template>

<script>
import router from '@/router'
import CreatedMovieList from './CreatedMovieList.vue'

export default {
  name: 'AdminPage',
  components: {
    CreatedMovieList,
  },
  methods: {
    goEdit() {
      router.push({name: 'MovieCreation'})
    }
  }
}
</script>

<style>

</style>
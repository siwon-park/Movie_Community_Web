<template>
  <div id="app">
    <nav-bar></nav-bar>
    <router-view></router-view>
    <!-- 업버튼(삭제) -->
    <button type="button" class="btn btn-danger btn-floating" id="btn-back-to-top"
    @click="backToTop">
      <i class="fas fa-arrow-up"></i>
    </button>
    <foot-bar></foot-bar>
  </div>
</template>

<script>
import NavBar from './NavBar.vue';
import FootBar from './FootBar.vue';

export default {
  name: 'App',
  components: { 
    NavBar,
    FootBar
  },
  methods: {
    backToTop() {
      document.body.scrollTop = 0;
      document.documentElement.scrollTop = 0;
    }
  },
}

</script>

<style>
  * {
    font-family: 'IBM Plex Sans KR', sans-serif;
  }

  *::selection{
    background-color: #e92964;
    color : #fff
  }

  #btn-back-to-top {
    position: fixed;
    bottom: 60px;
    right: 90px;
    background-color: #e92964;
    color:#fff;
  }
</style>
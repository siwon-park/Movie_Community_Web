<template>
<!-- 네브바에 stick-top을 넣을지 말지 결정 : 고정 버튼 없다면 있는게 나을 듯 함-->
  <nav class="navbar navbar-expand-md stick-top navbar-light sticky-top py-2">
    <div class="container-fluid">
      <!-- 이미지 연결 -->
      <router-link class="navbar-brand" to="/" style="margin-left: 15px; margin-right: 10px;padding-bottom: 15px;">
        <img id="navbar-logo" src="@/assets/logo2.png" alt="netflix_logo" width="60px" height="50px">
      </router-link>
      <!--햄버거 버튼-->
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-between" id="navbarSupportedContent">
        <ul class="navbar-nav pe-3">
          <li class="nav-item">
            <router-link class="nav-link" aria-current="page" to="/" style="color:black">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/community" style="color:black">Community</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/profile" style="color:black">Profile</router-link>
          </li>
          <li v-if="this.loginState === 'Login'" class="nav-item" >
            <router-link class="nav-link" to="/login" style="color:black">{{this.loginState}}</router-link>
          </li>
          <li v-if="this.loginState === 'Logout'" class="nav-item">
            <router-link @click.native="logout" class="nav-link" to="#" style="color:black">{{this.loginState}}</router-link>
          </li>
        </ul>
        <form class="d-flex" role="search">
          <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
          <button class="btn btn-outline-secondary " type="submit">Search</button>
        </form>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'NavBar',
  data() {
    return {
    }
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
    }
  },
  computed: {
    ...mapGetters(['isLoggedIn',]),
    loginState() {
      return (this.isLoggedIn) ? "Logout" : "Login"
    }
  },

}
</script>

<style scoped>

 .nav-link{
   text-align: center;
   min-width: 150px;
   padding: 10px 10px;
   margin: 15px;
   background: #ffffffe0;
   border: none;
   border-radius: 25px;
   color: rgb(81, 158, 214);
   text-transform: uppercase;
   letter-spacing: 2px;
   cursor: pointer;
   outline: none;
   box-shadow: -2px -2px 6px 0 rgba(255, 255, 255, 0.1),
   2px 2px 6px 0 rgba(97, 97, 97, 0.8);
  }

  .nav-link:hover{
    box-shadow: inset -2px -2px 6px 0 rgba(255, 255, 255, 0.2),
    inset 2px 2px 6px 0 rgba(97, 97, 97, 0.8);
  }

</style>
<template>
  <div style="margin-left: 25%; margin-right: 25%;">
    <h1 class="title" style="margin-top: 74px; font-size: 60px; font-weight: 500; margin-bottom: 25px; text-align:center;">
    프로필 수정</h1>
    <div class="d-flex justify-content-around" style="margin-left: 500px;">
      <div style="font-size: 15px;" >
        <router-link to="/password/change">비밀번호 변경</router-link>
        <!-- 회원 탈퇴하기 -->
        <div class="out" @click="onSignout">회원 탈퇴하기</div>
      </div> 
    </div>
    <form @submit.prevent="updateRequest()">
      <div style="font-size:20px; text-align: center;">
        <div class="d-flex justify-content-center" style="margin-bottom: 20px; margin-top:20px">
          <div>
            <label for="username" style="margin-bottom: 8px;">이름</label>
            <input v-model="currentUser.username" style="border: 1px solid #e92964; text-align: center;" type="text" id="username">
          </div>
          <div style="margin-left:20px">
            <label for="sex" style="margin-bottom: 8px;">성별</label>
            <input v-model="currentUser.sex"  style="border: 1px solid #e92964; text-align: center;"  type="text" id="sex">
          </div>
        </div>
        <div class="d-flex justify-content-center">
          <div style="margin-right: 175px;">
            <label for="region" style="margin-bottom: 8px;">지역</label>
            <input v-model="currentUser.region" style="border: 1px solid #e92964; text-align: center; margin-bottom: 10px;"  type="text" id="region">
          </div>
          <div class="btn-group">
            <div type="button" class="dropdown-toggle cta" data-bs-toggle="dropdown" aria-expanded="false">
              싫어하는 장르
            </div>
            <ul style="border: 1px solid #e92964;" class="dropdown-menu">
              <li><a class="dropdown-item" @click="sortBtn(12, '모험')">모험</a></li>
              <li><a class="dropdown-item" @click="sortBtn(14, '판타지')">판타지</a></li>
              <li><a class="dropdown-item" @click="sortBtn(16, '애니메이션')">애니메이션</a></li>
              <li><a class="dropdown-item" @click="sortBtn(18, '드라마')">드라마</a></li>
              <li><a class="dropdown-item" @click="sortBtn(27, '공포')">공포</a></li>
              <li><a class="dropdown-item" @click="sortBtn(28, '액션')">액션</a></li>
              <li><a class="dropdown-item" @click="sortBtn(35, '코미디')">코미디</a></li>
              <li><a class="dropdown-item" @click="sortBtn(36, '역사')">역사</a></li>
              <li><a class="dropdown-item" @click="sortBtn(37, '서부')">서부</a></li>
              <li><a class="dropdown-item" @click="sortBtn(53, '스릴러')">스릴러</a></li>
              <li><a class="dropdown-item" @click="sortBtn(80, '범죄')">범죄</a></li>
              <li><a class="dropdown-item" @click="sortBtn(99, '다큐멘터리')">다큐멘터리</a></li>
              <li><a class="dropdown-item" @click="sortBtn(878, 'SF')">SF</a></li>
              <li><a class="dropdown-item" @click="sortBtn(9648, '미스터리')">미스터리</a></li>
              <li><a class="dropdown-item" @click="sortBtn(10402, '음악')">음악</a></li>
              <li><a class="dropdown-item" @click="sortBtn(10749, '로맨스')">로맨스</a></li>
              <li><a class="dropdown-item" @click="sortBtn(10751, '가족')">가족</a></li>
              <li><a class="dropdown-item" @click="sortBtn(10752, '전쟁')">전쟁</a></li>
              <li><a class="dropdown-item" @click="sortBtn(10770, 'TV 영화')">TV 영화</a></li>
            </ul>
          </div>          
        </div> 
        <div style="font-size: 16px;  margin-top: 20px;" class="d-flex justify-content-center">
          <div style="margin-right: 15px;">
            <button>프로필 수정하기</button>
          </div>
          <div>
            <button @click="goBack">뒤로가기</button>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import router from '@/router'

export default {
  name: "PersonalProfileEdit",
  data() {
    return {
      profileData: {
        username:'',
        region: '',
        sex: '',
      }
    }
  },
  computed: {
    ...mapGetters(['currentUser', 'hateGenres'])
  },
  methods: {
    ...mapActions(['fetchCurrentUser', 'updateProfile', 'signout', 'hateGenresPick', 'fetchHateGenre']),
    updateRequest() {
      this.updateProfile({username: this.currentUser.username, sex: this.currentUser.sex, region: this.currentUser.region})
    },
    goBack() {
      router.push({ name: 'ProfilePage' }) 
    },
    onSignout() {
      this.signout()
    },
    sortBtn(gId) {
      this.hateGenresPick({userId: this.currentUser.id, genreId: gId})
      this.fetchHateGenre(this.currentUser.id)
      this.fetchHateGenre(this.currentUser.id)
    },
  },
  created() {
    // this.fetchCurrentUser() // 테스트
    // this.profileData = this.currentUser
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

  button{
    background-color: #E92964;
    box-shadow: #BC41AB 4px 4px 0px;
    border-radius: 8px;
    transition: transform 200ms, box-shadow 200ms;
    color : #fff;
    width : 120px;
    height: 45px;
  }

  button:active{
    transform: translateY(4px) translateX(4px);
    box-shadow: #BC41AB 0px 0px 0px;
  }

  .out{
    cursor:pointer;
    color:blue;
    text-decoration: underline ;
  }
</style>
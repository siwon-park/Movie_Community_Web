<template>
  <div style="margin-left: 25%; margin-right: 25%;">
    <h1 class="title" style="margin-top: 74px; font-size: 60px; font-weight: 500; margin-bottom: 35px; text-align:center;">비밀번호 변경</h1>
      <form @submit.prevent="changeSubmit(passwordData.newpassword1, passwordData.newpassword2)">
        <div style="text-align: center;">
          <div>
            <div>
              <label for="newpassword1" style="font-size:20px;">새 비밀번호</label>
            </div>
            <input v-model="passwordData.newpassword1" type="password" id="password1"
            style="border: 1px solid #e92964; text-align: center; height:40px; font-size:15px; margin-bottom: 40px; margin-top: 10px;" 
            size="70" placeholder="새 비밀번호를 입력해주세요" required/>
          </div>
          <div>
            <div>
              <label for="newpassword2" style="font-size:20px;">새 비밀번호 확인</label>
            </div>
            <input v-model="passwordData.newpassword2" type="password" id="password2"
            style="border: 1px solid #e92964; text-align: center; height:40px; font-size:15px; margin-bottom: 20px; margin-top: 5px;" 
            size="70" placeholder="다시 한번 입력해주세요" required/>
          </div>
        </div>
        <div style="font-size: 18px;margin-top: 25px;" class="d-flex justify-content-center">
          <button style="margin-right: 20px;">비밀번호 변경</button>
          <button @click="goBack">뒤로가기</button>
        </div>
      </form>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import router from '@/router'

export default {
  name: "PasswordChange",
  data() {
    return {
      passwordData: {
        password1: '',
        password2: '',
      }
    }
  },
  methods: {
    ...mapActions(['changePassword']),
    changeSubmit(p1, p2) {
      this.changePassword({password1: p1, password2: p2})
    },
    goBack() {
      router.push({ name: 'PersonalProfileEdit' }) 
    },
  }
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
</style>
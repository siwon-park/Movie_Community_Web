<template>
  <div>
    <div>
      <h1>비밀번호 찾기</h1>
      <form @submit.prevent="">
        <label for="email">이메일: </label>
        <input v-model="myEmail" style="border: 1px solid #e92964;  height:40px; font-size:20px; margin-bottom: 20px; margin-top: 20px;" type="email" name="email" id="email" placeholder="이메일을 입력하세요">
        <button @click="sendEmail">확인</button>
      </form>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: "PasswordFind",
  data() {
    return {
      myEmail: '',
    }
  },
  methods: {
    ...mapActions(['findPassword',]),
    sendEmail() {
      this.findPassword({e_mail: this.myEmail})
    }
  }
}
</script>

<style>

</style>
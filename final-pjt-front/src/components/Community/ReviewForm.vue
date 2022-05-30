<template>
  <div>
    <form @submit.prevent="onSubmit">
      <div style="text-align: center;">
        <div style = "font-size:18px; text-align: right; margin-bottom: 25px; margin-right: 100px;">
          <button style="margin-right: 20px;" class="back-button" @click="goBack">뒤로가기</button>
          <button>{{ actionBtn }}</button>
        </div>
        <div class="d-flex justify-content-end">
          <select v-model="movie_id" style="width: 400px; margin-right: 10%;" class="form-select" aria-label="영화 제목을 선택하세요">
            <option value="0">영화 선택</option>
            <option value="526896">모비우스</option>
            <option value="752623">로스트 시티</option>
            <option value="639933">노스맨</option>
            <option value="836225">엑소시즘 오브 갓</option>
            <option value="335787">언차티드</option>
            <option value="414906">더 배트맨</option>
            <option value="453395">닥터 스트레인지: 대혼돈의 멀티버스</option>
            <option value="634649">스파이더맨: 노 웨이 홈</option>
            <option value="629542">배드 가이즈</option>
            <option value="628900">더 컨트랙터</option>
            <option value="508947">메이의 새빨간 비밀</option>
            <option value="406759">문폴</option>
            <option value="785985">투캅스 인 파리: 더 테이크다운</option>
            <option value="763285">앰뷸런스</option>
            <option value="284052">닥터 스트레인지</option>
            <option value="799876">아웃핏</option>
            <option value="568124">엔칸토: 마법의 세계</option>
            <option value="606402">야차</option>
            <option value="829557">365일: 오늘</option>
            <option value="284052">닥터 스트레인지</option>
            <option value="951470">실버턴 포위 작전</option>
            <option value="294793">배신의 만찬</option>
            <option value="585083">몬스터 호텔 4: 뒤바뀐 세계</option>
            <option value="800937">시니어 이어</option>
            <option value="696806">애덤 프로젝트</option>
            <option value="774825">아이스 에이지: 벅의 대모험</option>
            <option value="768744">나의 히어로 아카데미아 더 무비: 월드 히어로즈 미션</option>
            <option value="823625">블랙라이트</option>
            <option value="338953">신비한 동물들과 덤블도어의 비밀</option>
            <option value="580489">베놈 2: 렛 데어 비 카니지</option>
            <option value="22">캐리비안의 해적: 블랙펄의 저주</option>
          </select>
        </div>
        <div>
          <label for="title"></label>
          <input v-model="newReview.title" style="border: 1px solid #e92964;  height:40px; font-size:20px; margin-bottom: 20px; margin-top: 20px;" type="text" id="title" size="70" placeholder=" 제목을 입력해주세요" required/>
        </div>
        <div>
          <label for="content"></label>
          <textarea v-model="newReview.content" rows="15" cols="73" style="border: 1px solid #e92964; font-size:20px;" type="text" id="content" placeholder=" 내용을 입력해주세요" required></textarea>
        </div>
      </div>
    </form>
  </div>
</template>
<script>
import { mapActions } from 'vuex'
import router from '@/router'

  export default {
    name: 'ReviewForm',
    props: {
      review: Object,
      action: String,
    },
    data() {
      return {
        newReview: {
          title: this.review.title,
          content: this.review.content,
        },
        movie_id: 0,
        actionBtn: (this.action === "create") ? "등록" : "수정"
      }
    },

    methods: {
      ...mapActions(['createReview', 'updateReview', 'createMovieReview']),
      onSubmit() {
        if (this.action === 'create') {
          if (this.movie_id === 0) {
            this.createReview(this.newReview)
          } else {
            this.createMovieReview({movieId: this.movie_id, review:this.newReview})
          }
          alert("등록되었습니다.")
        } else if (this.action === 'update') {
          const payload = {
            id: this.review.id,
            ...this.newReview,
          }
          this.updateReview(payload)
          alert("수정되었습니다.")
        }
      },
      goBack() {
        router.push({ name: 'CommunityView' })
      }
    },
  }
</script>

<style scoped>
  button{
    background-color: #E92964;
    box-shadow: #BC41AB 4px 4px 0px;
    border-radius: 8px;
    transition: transform 200ms, box-shadow 200ms;
    color : #fff;
    width : 100px;
    height: 45px;
  }

  button:active{
    transform: translateY(4px) translateX(4px);
    box-shadow: #BC41AB 0px 0px 0px;
  }

</style>
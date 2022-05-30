<template>
  <div style="margin-left: 25%; margin-right: 25%;">
    <div class="topic">
        <div class="wrapper">
          <div class="typing-demo" style="font-size:40px; font-weight:bolder; text-align:center;">
            당신의선택은?
          </div>
        </div>
        <div class="inner">
          <div class="d-flex justify-content-between">
            <!-- 차선 -->
            <h2 class="text-primary">카라멜 팝콘({{100-calResult}}%)</h2>
            <h2 class="text-danger">버터 팝콘({{calResult}}%)</h2>
          </div>
          <div class="progress" style="height: 50px;">
            <div :style="bannerStyle2" class="progress-bar progress-bar-striped fs-4" role="progressbar" aria-valuemin="0" aria-valuemax="100" f> {{100-calResult}}% </div>
            <div :style="bannerStyle" class="progress-bar progress-bar-striped bg-danger fs-4" role="progressbar" aria-valuemin="0" aria-valuemax="100">{{calResult}}% </div>
          </div>
          <div class="d-flex justify-content-around align-items-center" style="margin-top: 30px;">
            <div>
              <button @click="pickTrue" class="border btn btn-outline-primary">진리의 카라멜 팝콘이지</button>
            </div>
            <div>
              <button @click="pickFalse" class="border btn btn-outline-danger">무슨 소리? 버터 팝콘 모름?</button>
            </div>
          </div>
        </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: "OneVsOne",
  data() {
    return {
      pick: []
    }
  },
  computed: {
    ...mapGetters(['questionResult' , 'questionDetailResult']),
    calResult() {
      const m = this.questionResult.question_answer_count
      if (m === 0) {
        return 0
      }
      const n = this.questionDetailResult[0].new_question_answer_count
      const ret = (n/m) * 100
      return ret.toFixed(2)
    },

    bannerWidth() {
      const m = this.questionResult.question_answer_count
      if (m === 0) {
        return 0
      }
      const n = this.questionDetailResult[0].new_question_answer_count
      const ret = (n/m) * 100
      return `${ret.toFixed(2)}%`
    },

    bannerWidth2() {
      const m = this.questionResult.question_answer_count
      if (m === 0) {
        return 0
      }
      const n = this.questionDetailResult[0].new_question_answer_count
      const ret = (n/m) * 100
      return `${100 - ret.toFixed(2)}%`
    },

    bannerStyle() {
      return {
        'width': this.bannerWidth
      }
    },

    bannerStyle2() {
      return {
        'width': this.bannerWidth2
      }
    }

  },
  methods: {
    ...mapActions(['fetchQuestionResult', 'fetchDetailQuestionResult', 'voteQuestion']), 
    fetchDetailData(qId, vId) {
      this.fetchDetailQuestionResult({questId: qId, voteId: vId})
      this.pick = this.questionDetailResult
    },
    pickTrue() {
      this.fetchDetailData(1, 0)
      this.voteQuestion({questId: 1, choice: 1})
      this.fetchDetailData(1, 0)
    },
    pickFalse() {
      this.fetchDetailData(1, 0)
      this.voteQuestion({questId: 1, choice: 0})
      this.fetchDetailData(1, 0)
    },
  },
  created() {
    this.fetchQuestionResult(1) // 전체 질문들을 조회할 방법을 생각해봐야할 듯..?
    this.fetchDetailData(1, 0) // 1번 주제에 대해 false(0) 데이터 출력
  },
}
</script>

<style scoped>

 .topic{ 
    text-decoration: none;
    padding: 20px 50px;
    border: 5px outset #e92964;
    border-radius: 10px;
    margin-bottom: 20px;
}

.topic:hover{
    animation: pulsate 1s 
    ease-in-out; 
}

@keyframes pulsate {
    0%{
        box-shadow: 
        0 0 10px #e92964,
        0 0 10px #e92964;
    }
} 

 .wrapper{
   letter-spacing: 3px;
   height: 100px;
   display: flex;
   align-items: center;
   justify-content: center;
 }

 .typing-demo{
   /* 나오는 길이 */
   width: 15ch; 
   /* 속도 타자감 */
   animation: typing 2s steps(7), blink .5s step-end infinite alternate;
   white-space: nowrap;
   overflow: hidden;
   border-right: 3px solid;
   font-family: monospace;
   font-size: 2em;
 }

 @keyframes typing{
   from{
     width: 0;
   }
 }

 @keyframes blink{
   50%{
     border-color: transparent;
   }
 }

</style>
<template>
<!-- 네브바에 stick-top을 넣을지 말지 결정 : 고정 버튼 없다면 있는게 나을 듯 함-->
  <footer>
    <!-- 3. 본인 이름 작성 -->
    <div style="background-color:rgb(230, 230, 230); font-size: 13px; ">
      <div style="text-align:center;  margin-top:20px; color:grey">
        <div style="padding-top: 5px; padding-bottom: 2px;">REMO</div>
        <div style="padding-bottom: 2px;">SSAFY 7기</div>
        <div class="name" style="width:12.5%; font-size: 15px;">SiWon Park | HyeonJeong Lee</div>
        <div style="padding-top: 2px; padding-bottom: 10px;">© 2022 All Rights Reserved.</div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'FootBar',
  data() {
    return {
    }
  }

}
</script>

<style scoped>

 .name{
  background: linear-gradient(45deg, #9a9ae3, #ba68ed);
  animation: hue-rotate 2s linear infinite alternate;
  color: rgb(26, 26, 26);
  border-radius: 5px;
  display: inline-block;

}

@keyframes hue-rotate {
  to{ filter: hue-rotate(90deg)}
}

</style>
<template>
  <div>
    <h1>영화 생성</h1>
    <div class="container">
      <form class="row g-3">
        <div class="col-md-6">
          <label for="title" class="form-label">영화 제목</label>
          <input type="text" class="form-control" id="title">
        </div>
        <div class="col-md-6">
          <label for="release_date" class="form-label">개봉일</label>
          <input type="date" class="form-control" id="release_date">
        </div>

        <div class="form">
          <label for="overview">영화 내용</label>
          <textarea class="form-control" placeholder="영화 내용" id="overview" style="height: 100px"></textarea>
        </div>
        <div class="col-12">
          <label for="poster_path" class="form-label">포스터</label>
          <input type="text" class="form-control" id="poster_path" placeholder="poster_path">
        </div>
        <div class="col-12">
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="gridCheck">
            <label class="form-check-label" for="gridCheck">모험</label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="gridCheck">
            <label class="form-check-label" for="gridCheck">판타지</label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="gridCheck">
            <label class="form-check-label" for="gridCheck">애니메이션</label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="gridCheck">
            <label class="form-check-label" for="gridCheck">서부</label>
          </div>
        </div>
        <div class="col-12">
          <button type="submit" class="btn btn-primary text-white">등록</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
export default {
  name: "MovieCreation",
  // 새로운 데이터일 경우 빈 객체 생성
  // 아닐 경우 업데이트
  methods: {
    ...mapActions(['createMovie',]),
  },
  
}
</script>

<style>

</style>
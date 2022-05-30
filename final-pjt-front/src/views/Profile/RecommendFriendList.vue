<template>
  <div class="card mb-3" style="max-width: 540px; height: 200px">
    <div class="row g-0">
      <div class="col-sm-4" style="margin-top: 40px;">
        <img src="@/assets/logo2.png" class="img-fluid rounded-start" alt="...">
      </div>
      <div class="col-sm-8">
        <div class="card-body">
          <div class="card-title" style="margin-bottom: 10px; font-size:20px; font-weight:bold;">{{friend.username}}</div>
          <div class="card-text">
            <p style="margin-bottom: 5px;">성별 |  {{friend.sex}}</p>
            <p>나이 | {{new Date().getFullYear() - friend.birth_date.slice(0, 4)}}세</p>
          </div>
          <router-link :to="{ name: 'PersonalProfile', params: { userId: friend.id } }">
            <button class="update">프로필 상세 보기</button>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RecommendFriendList',
  props: {
    friend: Object,
  }
}
</script>

<style scoped>

.container{
height: 100vh;
}

.card{
width: 380px;
border: solid aliceblue 1px;
border-radius: 15px;
padding: 8px;
background-color: #fff;
position: relative;
height: 370px;
}

.upper{
height: 100px;
}

.upper img{
width: 100%;
border-top-left-radius: 10px;
border-top-right-radius: 10px;
}

.user{
position: relative;
}

.profile img{
height: 80px;
width: 80px;
margin-top:2px;
}

.profile{
position: absolute;
top:-50px;
left: 38%;
height: 90px;
width: 90px;
border:3px solid #fff;
border-radius: 50%;
}

.follow{
border-radius: 15px;
padding-left: 20px;
padding-right: 20px;
height: 35px;
}

.stats span{

font-size: 29px;
}

  .update{
    background-color: #E92964;
    box-shadow: #BC41AB 4px 4px 0px;
    border-radius: 5px;
    transition: transform 200ms, box-shadow 200ms;
    color : #fff;
    width: 120px;
    height: 40px;
    text-align: center;
    outline: none;
  }

  .update:active{
    transform: translateY(4px) translateX(4px);
    box-shadow: #BC41AB 0px 0px 0px;
  }
  
</style>
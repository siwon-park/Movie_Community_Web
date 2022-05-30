<template>
<div class="row py-5 px-4">
  <!-- 프로필 부분 -->
  <div class="col-sm-8">
    <div class="col">
      <div class="bg-white shadow rounded overflow-hidden">
        <div class="d-flex">
          <!-- 사진 + 이름 + 장소 -->
          <div class="name" style="height:250px; width:250px ">
            <div class="media align-items-end profile-head">
              <div class="about">
                <div class="profile" style="text-align:center">
                  <!-- 프로필 이미지 -->
                  <img src="@/assets/logo2.png" alt="..." width="180" class="rounded">
                </div>
              </div>
              <div class="text-white d-flex justify-content-evenly" style="margin-top: 20px;">
                <div class="mt-0 mb-0">{{currentUser.username}}</div>
                <div class="small mb-4"><i class="fas fa-map-marker-alt fa-lg" style="color:blue;"></i> {{currentUser.region}}</div>
              </div>
            </div>
          </div>
          <!-- About -->
          <div style="margin-left: 30px; margin-top: 20px;">
            <div class="d-flex" style="margin-bottom: 35px;">
              <div style="font-size:23px; font-weight:bold; margin-right: 50px; margin-top: 15px;">{{currentUser.username}}</div>
              <div class="d-flex" >
              <div>
                <div style="text-align:center; font-weight:bold;">{{this.movieList.user_rated_movie_count}}</div>
                <div style="margin-top:5px; margin-right:20px">⭐평점 매긴 영화</div>
              </div>
              <div>
                <div style="text-align:center; font-weight:bold;">{{this.movieList.like_movies_count}}</div>
                <div style="margin-top:5px; margin-right:20px">👍🏻좋아요를 누른 영화</div>
              </div>
              <div>
                <div style="text-align:center; font-weight:bold;">{{this.movieList.wish_moives_count}}</div>
                <div style="margin-top:5px; margin-right:20px">🔖위시리스트 영화</div>
              </div>
              <div>
                <div style="text-align:center; font-weight:bold;">{{ followersCount }}</div>
                <div style="margin-top:5px; margin-right:20px">🐦팔로잉</div>
              </div>
              <div>
                <div style="text-align:center; font-weight:bold; margin-top:5px;">{{ followingsCount }}</div>
                <div> <i class="fas fa-user-friends fa-lg"></i>팔로워</div>
              </div>
              </div>
            </div>
            <div>
              <div style="margin-top: 10px;"> 🍰 생년월일 | {{ currentUser.birth_date }}</div>
              <div style="margin-top: 10px;"> <i class="fa-solid fa-mars-and-venus fa-lg" style="color:purple;"></i> 성별 | {{ currentUser.sex }}</div>
              <div style="margin-top: 10px;"> <i class="fas fa-dizzy fa-lg"></i> 싫어하는 장르 {{ currentUser.hate_genres_count}}</div> 
              <div>
                <div v-if="!isHates" style="margin-top: 15px; margin-left:15px; margin-right:-60px">{{currentUser.username}}님은 싫어하는 장르가 없습니다</div>
                <div style="margin-top: 10px; margin-left:15px; margin-right:-60px" v-if="isHates" class="d-flex justify-content-between">
                  <div class="d-flex">
                    <div v-for="h_genre in hateGenres.hate_genres" :key="h_genre.id">
                    <button class="btn btn-outline-danger hate" style="margin-left:10px">{{h_genre.name}}</button>
                    </div>
                  </div>
                </div>
            </div>
            <button class="update" style="margin-top:15px; margin-left:25px;">
                <router-link style="text-decoration: none; color:white;" to="/profile/edit">프로필 수정</router-link>
            </button>
            </div><!--about끝-->
          </div> 
      </div>
        <!-- 영화 정보 -->
        <div class="py-4 px-4">
          <div class="d-flex align-items-center justify-content-between mb-3">
            <h5 style="font-weight:bold; margin-left:10px">{{ sortRet }} 영화</h5>
            <div class="dropdown">
              <button class="btn dropdown-toggle movie_update" style="border: 1px solid #e92964;" type="button" id="dropdownMenuButton2" data-bs-toggle="dropdown" aria-expanded="false">
                {{currentUser.username}} 님의 영화정보
              </button>
              <ul class="dropdown-menu" style="border: 1px solid #e92964;" aria-labelledby="dropdownMenuButton2">
                <li><a class="dropdown-item" @click="sortBtn('like_movies', '좋아요를 누른')">좋아요를 누른 영화</a></li>
                <li><a class="dropdown-item" @click="sortBtn(2, '좋아요 기반 추천')">좋아요 기반 추천 영화</a></li>
                <li><a class="dropdown-item" @click="sortBtn(3, '평점 기반 추천')">평점 기반 추천 영화</a></li>
                <li><a class="dropdown-item" @click="sortBtn('wish_moives', '위시리스트')">위시리스트 영화</a></li>
                <li><a class="dropdown-item" @click="sortBtn('user_rated_movie', '평점을 준')">평점을 준 영화</a></li>
              </ul>
            </div>
          </div>
          <!-- 영화 출력 -->
          <div class="p-4 rounded shadow-sm bg-light">
            <div class="row">
              <div v-if="rcmdToggle === 1" class="container-fluid">
                <Flicking
                :options="{ circular: true }"
                :plugins="plugins"
                >
                <PersonalMovie v-for="movie in movieList[this.keyvalue]"
                :key="movie.id"
                :movie="movie"></PersonalMovie>
                <div slot="viewport" class="flicking-pagination"></div>
                <span slot="viewport" class="flicking-arrow-prev is-circle"></span>
                <span slot="viewport" class="flicking-arrow-next is-circle"></span>
                </Flicking>
              </div>
              <div v-if="rcmdToggle === 2" class="container-fluid">
                <Flicking
                :options="{ circular: true }"
                :plugins="plugins"
                >
                <PersonalMovie v-for="movie in likeRecommendMovies"
                :key="movie.id"
                :movie="movie"></PersonalMovie>
                <div slot="viewport" class="flicking-pagination"></div>
                <span slot="viewport" class="flicking-arrow-prev is-circle"></span>
                <span slot="viewport" class="flicking-arrow-next is-circle"></span>
                </Flicking>
              </div>
              <div v-if="rcmdToggle === 3" class="container-fluid">
                <Flicking
                :options="{ circular: true }"
                :plugins="plugins"
                >
                <PersonalMovie v-for="movie in rateRecommendMovies"
                :key="movie.id"
                :movie="movie"></PersonalMovie>
                <div slot="viewport" class="flicking-pagination"></div>
                <span slot="viewport" class="flicking-arrow-prev is-circle"></span>
                <span slot="viewport" class="flicking-arrow-next is-circle"></span>
                </Flicking>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- 친구 추천 부분 -->
  <div class="col-sm-4">
    <div class="col">
      <div class="bg-white shadow rounded overflow-hidden">
        <center>
          <h3 style="font-weight:bold;">추천 친구 목록</h3>
        </center>
        <div>
          <div v-if="recommendFriends !== ''" class="d-flex flex-column justify-content-center align-items-center">
            <RecommendFriendList
            v-for="friend in recommendFriends"
            :key="friend.id"
            :friend="friend"></RecommendFriendList>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import { Flicking } from '@egjs/vue-flicking'
import { Arrow } from "@egjs/flicking-plugins";
import { mapActions, mapGetters } from 'vuex'
import PersonalMovie from './PersonalMovie.vue'
import RecommendFriendList from './RecommendFriendList.vue'

export default {
  name: "ProfilePage",

  components: {
    Flicking,
    PersonalMovie,
    RecommendFriendList,
  },

  data() {
    return {
      userId: this.$route.params.userId,
      plugins: [new Arrow()],
      sortRet: '좋아요를 누른',
      keyvalue: 'like_movies',
      rcmdToggle: 1,
    }
  },

  computed: {
    ...mapGetters(['currentUser','movieList', 'hateGenres', 'likeRecommendMovies', 'rateRecommendMovies', 'recommendFriends']),
    followersCount() {
      return this.currentUser.followers?.length
    },
    followingsCount() {
      return this.currentUser.followings?.length
    },
    isHates() {
      return (this.hateGenres.hate_genres_count === 0) ? false : true
    },
  },

  methods: {
    ...mapActions(['fetchCurrentUser', 'fetchPersonalMovieList', 'fetchHateGenre', 'hateGenresPick', 'fetchRateRecommendMovies', 'fetchLikeRecommendMovies','fetchRecommendFriend' ]),
    
    genreInput(value) {
      this.hateGenresPick({userId:this.currentUser.id, genreId:value})
    },

    sortBtn(kv, srt) {
      if (kv === 2) {
          this.rcmdToggle = 2
        } else if (kv === 3) {
          this.rcmdToggle = 3
        } else {
          this.keyvalue = kv
          this.rcmdToggle = 1
        }
      this.sortRet = srt
    },

  },

  created() {
    this.fetchCurrentUser()
    this.fetchPersonalMovieList(this.currentUser.id)
    this.fetchLikeRecommendMovies(this.currentUser.id)
    this.fetchRateRecommendMovies(this.currentUser.id)
    this.fetchRecommendFriend(this.currentUser.id)
    this.fetchHateGenre(this.currentUser.id)
  },
}
</script>

<style scoped>
@import "@egjs/flicking-plugins/dist/arrow.css";
.my-block {
  background-color: black;
}

.profile-head {
    transform: translateY(3rem)
}


.is-circle {
  background-color:darkgray;
}


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

.hate{
    cursor:text;
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

  .movie_update{
    background-color: #E92964;
    box-shadow: #BC41AB 4px 4px 0px;
    border-radius: 5px;
    transition: transform 200ms, box-shadow 200ms;
    color : #fff;
    width: 175px;
    height: 40px;
    text-align: center;
    outline: none;
   

  }

  .movie_update:active{
    transform: translateY(4px) translateX(4px);
    box-shadow: #BC41AB 0px 0px 0px;
  }


  /*.cover {
      background-image: url(https://images.unsplash.com/photo-1530305408560-82d13781b33a?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1352&q=80); 
      background-size: cover;
      background: #654ea3;
      background: linear-gradient(to right, #e96443, #904e95);
      background-repeat: no-repeat
  }
  */
  
  /* body {
      background: #654ea3;
      background: linear-gradient(to right, #e96443, #904e95);
      min-height: 100vh;
      overflow-x:hidden;
  } */


</style>
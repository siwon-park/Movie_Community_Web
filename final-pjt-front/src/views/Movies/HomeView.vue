<template>
  <div style="margin-left: 10%; margin-right: 10%;">
    <div class="HomeView ">
      <div class="title" style="text-align:center; margin-top:40px">현재 상영작</div>
      <hr>
      <div class="container-fluid" style="margin-top: 40px">
        <Flicking
          class="slide"
          :options="{ circular: true }"
          :plugins="plugins"
        >
        <MainMovieCard v-for="mainMovie in mainMovies"
        :key="mainMovie.id"
        :mainMovie="mainMovie"></MainMovieCard>
        </Flicking>
      </div>
      <div>
        <!-- 영화 분류 제목 -->
        <div class="title" style="text-align:center; margin-top:75px ">{{this.recommend_movie_genre}} 추천 영화</div>
          <!-- 영화 예매 아이콘 영역 -->
          <div class="d-flex justify-content-end">
            <div>
              <center><div style="font-weight:bold; font-size:20px">영화 예매하러 가기</div></center>
              <div>
                <a href="http://www.cgv.co.kr/ticket/" target="_blank">
                  <img src="@/assets/images/logoRed.png" width="60px" alt="" style="margin-right: 30px;">
                </a>
                <a href="https://www.lottecinema.co.kr/NLCMW/Ticketing/Cinema" target="_blank">
                  <img src="@/assets/images/lottecinema.png" width="80px" height="40px" alt="">
                </a>
                <a href="https://www.megabox.co.kr/booking?rpstMovieNo=" target="_blank">
                  <img src="@/assets/images/megabox.png" alt="">
                </a>
              </div>
            </div>
          </div>
      </div>

      <div>
        <div class="drop d-flex justify-content-evenly align-items-center" style="font-weight:bold; margin-top:20px; margin-bottom:20px; border: 1px solid #e92964;">
          <button class="cta" @click="sortBtn(1, '인기순')">인기순</button>
          <button class="cta" @click="sortBtn(2, '최신순')">최신순</button>
          <button class="cta" @click="sortBtn(3, '개봉 예정순')">개봉 예정순</button>
          <button class="cta" @click="sortBtn(4, '리뷰 많은순')">리뷰 많은순</button>
          <button class="cta " @click="sortBtn(5, '평점순')">평점순</button>
          <div class="btn-group">
            <button type="button" class="dropdown-toggle cta" data-bs-toggle="dropdown" aria-expanded="false">
              장르순
            </button>
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
      </div>
      <!-- 서브 무비  -->
      <v-app>
        <v-main>
          <v-container fluid>
            <div class="row row-cols-4 row-cols-md-5 gy-3">
              <SubMovieCard v-for="subMovie in subMovies"
              :key="subMovie.id"
              :subMovie="subMovie"
              ></SubMovieCard>
            </div>
          </v-container>
        </v-main>
      </v-app>
    </div>
  </div>
</template>

<script>
import { Flicking } from '@egjs/vue-flicking'
import { Fade, Perspective, AutoPlay } from '@egjs/flicking-plugins'
import { mapActions, mapGetters } from 'vuex'
import MainMovieCard from '@/components/Movies/MainMovieCard.vue'
import SubMovieCard from '@/components/Movies/SubMovieCard.vue'

export default {
  name: 'HomeView',
  components: {
    Flicking: Flicking,
    MainMovieCard,
    SubMovieCard,
  },
  computed: {
    ...mapGetters(['mainMovies', 'subMovies', 'currentUser', 'movieList']),
  },
  methods: {
    ...mapActions(['main_movie_load', 'sub_movie_load', 'fetchPersonalMovieList', 'fetchRate',]),
    sortBtn(v, genre_pick) {
      this.sub_movie_load(v)
      this.recommend_movie_genre = genre_pick
    },
  },
  data() {
    return {
      movie_gerne: "",
      plugins: [new Fade(), new Perspective({ rotate: -1 }), new AutoPlay({ duration: 2000, direction: "NEXT", stopOnHover: false })],
      recommend_movie_genre: '인기순',
    }
  },
  created() {
    this.main_movie_load()
    this.sub_movie_load(1)
    this.fetchPersonalMovieList(this.currentUser.id)
    this.fetchRate(this.currentUser.id)
  },
}
</script>

<style scoped>
 @import "@egjs/vue-flicking/dist/flicking.css";


 .cta{
    font-size: 22px;
    display: inline-block;
    text-decoration: none;
    text-transform: uppercase;
    outline: 2px solid #FFF;
    padding: 1px 20px;
    position: relative;
    overflow: hidden;
    transition: color 1s;
}

.cta:hover{
    color: #fff;
}

.cta::before{
    content: '';
    position: absolute;
    top: 0;
    left: -50px;
    width: 150%;
    height: 100%;
    background-color: #E92964;
    color:#fff;
    transform: scaleX(0) skewX(35deg);
    transform-origin: left;
    z-index: -1;
    transition: transform 1s;
}

.cta:hover::before{
    transform: scaleX(1.5) skewX(35deg);
} 


.animated-background{
    background: linear-gradient(
        to right, #833ab4,
        #fd1d1d, #fcb045); 
    background-size: 400% 400%;
    animation: animate-background 10s infinite ease-in-out;
}

@keyframes animate-background {
  0%{
    background-position: 0 50%;
    }
    50%{
      background-position: 100% 50%;
    }
    100%{
      background-position: 0 50%;
    }
}

  .title {
    font-family: 'Do Hyeon', sans-serif;
    }


/* 그라데이션 글씨색 */
.title{
  letter-spacing: 0px;
  background: linear-gradient(45deg, deepskyblue, deeppink, deepskyblue, deeppink);
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
  font-size: 70px;
}

  /* #hover시 태그 효과 
  .link::before{
    content: '#';
    display: inline-block;
    width: 0.75em;
    color: #888888;
    opacity: 0;
    transition: opacity 200ms;
  }

  .link:hover{
    transform: none;
  }

  .link:hover::before{
    opacity: 1;
  } */


/* 입체글씨 */
  /* .reco{
    transform: skewY(-4edge);
    color: #E92964;
    text-shadow: #ff8cae 4px 4px, #ffdef7 8px 8px;
    font-size: 50px;

  }

  .link{
    transform: translateX(-0.75em);
    transition: transform 200ms;
  } */
</style>
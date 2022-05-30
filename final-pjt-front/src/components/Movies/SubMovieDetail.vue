<template>
  <v-app>
    <v-main>
      <v-container fluid>
        <div>
          <v-row>
            <v-col cols="12" sm="4">
              <v-img
              :src="`https://image.tmdb.org/t/p/original${subMovieDetail.poster_path}`"
              class="card-img"
              height=100%
              width="400"
              style="border-radius: 10px;"
              ></v-img>
            </v-col>

            <v-col cols="12" sm="8">
              <v-card-text>
                <div>
                  <div>
                    <div class="reco" style="font-size:40px; margin-top: 15px; ">{{subMovieDetail.title}}</div>
                  </div>

                  <div class="d-flex justify-content-start;" style="font-size: 20px; margin-top: 30px;">
                    <div > 개봉일: {{subMovieDetail.release_date}}</div>
                    <div style="margin-left: 10px;">
                      <i class="fa-solid fa-star fa-lg" style="color:orange;" ></i>
                      {{subMovieDetail.vote_average}}
                    </div>
                  </div>
                </div>
              </v-card-text >
              <div style="margin-left:5px" >
                <div style="margin-left:10px" class="btn btn-outline-danger" v-for="genre in subMovieDetail.genre_check" :key="genre.id">
                  {{genre.name}}
                </div>
              </div>
              <v-card-text style="padding-top: 40px; padding-bottom: 10px;">
                <h3 style="font-weight: 800;">줄거리</h3>
                <div style="font-size: 15px;">
                  {{subMovieDetail.overview}}
                </div>
              </v-card-text>
              <v-card-text style="padding-top: 30px; padding-bottom: 10px;">
                <h3 style="font-weight: 800;">관련 리뷰글 ({{review_count}})</h3>
                <ul style="padding-left: 0px;">
                  <div style="font-size: 15px; text-decoration: none;">
                    <li style="list-style-type:none" v-if="review_count === 0">관련 리뷰가 없습니다.</li>
                  </div>
                  <div v-if="review_count !== 0">
                    <li style="list-style-type:none" v-for="review in subMovieReviews.write_movie_review"
                    :key="review.id">
                    <router-link :to="{ name: 'review', params: {reviewId: review.id } }" class="link" style="color: black; font-size: 15px; text-decoration: none;">
                      {{ review.title }}
                    </router-link>
                    </li>
                  </div>
                </ul>
              </v-card-text>
              <v-card-text style="padding-top: 30px; padding-bottom: 10px;">
                <h3 style="font-weight: 800;">{{this.currentUser.username}}의 평점 : {{getRate}}</h3>
                <div class="dropdown" style="color:pink;">
                  <button class="btn btn-outline-danger dropdown-toggle"  type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
                    평점 수정
                  </button>
                  <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                    <li><a class="dropdown-item" @click="reRateScore(0)" style="color:pink;">☆☆☆☆☆</a></li>
                    <li><a class="dropdown-item" @click="reRateScore(1)" style="color:pink;">★☆☆☆☆</a></li>
                    <li><a class="dropdown-item" @click="reRateScore(2)" style="color:pink;">★★☆☆☆</a></li>
                    <li><a class="dropdown-item" @click="reRateScore(3)" style="color:pink;">★★★☆☆</a></li>
                    <li><a class="dropdown-item" @click="reRateScore(4)" style="color:pink;">★★★★☆</a></li>
                    <li><a class="dropdown-item" @click="reRateScore(5)" style="color:pink;">★★★★★</a></li>
                  </ul>
                </div>
              </v-card-text>
            </v-col>
          </v-row>
          
          <v-row>
            <div class="reco" style="margin-top: 50px; font-size: 50px; text-align:center; margin-bottom:20px">유사 장르 추천 영화</div>
            <div style="margin-bottom: 50px;" class="d-flex justify-content-around align-items-center">
              <div class="block">
                <v-img :src="`https://image.tmdb.org/t/p/original${subMovieRelated[0].poster_path}`" class="fill image"></v-img>
                <h5>{{subMovieRelated[0].title}}</h5>
              </div>
              <div class="block">
                <v-img :src="`https://image.tmdb.org/t/p/original${subMovieRelated[1].poster_path}`" class="fill image"></v-img>
                <h5>{{subMovieRelated[1].title}}</h5>
              </div>
              <div class="block">
                <v-img :src="`https://image.tmdb.org/t/p/original${subMovieRelated[2].poster_path}`" class="fill image"></v-img>
                <h5>{{subMovieRelated[2].title}}</h5>
              </div>
            </div>
          </v-row>
        </div>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
export default {
  name:"SubMovieDetail",
  props: {
    subMovieDetail: {
      type: Object,
    },
    subMovieReviews: {
      type: Object,
    },
    subMovieRelated: {
      type: Array,
    },
  },
  computed: {
    ...mapGetters(['movieRate', 'rateList', 'currentUser']),
    review_count() {
      return this.subMovieReviews.write_movie_review?.length
    },
    getRate() {
      for(const rate_res of this.rateList.user_rated) {
        if (rate_res.rate_movie === this.subMovieDetail.id) {
          return rate_res.rate_score
        }
      }
      return 0
    },
    getRateId() {
      for(const rate_res of this.rateList.user_rated) {
        if (rate_res.rate_movie === this.subMovieDetail.id) {
          return rate_res.id
        }
      }
      return 0
    },

  },
  methods: {
    ...mapActions(['reRateMovie', 'fetchRate']),
    reRateScore(score) {
      const rerate = { movieId: this.subMovieDetail.id, rateId: this.getRateId, rate_score:score }
      this.reRateMovie(rerate)
      this.fetchRate(this.currentUser.id)
      this.fetchRate(this.currentUser.id)
    },
  }
}
</script>

<style scoped>
  .block .fill {
    object-fit: cover;
    height: 350px;
    width: 250px;
  }

  .btn{
    cursor:text;
  }
  
/* 입체 글씨 */
  .reco {
  font-family: 'Do Hyeon', sans-serif;
  }

/* 영화 제목 hover */
  .block{
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    float: right;
    overflow: hidden;
    border-radius: 10px;
  }

  .block v-img{
    transition: all ease-in-out .3s;
  }

  .block:hover v-img{
    transform: scale(1.5);
  }

  .block h5{
    position: absolute;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 150px;
    height: 150px;
    border: 2px solid #E92964;
    border-radius: 50%;
    font-size: 14px;
    font-weight: 800;
    text-align: center;
    color: #E92964;
    background-color: #222831;
    z-index: 11;
    transform: scale(.1);
    transition: all ease-in-out .3s;
    cursor: pointer;
    opacity: 0;
  }

  .block:hover h5{
    transform: scale(1);
    opacity: 1;
  }

  .block::before{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    color: #222831;
    background: rgba(57, 62, 70, .4);
    z-index: 1;
    transition: all ease-in-out .3s;
    opacity: 1;
  }

</style>
<template>
  <v-app>
    <div style="margin-left: 25%; margin-right: 25%;">
      <ul>
        <div class="d-flex justify-content-between" style="font-size: 18px; margin-bottom:20px">
          <div class="btn-group">
            <button  type="button" class="dropdown-toggle cta" data-bs-toggle="dropdown" aria-expanded="false">
              정렬
            </button>
            <ul class="dropdown-menu" style="border: 1px solid #e92964;">
              <li><a class="dropdown-item" @click="sortBtn(1)">최신순</a></li>
              <li><a class="dropdown-item" @click="sortBtn(2)">좋아요</a></li>
              <li><a class="dropdown-item" @click="sortBtn(3)">댓글 많은 순</a></li>
            </ul>
          </div>  
          <router-link to="/new" class="article">New Article →<i class="arrow"></i></router-link>
        </div>
        <!-- 정렬 됐으면 출력 -->
        <div v-if="isSorted === true">
          <li v-for="review in sortedReviews" :key="review.id">
            <div>
              <div class="oneline" style="margin-bottom: 10px;">
                <div>No.{{ review.id }} </div>
                <div v-if="review.write_review_movie">{{ review.write_review_movie.title }}</div>
              </div>

              <div>
                <div class="d-flex justify-content-between">
                  <router-link class="router"
                :to="{ name: 'review', params: {reviewId: review.id } }"> 
                  <p class="title" style="margin-top: 5px;">{{ review.title }} </p>
                </router-link>
                  <div>
                    <p class="heart icon">💟{{ review.like_count }}</p>
                    <p class="comment icon">💬{{ review.comment_count }}</p>
                  </div>
                </div>

                <div class="write d-flex justify-content-between">
                  <div>
                    <div style="margin-top: 10px; font-size: 17px;">{{ review.write_review_user.username }}</div>
                  </div>
                  <div style = "font-size: 13px; color:grey;" >
                    <p style="margin-bottom: 0px; ">created : {{ review.created_at }}</p>
                    <p>updated : {{ review.created_at }}</p>
                  </div>
                </div>
              </div>
            </div>
            <hr>
          </li>
        </div>
        <!-- 정렬되지 않았으면 출력 -->
        <div v-if="isSorted === false">
          <li v-for="review in reviews" :key="review.id">
            <div>
              <div class="oneline" style="margin-bottom: 10px;">
                <div>No.{{ review.id }} </div>
                <div v-if="review.write_review_movie">{{ review.write_review_movie.title }}</div>
              </div>

              <div>
                <div class="d-flex justify-content-between">
                  <router-link class="router"
                :to="{ name: 'review', params: {reviewId: review.id } }"> 
                  <p class="title" style="margin-top: 5px;">{{ review.title }} </p>
                </router-link>
                  <div>
                    <p class="heart icon">💟{{ review.like_count }}</p>
                    <p class="comment icon">💬{{ review.comment_count }}</p>
                  </div>
                </div>

                <div class="write d-flex justify-content-between">
                  <div>
                    <router-link :to="{ name: 'PersonalProfile', params: { userId: review.write_review_user.id } }">
                      <p style="margin-top: 10px; font-size: 17px;">{{ review.write_review_user.username }}</p>
                    </router-link>
                  </div>
                  <div style = "font-size: 13px; color:grey;" >
                    <p style="margin-bottom: 0px; ">created : {{ review.created_at }}</p>
                    <p>updated : {{ review.created_at }}</p>
                  </div>
                </div>
              </div>
            </div>
            <hr>
          </li>
        </div>
      </ul>
    </div>
  </v-app>
</template>

<script>
  import { mapActions, mapGetters } from 'vuex'

  export default {
    name: 'ReviewListView',
    data() {
      return {
        isSorted:false,
      }
    },
    computed: {
      ...mapGetters(['reviews', 'sortedReviews'])
    },
    methods: {
      ...mapActions(['fetchReviews', 'fetchSortedReviews']),
      sortBtn(v) {
        this.fetchSortedReviews(v)
        this.isSorted = !this.isSorted
      }
      
    },
    created() {
      this.fetchReviews()
    },
  }
</script>

<style scoped>

  .dropdown-item{
    color:black;
  }
  
  .write{
    display: inline;
  }

  ul{
    list-style: none;
  }

  p{
    margin-bottom: 10px;
  }
  .oneline div{
    display: inline;
    color: #e92964;
    font-size: 17px;
    font-weight: bolder;
    
  }
  .title{
    font-weight: bold;
  }

  .v-application .title{
    font-size: 23px !important;
  }

  .router{
    color:black;
  }

  .router:link {
    text-decoration: none;
    display: inline-block;
    position: relative;
    color: #fff;
  }

  .router:link::after{
    content: '';
    width: 100%;
    height: 1px;
    /* 밑줄 색상 */
    background-color: #e92964;
    border-radius: 4px;
    position: absolute;
    left: 0;
    bottom: 0;
    transform: scaleX(0);
    transform-origin: left;
    transition: transform .25s ease;
  }

  .router:link:hover::after{
    transform: scaleX(1);
  }

  .icon{
    display: inline-block;
    animation: float 3.5s ease-in-out infinite;
    cursor:text; 
  }
  .heart{
    animation-delay: 0s;
  }
  .comment{
    animation-delay: 0.8s;
  }

  .article{
    display: flex;
    align-items: center;
    color: #000;
    background-color: none;
    border: none;
    padding: 12px 18px;
    position: relative;
    text-decoration: none;
  }

  .article::before{
    content: "";
    position: absolute;
    top: 50%;
    transform: translateY(-50%)translateX(calc(100% + 4px));
    width: 45px;
    height: 45px;
    background:#e92964;
    border-radius: 50px;
    transition: transform .25s .25s cubic-bezier(0, 0, .5, 2), width .25s cubic-bezier(0, 0, .5, 2);
    z-index: -1;
  }

  .article:hover::before{
    width: 100%;
    transform: translateY(-50%) translateX(-18px);
    transition: transform .25s cubic-bezier(0, 0, .5, 2), width .25s .25s cubic-bezier(0, 0, .5, 2);
  }

  .article i{
    margin-left: 5px;
    transition: transform .25s .4s cubic-bezier(0, 0, .5, 2);
  }

  .article:hover{
    transform: translateX(3px);
  }

  @keyframes float{
    0%{
      transform: translateY(0);
    }
    50%{
      transform: translateY(-7px);
    }
    100%{
      transform: translateY(0);
    }
  }

</style>

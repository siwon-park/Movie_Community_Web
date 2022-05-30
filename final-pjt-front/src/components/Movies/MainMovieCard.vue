<template>
  <div class="card panel">
    <img :src="`https://image.tmdb.org/t/p/original${mainMovie.poster_path}`" class="img-fluid image" alt="...">
    <div class="middle">
      <div class="text-block">
        <h3>{{mainMovie.title}}</h3>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MainMovieCard",
  props: {
    mainMovie: {
      type: Object,
    }
  }

}
</script>

<style scoped>
.card {
  height: 500px;
}
.card:hover .image {
  opacity: 0.2;
}
.card:hover .middle {
  opacity: 2;
}
.middle {
  transition: .5s ease;
  opacity: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  text-align: center;
  
}
.text-block {
  color: #000;
  padding-left: 30px;
  padding-right: 20px;
  bottom: 20px;
  right: 20px;
  width: 500px;
  
}
.image {
  opacity: 1;
  transition: .5s ease;
  backface-visibility: hidden;
  height: 500px;
  object-fit: cover;
}

</style>
<template>
<div>
  <div class="card">
    <img :src="`https://image.tmdb.org/t/p/original${movie.poster_path}`" class="img-fluid image zoom" alt="...">
  </div>
  <div slot="viewport" class="flicking-pagination"></div>
</div>
</template>

<script>
export default {
  name: "PersonalMovie",
  props: {
    movie: {
      type: Object,
    },
  },
  data() {
    return {
      toggle: false,
    }
  },
  methods: {
    openModal() {
      console.log("hi")
      this.toggle = !this.toggle
    }
  },

}
</script>

<style scoped>
.card .image {
  height: 350px;
  width: 250px;
  object-fit: cover;
}

.zoom {
  transition: transform .2s; /* Animation */
  margin: 0 auto;
}

.zoom:hover {
  transform: scale(1.2);
}
</style>
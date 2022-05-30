<template>
  <v-app class="red lighten-2">
    <!-- <img class="not-found" src="@/assets/404.jpg" alt="not-found"> -->
    <v-alert
      dense
      outlined
      type="error"
    >
    <h1>404 Not Found</h1>
    </v-alert>
  </v-app>
</template>

<script>
  export default {
    name: 'NotFound404',
  }
</script>

<style>
  img.not-found {
    width: 100%;
  }
</style>

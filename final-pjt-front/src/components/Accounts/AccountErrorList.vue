<template>
  <div>
    <v-alert
      dense
      outlined
      type="error"
    >
    <p v-for="(errors, field) in authError" :key="field">
      {{ field }}
      <ul>
        <li v-for="(error, idx) in errors" :key="idx">
          {{ error }}
        </li>
      </ul>
    </p>
    </v-alert>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'AccountErrorList',
  computed: {
    ...mapGetters(['authError'])
  },
}
</script>

<style>
  .account-error-list {
    color: red;
  }
</style>

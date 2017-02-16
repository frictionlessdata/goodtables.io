<script>
export default {
  props: {
    userName: String,
    userEmail: String,
  },
}
</script>

<template>
<div class="container">
  <h1>User</h1>
  <ul>
    <li>Name - {{ userName }}</li>
    <li v-if="userEmail">Email - {{ userEmail }}</li>
  </ul>
</div>
</template>

<style scoped>
</style>

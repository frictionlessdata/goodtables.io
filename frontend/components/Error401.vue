<script>
export default {
  name: 'Error401',
  props: {
    message: String,
  },
}
</script>

<template>
<div class="container">
  <h1>Not Authorized</h1>
  <p v-if:message>{{ message }}</p>
</div>
</template>

<style scoped>
</style>

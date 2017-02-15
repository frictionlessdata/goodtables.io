<script>
export default {
  props: {
    messages: Array,
  },
}
</script>

<template>
<div class="container">
  <div v-for="message of messages" :class="`alert alert-${message[0]}`" role="alert">
    {{ message[1] }}
  </div>
</div>
</template>

<style scoped>
</style>

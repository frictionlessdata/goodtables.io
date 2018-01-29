<script>
export default {
  name: 'Messages',
  props: {
    messages: Array,
  },
}
</script>

<template>
<div v-if="messages.length" class="messages">
  <div v-for="message of messages" :class="`alert alert-${message[0]}`" role="alert">
    {{ message[1] }}
  </div>
</div>
</template>

<style scoped>
</style>

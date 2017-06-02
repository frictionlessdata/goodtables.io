<script>
export default {
  name: 'MessageGroup',
  data() {
    return {
      isExpanded: false,
    }
  },
  props: {
    type: String,
    title: String,
    messages: Array,
    expandText: String,
  },
}
</script>

<template>
<div :class="`alert alert-${type}`" role="alert">
  <span @click="isExpanded = !isExpanded" class="title" >{{ title }}</span>
  <a @click="isExpanded = !isExpanded" class="show-details">{{ expandText }}</a>
  <template v-if="isExpanded">
    <hr /><ul><li v-for="message of messages">{{ message }}</li></ul>
  </template>
</div>
</template>

<style scoped>
.title {
  cursor: pointer;
}
.title:hover {
  text-decoration: underline;
}
.show-details {
  float: right;
  color: #2f3135;
}
</style>

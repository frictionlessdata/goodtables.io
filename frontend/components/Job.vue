<script>
const Report = (typeof goodtablesVue !== 'undefined') ? goodtablesVue.Report : null  // eslint-disable-line no-undef
export default {
  name: 'Job',
  props: {
    job: Object,
  },
  components: {
    Report,
  },
}
</script>

<template>
<div class="container">
  <Report v-if="job.report" :report="job.report" />
  <p v-else>There is an error in the job!</p>
</div>
</template>

<style scoped>
</style>

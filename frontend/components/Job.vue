<script>
export default {
  props: {
    job: Object,
  },
  components: {
    'app-report': goodtablesVue.Report,
  },
}
</script>

<template>
<div class="container">
  <app-report v-if="job.report" :report="job.report" />
  <p v-else>There is an error in the job!</p>
</div>
</template>

<style scoped>
</style>

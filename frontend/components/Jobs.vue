<script>
import JobList from './JobList.vue'

export default {
  name: 'Jobs',
  props: {
    jobs: Array,
  },
  components: {
    JobList,
  },
}
</script>

<template>
<div class="container">
  <h1>All Jobs</h1>

  <template v-if="jobs">
    <JobList :jobs="jobs" />
  </template>

  <template v-else>
    <p>No active or finished jobs.</p>
  </template>
</div>
</template>

<style scoped>
</style>

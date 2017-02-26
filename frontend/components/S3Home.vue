<script>
import JobList from './JobList.vue'

export default {
  name: 'S3Home',
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

  <h1>Amazon S3 Jobs</h1>

  <div style="margin-bottom: 30px" class="row">
    <div style="float: right">
      <a href="/s3/settings" class="btn btn-primary" style="width:120px;">Add bucket</a>
    </div>
  </div>

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

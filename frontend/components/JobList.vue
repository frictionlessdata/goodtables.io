<script>

export default {
  props: {
    jobs: Array,
  },
}
</script>

<template>
<div class="container">
  <div v-for="job of jobs" class="row">
    <a v-if="job.status === 'success'" :href="`/jobs/${job.id}`" class="btn btn-success">Valid</a>
    <a v-else-if="job.status === 'error'" :href="`/jobs/${job.id}`" class="btn btn-warning">Errored</a>
    <a v-else :href="`/jobs/${job.id}`" class="btn btn-danger">Invalid</a>

    <template v-if="job.integration_name === 'github'">
      <a :href="`/jobs/${job.id}`">{{ job.conf.repository.owner }}/{{ job.conf.repository.name }}</a> -
      (<a :href="`https://github.com/${job.conf.repository.owner}/${job.conf.repository.name}/commit/${job.conf.sha}`">{{ job.conf.sha.slice(0, 6) }}</a>)
    </template>

    <template v-else-if="job.integration_name === 's3'">
      <a :href="`/jobs/${job.id}`">{{ job.conf.bucket }}</a>
    </template>

    <small>({{ job.created }})</small>
  </div>
</div>
</template>

<style scoped>
.row {
  border-bottom: solid 1px #eee;
  padding: 5px 0;
}
.btn {
  widht: 80px;
}
small {
  color: #777;
}
</style>

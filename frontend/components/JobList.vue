<script>

import JobListItem from './JobListItem.vue'

export default {
  name: 'JobList',
  props: {
    jobs: Array,
  },
  components: {
    JobListItem,
  },
}

</script>


<template>
  <div>
    <JobListItem v-for="job in jobs" :job="job" />
  </div>
</template>

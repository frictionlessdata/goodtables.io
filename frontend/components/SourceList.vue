<script>

import SourceListItem from './SourceListItem.vue'

export default {
  name: 'SourceList',
  props: {
    jobs: Array,
    eventHub: Object,
    activeSourceIndex: {
      type: Number,
      default: 0,
    },
  },
  components: {
    SourceListItem,
  },
}

</script>


<template>
  <div>
    <SourceListItem
      v-for="(job, index) of (jobs || [])" 
      :job="job" 
      :eventHub="eventHub"
      :active="index === activeSourceIndex" />
  </div>

</template>

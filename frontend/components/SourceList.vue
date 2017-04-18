<script>

import SourceListItem from './SourceListItem.vue'

export default {
  name: 'SourceList',
  props: {
    sources: Array,
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
      v-for="(source, index) of (sources || [])" 
      :source="source" 
      :eventHub="eventHub"
      :active="index === activeSourceIndex" />
  </div>

</template>

<script>

import SourceListItem from './SourceListItem.vue'

export default {
  name: 'SourceList',
  props: {
    sources: Array,
  },
  components: {
    SourceListItem,
  },
}

</script>


<template>
  <div>
    <SourceListItem v-for="source in sources" :source="source" />
  </div>
</template>

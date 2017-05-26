<script>
import ReportTable from './ReportTable.vue'

export default {
  name: 'Report',
  props: {
    report: Object,
  },
  components: {
    ReportTable,
  },
}
</script>

<template>
<div class="report">

  <ul class="dataset-errors">
    <li v-for="warning of report.warnings">{{ warning }}</li>
  </ul>

  <template v-for="(table, index) of report.tables">
    <ReportTable :table="table" :tablesCount="report['table-count']" :tableNumber="index + 1" />
  </template>

</div>
</template>

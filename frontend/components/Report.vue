<script>
import Table from './Table.vue'

export default {
  name: 'Report',
  props: {
    report: Object,
  },
  components: {
    MyTable: Table,
  },
}
</script>

<template>
<div class="goodtables-vue-report">

  <ul class="dataset-errors">
    <li v-for="error of report.errors">{{ error.message }}</li>
  </ul>

  <template v-for="(table, index) of report.tables" v-if="!table.valid">
    <MyTable :table="table" :tablesCount="report['table-count']" :tableNumber="index + 1" />
  </template>

</div>
</template>

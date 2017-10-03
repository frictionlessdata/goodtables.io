<script>
import ReportTable from './ReportTable.vue'
import MessageGroup from './MessageGroup.vue'
import {removeBaseUrl} from '../helpers'

export default {
  name: 'Report',
  props: {
    report: Object,
  },
  components: {
    ReportTable,
    MessageGroup,
  },
  computed: {
    processedWarnings() {
      // Before `goodtables@1.0` there was no warnings property
      return (this.report.warnings || []).map(warning => removeBaseUrl(warning))
    },
    validTableFiles() {
      return this.report.tables
        .filter(table => table.valid)
        .map(table => removeBaseUrl(table.source))
    },
    invalidTables() {
      return this.report.tables.filter(table => !table.valid)
    },
  },
}
</script>

<template>
<div class="report">

  <MessageGroup v-if="processedWarnings.length"
                type="warning"
                :title="`There are ${processedWarnings.length} warning(s)`"
                expandText="Warning details"
                :messages="processedWarnings" />

  <MessageGroup v-if="validTableFiles.length"
                type="success"
                :title="`There are ${validTableFiles.length} valid table(s)`"
                expandText="Success details"
                :messages="validTableFiles" />

  <template v-for="(table, index) of invalidTables">
    <ReportTable :table="table" :tablesCount="invalidTables.length" :tableNumber="index + 1" />
  </template>

</div>
</template>

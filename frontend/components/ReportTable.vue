<script>
import ReportErrorGroup from './ReportErrorGroup.vue'
import {removeBaseUrl} from '../helpers'

export default {
  name: 'ReportTable',
  props: {
    table: Object,
    tableNumber: Number,
    tablesCount: Number,
  },
  components: {
    ReportErrorGroup,
  },
  computed: {
    errorGroups() {
      const groups = {}
      for (const error of this.table.errors) {

        // Get group
        let group = groups[error.code]

        // Create group
        if (!group) {
          group = {
            code: error.code,
            rows: {},
            count: 0,
            headers: this.table.headers,
            messages: [],
          }
        }

        // Get row
        let row = group.rows[error['row-number']]

        // Create row
        if (!row) {
          let values = error.row
          if (!error['row-number']) {
            values = this.table.headers
          }
          row = {
            values,
            badcols: new Set(),
          }
        }

        // Ensure missing value
        if (error.code === 'missing-value') {
          row.values[error['column-number'] - 1] = ''
        }

        // Add row badcols
        if (error['column-number']) {
          row.badcols.add(error['column-number'])
        } else if (row.values) {
          row.badcols = new Set(row.values.map((value, index) => index + 1))
        }

        // Save group
        group.count += 1
        group.messages.push(error.message)
        group.rows[error['row-number']] = row
        groups[error.code] = group

      }
      return groups
    },
    tableFile() {
      return removeBaseUrl(this.table.source)
    },
  },
}
</script>

<template>
<div class="report-table">

  <h4 class="file-heading">
    <span>
      <a class="file-name" :href="table.source">{{ tableFile }}</a>
      <span class="file-count">Invalid {{ tableNumber }} of {{ tablesCount }}</span>
    </span>
  </h4>

  <template v-if="!table.valid">
  <ReportErrorGroup v-for="errorGroup of errorGroups" :errorGroup="errorGroup" />
  </template>

  <template v-else-if="table.valid">
  <div class="result panel panel-success">
    <div class="panel-heading">
      <span class="text-uppercase label label-success">Valid</span>
    </div>
  </div>
  </template>

</div>
</template>

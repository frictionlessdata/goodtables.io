<script>
import ReportErrorGroup from './ReportErrorGroup.vue'

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
          }
        }

        // Get row
        let row = group.rows[error['row-number']]

        // Create row
        if (!row) {
          let values = error.row
          if (!error['row-number']) values = this.table.headers
          if (error.code === 'blank-row') values = this.table.headers.map(() => '')
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
        group.rows[error['row-number']] = row
        groups[error.code] = group

      }
      return groups
    },
    githubTableSourceName() {
      const source = this.table.source
      if (source.startsWith('https://raw.githubusercontent.com')) {
        return source.replace(/https:\/\/raw\.githubusercontent\.com\/\S*\/\S*\/[a-z0-9]{40}\//, '')
      }
      return source
    },
  },
}
</script>

<template>
<div>

  <h4 class="file-heading">
    <span>
      <a class="file-name" :href="table.source">{{ githubTableSourceName }}</a>
      <span class="file-count">Table {{ tableNumber }} of {{ tablesCount }}</span>
    </span>
  </h4>

  <template v-if="!table.valid">
  <ReportErrorGroup v-for="errorGroup of errorGroups" :errorGroup="errorGroup" />
  </template>

  <template v-else-if="table.valid">
  <div class="result panel panel-success">
    <div class="panel-heading">
      <span class="text-uppercase label label-success">Valid</span>
      <span class="help"
            rel="popover"
            data-toggle="popover"
            data-placement="left"
            data-content="No errors where found">
        <span class="icon-info"><i>What is this?</i></span>
      </span>
    </div>
  </div>
  </template>

</div>
</template>

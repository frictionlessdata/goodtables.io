<script>
import ErrorGroup from './ErrorGroup.vue'

export default {
  name: 'Table',
  props: {
    table: Object,
    tableNumber: Number,
    tablesCount: Number,
  },
  components: {
    ErrorGroup,
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
            name: error.code,
            type: 'type',
            rows: {},
            count: 0,
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
        } else {
          row.badcols = new Set(row.values.map((value, index) => index + 1))
        }

        // Save group
        group.count += 1
        group.rows[error['row-number']] = row
        groups[error.code] = group

      }
      return groups
    },
  },
}
</script>

<template>
<div>

  <h4 class="file-heading">
    <span>
      <a class="file-name" :href="table.source">{{ table.source }}</a>
      <a class="file-count" :href="table.source">Table {{ tableNumber }} of {{ tablesCount }}</a>
    </span>
  </h4>

  <ErrorGroup v-for="errorGroup of errorGroups" :errorGroup="errorGroup" />

</div>
</template>

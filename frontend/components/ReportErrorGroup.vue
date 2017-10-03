<script>
import marked from 'marked'
const spec = require('../spec.json')

export default {
  name: 'ReportErrorGroup',
  props: {
    errorGroup: Object,
  },
  data() {
    return {
      showErrorDetails: false,
      visibleRowsCount: 10,
    }
  },
  mounted: () => {
    if (typeof $ !== 'undefined') { // eslint-disable-line
      $('[rel="popover"]').popover({ // eslint-disable-line
        html: true,
      })
    }
  },
  computed: {
    errorDetails() {

      // Get code handling legacy codes
      let code = this.errorGroup.code
      if (code === 'non-castable-value') {
        code = 'type-or-format-error'
      }

      // Get details handling custom errors
      let details = spec.errors[code]
      if (!details) details = {
        name: 'Custom Error',
        type: 'custom',
        context: 'body',
        description: 'Custom Error',
      }

      return details
    },
    rowNumbers() {
      return Object.keys(this.errorGroup.rows)
        .map(item => parseInt(item, 10) || null)
        .sort((a, b) => a - b)
    },
    showHeaders() {
      return this.errorDetails.context === 'body'
    },
    description() {
      const description = this.errorDetails.description
        .replace('{validator}', '`goodtables.yml`')
      return marked(description)
    },
  },
}
</script>

<template>
<div class="result panel panel-danger">

  <div class="panel-heading">
    <span class="text-uppercase label label-danger">Invalid</span>
    <span class="text-uppercase label label-info">{{ errorDetails.type }}</span>
    <span class="count label">{{ errorGroup.count }}</span>
    <h5 class="panel-title">
      <a @click="showErrorDetails = !showErrorDetails">
        {{ errorDetails.name }}
      </a>
    </h5>
    <a @click="showErrorDetails = !showErrorDetails" class="error-details-link">
      Error details
    </a>
  </div>

  <div v-if="showErrorDetails" class="panel-heading error-details">
    <p><div v-html="description"></div></p>
  </div>

  <div v-if="showErrorDetails" class="panel-heading error-details">
    <p>The full list of error messages:</p>
    <ul><li v-for="message of errorGroup.messages">{{ message }}</li></ul>
  </div>

  <div class="panel-body">
    <div class="table-container">
      <table class="table table-bordered table-condensed">
        <thead v-if="showHeaders">
          <tr>
            <th></th>
            <th v-for="header of errorGroup.headers">{{ header }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="rowNumber, index of rowNumbers" v-if="index < visibleRowsCount " class="result-header-row">
            <td v-if="rowNumber !== null" class="result-row-index">{{ rowNumber }}</td>
            <td v-for="(value, index) of errorGroup.rows[rowNumber].values"
                :class="{danger: errorGroup.rows[rowNumber].badcols.has(index + 1)}">
              {{ value }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="show-more" v-if="visibleRowsCount < rowNumbers.length">
      <a @click="visibleRowsCount += 10">Show next 10 rows</a>
    </div>
  </div>
</div>
</template>

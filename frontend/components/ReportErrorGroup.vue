<script>
export default {
  name: 'ReportErrorGroup',
  props: {
    errorGroup: Object,
  },
  data() {
    return {
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
    rowNumbers() {
      return Object.keys(this.errorGroup.rows)
        .map(item => parseInt(item, 10) || null)
        .sort((a, b) => a - b)
    },
  },
}
</script>

<template>
<div class="result panel panel-danger">

  <div class="panel-heading">
    <span class="text-uppercase label label-danger">Invalid</span>
    <span class="count label">{{ errorGroup.count }}</span>
    <h5 class="panel-title">{{ errorGroup.name }}</h5>
    <span class="help"
          rel="popover"
          data-toggle="popover"
          data-placement="left"
          :title="`<span class='label label-info'>${errorGroup.type}</span> ${errorGroup.name}`"
          :data-content="`${errorGroup.name}. <a>Read more</a>`">
      <span class="icon-info"><i>What is this?</i></span>
    </span>
  </div>

  <div class="panel-body">
    <div class="table-container">
      <table class="table table-bordered table-condensed">
        <thead v-if="errorGroup.headers">
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

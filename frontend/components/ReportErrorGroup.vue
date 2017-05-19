<script>
export default {
  name: 'ReportErrorGroup',
  props: {
    errorGroup: Object,
  },
  mounted: () => {
    if (typeof $ !== 'undefined') { // eslint-disable-line
      $('[rel="popover"]').popover({ // eslint-disable-line
        html: true,
      })
    }
  },
}
</script>

<template>
<div class="result panel panel-danger">

  <div class="panel-heading">
    <span class="text-uppercase label label-danger">Invalid</span>
    <span class="count label">{{ (errorGroup.count < 10) ? errorGroup.count : `10/${errorGroup.count}` }}</span>
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
    <table class="table table-bordered table-condensed">
      <thead v-if="errorGroup.headers">
        <tr>
          <th>H</th>
          <th v-for="header of errorGroup.headers">{{ header }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="rowNumber, index of Object.keys(errorGroup.rows).sort()" v-if="index < 10 " class="result-header-row">
          <td class="result-row-index">{{ (rowNumber !== 'null') ? rowNumber : 'H' }}</td>
          <td v-for="(value, index) of errorGroup.rows[rowNumber].values"
              :class="{danger: errorGroup.rows[rowNumber].badcols.has(index + 1)}">
            {{ value }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>

</div>
</template>

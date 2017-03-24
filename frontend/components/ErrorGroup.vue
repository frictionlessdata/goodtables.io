<script>
export default {
  name: 'ErrorGroup',
  props: {
    errorGroup: Object,
  },
  mounted: () => {
    // $('[rel="popover"]').popover({
      // html: true,
    // })
  },
}
</script>

<template>
<div class="result panel panel-danger">

  <div class="panel-heading">
    <span class="text-uppercase label label-danger">error</span>
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
    <table class="table table-bordered table-condensed">
      <tbody>
        <tr v-for="rowNumber of Object.keys(errorGroup.rows).sort()" class="result-header-row">
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

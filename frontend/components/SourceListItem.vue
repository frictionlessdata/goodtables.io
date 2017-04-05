<script>

export default {
  name: 'JobListItem',
  props: {
    job: Object,
    active: Boolean
  },
  computed: {
    panelStatusClass: function() {
      return {
        'panel-success': this.job.status === 'success',
        'panel-danger': this.job.status === 'failure',
        'panel-warning': this.job.status === 'error',
        'active': this.active

      }
    },
    integrationIconClass: function() {
      return {
        'icon-github': this.job.integration_name == 'github',
        'icon-amazon': this.job.integration_name == 's3',

      }
    }
  }
}

</script>


<template>
  <div class="source-item panel" v-bind:class="panelStatusClass">
    <div v-bind:class="job.integration_name">
      <a class="source" v-bind:class="{active: active}">
        <span class="status">{{ job.status }} </span>

        <span v-if="job.status === 'success'" class="label label-success">
          <span class="icon-checkmark"><i>Valid</i></span>
        </span>
        <span v-else-if="job.status === 'failure'" class="label label-danger">
          <span class="icon-cross"><i>Invalid</i></span>
        </span>
        <span v-else-if="job.status === 'error'" class="label label-warning">
          <span class="icon-warning"><i>Error</i></span>
        </span>

          <h3 class="panel-title">

              <template v-if="job.integration_name === 'github'">
              {{ job.integration_name }}/{{ job.conf.owner }}/{{job.conf.repo }}
              </template>
              <template v-else-if="job.integration_name === 's3'">
              {{ job.integration_name }}/{{job.conf.bucket }}
              </template>
            <span class="jobnumber">#XX</span>
          </h3>
        </a>

        <a class="job"  v-bind:class="{active: active}">
          <span class="jobcount">
            <span class="jobnumber"> #XX</span>
            <span class="jobtotal"> of YY</span>
          </span>
          <span class="icon-clock"></span><span class="time"> TIME</span>
        </a>
        <a class="integration" v-bind:class="integrationIconClass"></a>
      </div>
  </div>

  </div>

</template>


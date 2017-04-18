<script>

export default {
  name: 'SourceListItem',
  props: {
    job: Object,
    eventHub: Object,
    active: Boolean,
    inSourcePanel: Boolean,
  },
  data() {
    return {
      isActive: this.active,
    }
  },
  computed: {
    panelStatusClass() {
      return {
        'panel-success': this.job.status === 'success',
        'panel-danger': this.job.status === 'failure',
        'panel-warning': this.job.status === 'error',
        active: this.isActive,

      }
    },
    integrationIconClass() {
      return {
        'icon-github': this.job.integration_name === 'github',
        'icon-amazon': this.job.integration_name === 's3',

      }
    },
  },
  methods: {
    onClickSourceItem() {
      this.eventHub.$emit('job:changed', this.job)
    },
    setActive(job) {
      this.isActive = job === this.job
    },
  },
  created() {
    if (!this.inSourcePanel) {
      this.eventHub.$on('job:changed', this.setActive)
    }
  },
}

</script>


<template>
  <div class="source-item panel" v-on:click="onClickSourceItem" v-bind:class="panelStatusClass">
    <div v-bind:class="job.integration_name">
      <a class="source" v-bind:class="{active: inSourcePanel}">
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

        <a class="job"  v-bind:class="{active: isActive || inSourcePanel}">
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


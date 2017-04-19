<script>

export default {
  name: 'SourceListItem',
  props: {
    source: Object,
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
        'panel-success': (this.source.last_job && this.source.last_job.status === 'success'),
        'panel-danger': (this.source.last_job && this.source.last_job.status === 'failure'),
        'panel-warning': (this.source.last_job && this.source.last_job.status === 'error'),
        'panel-info': !this.source.last_job,
        active: this.isActive,

      }
    },
    integrationIconClass() {
      return {
        'icon-github': this.source.integration_name === 'github',
        'icon-amazon': this.source.integration_name === 's3',

      }
    },
  },
  methods: {
    onClickSourceItem() {
      this.eventHub.$emit('source:changed', this.source)
    },
    setActive(source) {
      this.isActive = source === this.source
    },
  },
  created() {
    if (!this.inSourcePanel) {
      this.eventHub.$on('source:changed', this.setActive)
    }
  },
}

</script>


<template>
  <div class="source-item panel" v-on:click="onClickSourceItem" v-bind:class="panelStatusClass">
    <div v-bind:class="source.integration_name">
      <a class="source" v-bind:class="{active: inSourcePanel}">

        <template v-if="source.last_job">
        <span class="status">{{ source.last_job.status }} </span>

        <span v-if="source.last_job.status === 'success'" class="label label-success">
          <span class="icon-checkmark"><i>Valid</i></span>
        </span>
        <span v-else-if="source.last_job.status === 'failure'" class="label label-danger">
          <span class="icon-cross"><i>Invalid</i></span>
        </span>
        <span v-else-if="source.last_job.status === 'error'" class="label label-warning">
          <span class="icon-warning"><i>Error</i></span>
        </span>

        </template>

        <template v-if="!source.last_job">
        <span class="label label-info">
          <span class="icon-info"><i>No jobs yet</i></span>
        </span>
        </template>

          <h3 class="panel-title">
            {{ source.name }}

            <span v-if="source.last_job" class="jobnumber">#{{ source.last_job.number }}</span>
          </h3>
        </a>

        <a class="job"  v-bind:class="{active: isActive || inSourcePanel}">

          <template v-if="source.last_job">
          <span class="jobcount">
            <span class="jobnumber"> #{{ source.last_job.number }}</span>
          </span>
          <span class="icon-clock"></span><span class="time"> TIME</span>
          </template>

          <template v-if="!source.last_job">
          <span class="time">No jobs yet</span>
          </template>

        </a>

        <a class="integration" v-bind:class="integrationIconClass"></a>
      </div>
  </div>

  </div>

</template>


<script>
import SettingsGithub from './SettingsGithub.vue'
import SettingsS3 from './SettingsS3.vue'

export default {
  name: 'Settings',
  components: {
    SettingsGithub,
    SettingsS3,
  },
}
</script>

<template>
<div class="app add-view">
  <div class="inner">
    <section class="add-source">
      <header class="main-header">
        <ul class="nav nav-tabs" role="tablist">
          <li role="presentation" class="active"><a href="#addGithub" aria-controls="addGithub" role="tab" data-toggle="tab">GitHub</a></li>
          <li role="presentation"><a href="#addAmazon" aria-controls="addAmazon" role="tab" data-toggle="tab">Amazon</a></li>
        </ul>
      </header>
      <div class="tab-content">
        <div role="tabpanel" class="github tab-pane active" id="addGithub">
          <SettingsGithub />
        </div>
        <div role="tabpanel" class="amazon tab-pane" id="addAmazon">
          <SettingsS3 />
        </div>
      </div>
    </section>
  </div>
</div>
</template>

<style scoped>
</style>

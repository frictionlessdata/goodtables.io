<script>
import SettingsGithub from './SettingsGithub.vue'
import SettingsS3 from './SettingsS3.vue'
import SettingsTokens from './SettingsTokens.vue'

export default {
  name: 'Settings',
  components: {
    SettingsGithub,
    SettingsS3,
    SettingsTokens,
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
          <li role="presentation"><a href="#addTokens" aria-controls="addTokens" role="tab" data-toggle="tab">API Tokens</a></li>
        </ul>
      </header>
      <div class="tab-content">
        <div role="tabpanel" class="github tab-pane active" id="addGithub">
          <SettingsGithub />
        </div>
        <div role="tabpanel" class="amazon tab-pane" id="addAmazon">
          <SettingsS3 />
        </div>
        <div role="tabpanel" class="tokens tab-pane" id="addTokens">
          <SettingsTokens />
        </div>
      </div>
    </section>
  </div>
</div>
</template>

<style scoped>
</style>

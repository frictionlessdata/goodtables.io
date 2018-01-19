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

  <div class="sources only">

    <!-- Nav tabs -->
    <ul class="nav nav-tabs" role="tablist">
      <li role="presentation" class="active">
        <a href="#github" aria-controls="github" role="tab" data-toggle="tab">GitHub</a>
      </li>
      <li role="presentation">
        <a href="#amazon" aria-controls="amazon" role="tab" data-toggle="tab">Amazon</a>
      </li>
      <li role="presentation">
        <a href="#tokens" aria-controls="tokens" role="tab" data-toggle="tab">API Tokens</a>
      </li>
    </ul>

    <!-- Tab panes -->
    <div class="tab-content">
      <div role="tabpanel" class="tab-pane active" id="github">
        <SettingsGithub />
      </div>
      <div role="tabpanel" class="tab-pane active" id="amazon">
        <SettingsS3 />
      </div>
      <div role="tabpanel" class="tab-pane active" id="tokens">
        <SettingsTokens />
      </div>
    </div>

  </div>
</template>

<style scoped>
</style>

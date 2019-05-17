<script>
import Logo from './Logo.vue'
import Messages from './Messages.vue'

export default {
  name: 'App',
  components: {
    Logo,
    Messages,
  },
  props: {
    component: String,
    userName: String,
    baseUrl: String,
    githubId: Number,
    messages: Array,
  },
  computed: {
    avatarURL() {
      if (this.githubId) {
        return `https://avatars1.githubusercontent.com/u/${this.githubId}?s=52&v=4`
      }
    },
  },
}
</script>

<template>
  <div class="app">
    <div class="inner">
      <nav class="main-nav">

        <!-- Logo -->
        <Logo :baseUrl="baseUrl" />

        <!-- Navigation -->
        <ul v-if="userName" class="nav primary">
          <li :class="{active: component === 'Dashboard'}">
            <a href="/dashboard">
              <span class="icon-dashboard section-icon" aria-hidden="true"></span>
              <span class="text">Dashboard</span>
            </a>
          </li>
          <li :class="{active: component === 'Jobs', 'active-parent': component === 'Source'}">
            <a href="/jobs">
              <span class="icon-jobs section-icon" aria-hidden="true"></span>
              <span class="text">Jobs</span>
            </a>
          </li>
          <li :class="{active: component === 'Settings'}">
            <a href="/settings">
              <span class="icon-equalizer section-icon" aria-hidden="true"></span>
              <span class="text">Manage Sources</span>
            </a>
          </li>
        </ul>

        <!-- Description -->
        <div v-else class="text">
          <div class="description">
            <h3>What is goodtables.io?</h3>
            <p>
              <a href="https://goodtables.io">Goodtables.io</a> is a free online service for continuous data validation. It checks tabular data sources for structural problems, such as blank rows and, if available, checks the data against a <a href="https://frictionlessdata.io/specs/table-schema/">Table Schema</a>. Read more about it on <a href="https://goodtables.io">https://goodtables.io</a>.
            </p>
          </div>
        </div>

        <!-- Messages -->
        <Messages :messages="messages" />

        <!-- User -->
        <ul class="nav secondary">
          <li>
            <a href="https://docs.goodtables.io" rel="external">
              <span class="icon-info"></span>
              <span class="text">Help</span>
            </a>
          </li>
          <li class="feedback">
            <a
              href="#feedback"
              class="expand collapsed"
              data-toggle="collapse"
              aria-expanded="false"
              aria-controls="feedback"
            >
              <span class="icon-bubble"></span>
              <span class="text">Feedback</span>
            </a>
            <div class="nav-content collapse" id="feedback">
              <div>
                <p>To provide feedback or report an issue:</p>
                <ul>
                  <li>Give feedback <a href="https://discuss.okfn.org/t/launching-goodtables-io-tell-us-what-you-think" target="_blank">thread</a> on the Open Knowledge Foundation forum.</li>
                  <li>Open a bug report or a feature request on the <a href="https://github.com/frictionlessdata/goodtables.io/issues" target="_blank">goodtables.io issue tracker</a>.</li>
                  <li>Join our <a href="https://gitter.im/frictionlessdata/chat" target="_blank">chat room on Gitter, and talk to the team</a>.</li>
                </ul>
              </div>
            </div>
          </li>
          <li>
            <a href="https://okfn.org/privacy-policy/" rel="external">
              <span class="icon-list"></span>
              <span class="text">Privacy policy</span>
            </a>
          </li>
          <li v-if="userName" class="log-out">
            <a :href="`${baseUrl}/user/logout`">
              <img v-if="avatarURL" :src="avatarURL" alt="" />
              <span class="text">Log out</span>
            </a>
          </li>
          <li v-else class="log-in">
            <a :href="`${baseUrl}/user/login/github`">
              <span class="icon-login"></span>
              <span class="text">Log in</span>
            </a>
          </li>
        </ul>
      </nav>
      <div class="content">

        <!-- Contents -->
        <slot name="contents"></slot>

      </div>
    </div>
  </div>
</template>

<style scoped>
</style>

<!-- Import global styles -->
<style lang="scss" src="../styles/main.scss"></style>
<style lang="css" src="../../node_modules/goodtables-ui/dist/goodtables-ui.css"></style>

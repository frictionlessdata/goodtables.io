<script>
import Logo from './Logo.vue'
import Messages from './Messages.vue'
import loginImage from '../images/login.svg'

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
  data: () => {
    return {
      menuClass: 'default-menu-view',
      loginImage,
    }
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
  <div class="app" :class="menuClass">
    <div class="inner">
      <nav class="main-nav">

        <!-- Logo -->
        <Logo :baseUrl="baseUrl" />

        <!-- Navigation -->
        <ul v-if="userName" class="nav primary">
          <li :class="{active: component === 'Dashboard'}">
            <a href="/dashboard">
              <span class="icon-keyboard_arrow_left back-icon" aria-hidden="true"></span>
              <span class="icon-dashboard section-icon" aria-hidden="true"></span>
              <span class="text">Dashboard</span>
            </a>
          </li>
          <li :class="{active: component === 'Jobs', 'active-parent': component === 'Source'}">
            <a href="/jobs">
              <span class="icon-keyboard_arrow_left back-icon" aria-hidden="true"></span>
              <span class="icon-jobs section-icon" aria-hidden="true"></span>
              <span class="text">Jobs</span>
            </a>
          </li>
          <li :class="{active: component === 'Settings'}">
            <a href="/settings">
              <span class="icon-keyboard_arrow_left back-icon" aria-hidden="true"></span>
              <span class="icon-equalizer section-icon" aria-hidden="true"></span>
              <span class="text">Manage Sources</span>
            </a>
          </li>
        </ul>

        <!-- Description -->
        <div v-else class="text">
          <div class="description">
            <h3>What is goodtables.io?</h3>
            <p>goodtables.io is a free online service for continuous data validation. goodtables.io checks tabular data sources for structural problems, such as blank rows and non-tabular input, and optionally checks the data against a given schema, providing robust quality assurance for your data. goodtables.io supports many formats used for tabular data storage, including CSV, Excel, JSON, and ODS. Read more about the bad data problems goodtables.io can address <a href="http://okfnlabs.org/bad-data/" target="_blank">here</a>.</p>
          </div>
        </div>

        <!-- Messages -->
        <Messages :messages="messages" />

        <!-- User -->
        <ul class="nav secondary">
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
                  <li>Give feedback <a href="https://discuss.okfn.org/t/launching-goodtables-io-tell-us-what-you-think" target="_blank">thread</a> on the Open Knowledge International forum.</li>
                  <li>Open a bug report or a feature request on the <a href="https://github.com/frictionlessdata/goodtables.io/issues" target="_blank">goodtables.io issue tracker</a>.</li>
                  <li>Join our <a href="https://gitter.im/frictionlessdata/chat" target="_blank">chat room on Gitter, and talk to the team</a>.</li>
                </ul>
              </div>
            </div>
          </li>
          <li v-if="userName" class="log-out">
            <a :href="`${baseUrl}/user/logout`">
              <img v-if="avatarURL" :src="avatarURL" alt="" />
              <span class="text">Log out</span>
            </a>
          </li>
          <li v-else class="log-in">
            <a :href="`${baseUrl}/user/login/github`">
              <img :src="loginImage" alt="Login">
              <span class="text">Log in</span>
            </a>
          </li>
        </ul>

        <!-- Collapse -->
        <a v-on:click="menuClass = 'collapsed-menu-view'" class="collapse-view left">
          Collapse sidebar
        </a>

      </nav>
      <div class="content">

        <!-- Contents -->
        <slot name="contents"></slot>

        <!-- Collapse -->
        <a v-on:click="menuClass = 'default-menu-view'" class="expand-view right">
          Collapse sidebar
        </a>

      </div>
    </div>
  </div>
</template>

<style scoped>
</style>

<!-- Import global styles -->
<style lang="scss" src="../styles/main.scss"></style>
<style lang="css" src="../../node_modules/goodtables-ui/dist/goodtables-ui.css"></style>

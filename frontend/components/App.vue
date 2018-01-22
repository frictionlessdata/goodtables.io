<script>
import Logo from './Logo.vue'

export default {
  name: 'App',
  components: {
    Logo,
  },
  props: {
    component: String,
    userName: String,
    baseUrl: String,
  },
  data: () => {
    return {
      menuClass: 'default-menu-view',
    }
  }
}
</script>

<template>
  <div class="app" :class="menuClass">
    <div class="inner">
      <nav class="main-nav">

        <!-- Logo -->
        <Logo />

        <!-- Navigation -->
        <ul class="nav primary">
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

        <!-- User -->
        <ul class="nav secondary">
          <li class="feedback">
            <a class="expand collapsed" data-toggle="collapse" href="#feedback" aria-expanded="false" aria-controls="feedback"><img src="../images/feedback.svg" alt="">
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
              <img src="https://github.com/smth.png?size=52" alt="" />
              <span class="text">Log out</span>
            </a>
          </li>
          <li v-else class="log-in">
            <a href="#">
              <img src="../images/login.svg" alt="">
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

        <!-- Messages -->
        <slot name="messages"></slot>

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

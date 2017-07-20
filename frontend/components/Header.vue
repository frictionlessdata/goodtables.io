<script>
import Logo from './Logo.vue'
export default {
  name: 'Header',
  props: {
    userName: String,
    baseUrl: String,
  },
  components: {
    Logo,
  },
}
</script>

<template>
<nav class="navbar navbar-default">

    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <Logo/>
    </div>

    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">

      <ul class="nav navbar-nav navbar-right">
        <template v-if="!userName">
          <li><a :href="`${baseUrl}/user/login/github`">Login with GitHub</a></li>
        </template>
        <template v-else>
          <li>
            <a href="https://discuss.okfn.org/t/launching-goodtables-io-tell-us-what-you-think"><span class="icon-info"></span>Give Feedback</a>
          </li>
          <li role="separator" class="divider"></li>
          <li>
            <a :href="`${baseUrl}/settings`"><span class="icon-equalizer"></span>Manage Sources</a>
          </li>
          <li role="separator" class="divider"></li>
          <li><a :href="`${baseUrl}/user/logout`"><span class="icon-exit"></span>Logout</a></li>
        </template>
      </ul>
    </div>

</nav>
</template>

<style scoped>
</style>

<!-- Import global styles -->
<style lang="scss" src="../styles/main.scss"></style>

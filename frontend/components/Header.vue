<script>
export default {
  props: {
    userName: String,
  },
}
</script>

<template>
<nav class="navbar navbar-default">
  <div class="container">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="/">goodtables.io</a>
    </div>

    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">

      <ul class="nav navbar-nav navbar-right">
        <template v-if="!userName">
          <li><a href="/user/login/github">Login with GitHub</a></li>
        </template>
        <template v-else>
          <li><p class="navbar-text">Hello <a href="/user">{{ userName }}</a></p></li>
          <li role="separator" class="divider"></li>
          <li><a href="/user/logout">Logout</a></li>
        </template>
      </ul>
    </div>
  </div>
</nav>
</template>

<style scoped>
</style>

<!-- Import global styles -->
<style src="../styles.css"></style>

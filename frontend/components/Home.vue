<script>
import Logo from './Logo.vue'

export default {
  name: 'Home',
  props: {},
  components: {
    Logo,
  },
}
</script>

<template>
  <div class="landing">
    <header class="main-header">
      <div class="pattern">
        <div class="inner">
          <div class="container">
            <Logo/>
            <div class="text">
              <h1>Valid Data. Always.</h1>
              <p>
                Welcome to continuous validation for tabular data.
              </p>
              <a class="btn btn-default" href="#">Learn more</a>
              <a class="btn btn-primary" href="/user/login/github">Sign in with GitHub</a>
            </div>
          </div>
        </div>
      </div>
    </header>
  </div>
</template>

<style scoped>
</style>

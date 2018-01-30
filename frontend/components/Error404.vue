<script>
import Logo from './Logo.vue'
import Maze from './Maze.vue'

export default {
  name: 'Error404',
  props: {},
  components: {
    Logo,
    Maze,
  },
}
</script>

<template>
  <div class="minimal">
    <div class="error-page">
      <section class="inner">
        <h1>
          This page could not be found (404)
        </h1>
        <Maze />
        <Logo />
      </section>
    </div>
  </div>
</template>

<style scoped>
</style>

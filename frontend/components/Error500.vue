<script>
import Logo from './Logo.vue'
import Maze from './Maze.vue'

export default {
  name: 'Error500',
  props: {},
  components: {
    Logo,
    Maze,
  }
}
</script>

<template>
  <div class="minimal">
    <div class="error-page">
      <section class="inner">
        <h1>
          Internal error (500)
        </h1>
        <Maze />
        <Logo />
      </section>
    </div>
  </div>
</template>

<style scoped>
</style>

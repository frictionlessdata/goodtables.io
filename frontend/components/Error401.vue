<script>
import Logo from './Logo.vue'
import Maze from './Maze.vue'

export default {
  name: 'Error401',
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
          Not authorized {{ message }} (401)
        </h1>
        <Maze />
        <Logo />
      </section>
    </div>
  </div>
</template>

<style scoped>
</style>

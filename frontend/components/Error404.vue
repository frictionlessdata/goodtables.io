<script>
import Logo from './Logo.vue'
import mazeImage from '../images/maze.svg'

export default {
  name: 'Error404',
  props: {},
  components: {
    Logo,
  },
  data() {
    return {
      mazeImage,
    }
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
        <span v-html="mazeImage"></span>
        <Logo />
      </section>
    </div>
  </div>
</template>

<style scoped>
</style>

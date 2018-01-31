<script>
import Logo from './Logo.vue'
import mazeImage from '../images/maze.svg'

export default {
  name: 'Error500',
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
          Internal error (500)
        </h1>
        <span v-html="mazeImage"></span>
        <Logo />
      </section>
    </div>
  </div>
</template>

<style scoped>
</style>

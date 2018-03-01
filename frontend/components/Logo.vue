<script>
import logoGoodtables from '../images/logo.svg'

export default {
  name: 'Logo',
  props: {
    baseUrl: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      logoGoodtables,
    }
  },
}
</script>

<template>
  <a v-html="logoGoodtables" class="logo" :href="baseUrl">
  </a>
</template>

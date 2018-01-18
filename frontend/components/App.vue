<script>
export default {
  name: 'App',
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
        <slot name="sidebar"></slot>
        <a v-on:click="menuClass = 'collapsed-menu-view'" class="collapse-view left">
          Collapse sidebar
        </a>
      </nav>
      <div class="content">
        <slot name="messages"></slot>
        <slot name="contents"></slot>
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

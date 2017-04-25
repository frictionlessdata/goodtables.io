<script>

import Logo from './Logo.vue'
import SourceList from './SourceList.vue'


export default {
  name: 'Dashboard',
  props: {
    sources: Array,
  },
  components: {
    Logo,
    SourceList,
  },
}
</script>

<template>
  <div class="app list-view">
    <div class="inner">

      <div class="default">
          <main class="main-nav">
            <div role="tabpanel" class="tab-pane active my-sources" id="my-sources">
              <template v-if="sources">
               <SourceList :sources="sources" ref="source-list" />
              </template>
              <template v-if="!sources.length">
                <div class="no-sources panel">No sources added yet! Click on the "Add Sources" button to get started.</div>
                <a href="/settings" type="button" class="btn btn-default"><span class="glyphicon glyphicon-plus-sign" aria-hidden="true"></span> Add Sources</a>
              </template>
            </div>
          </main>
      </div>
    </div>
  </div>
</template>

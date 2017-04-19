<script>

import Vue from 'vue'
import Logo from './Logo.vue'
import SourceList from './SourceList.vue'
import Source_ from './Source.vue'


export default {
  name: 'Dashboard',
  props: {
    sources: Array,
  },
  components: {
    Logo,
    SourceList,
    Source_,
  },
}
</script>

<template>
  <div class="app list-view">
    <div class="inner">

      <div class="default">
          <header>
            <div>
              <button type="button" class="btn btn-default"><span class="glyphicon glyphicon-plus-sign" aria-hidden="true"></span> Add Sources</button>
            </div>
          </header>

          <main class="main-nav">
            <div role="tabpanel" class="tab-pane active my-sources" id="my-sources">
              <template v-if="sources">
               <SourceList :sources="sources" ref="source-list" />
              </template>
              <template v-if="!sources.length">
                <div class="no-sources panel">No sources added yet!</div>
              </template>
            </div>
          </main>
      </div>
    </div>
  </div>
</template>

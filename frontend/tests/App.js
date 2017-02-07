import Vue from 'vue'
import App from '../components/App.vue'
const assert = require('chai').assert

// Tests

describe('App', () => {

  it('should render', () => {
    const vm = new Vue({
      template: '<div><app /></div>',
      components: {
        app: App,
      },
    }).$mount()
    const html = vm.$el.innerHTML
    assert.include(html, 'App')
  })

})

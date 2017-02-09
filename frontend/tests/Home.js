import Vue from 'vue'
import Home from '../components/Home.vue'
const assert = require('chai').assert

// Tests

describe('Home', () => {

  it('should render', () => {
    const vm = new Vue({
      template: '<div><app-home /></div>',
      components: {
        'app-home': Home,
      },
    }).$mount()
    const html = vm.$el.innerHTML
    assert.include(html, 'Home')
  })

})

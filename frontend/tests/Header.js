import Vue from 'vue'
import Header from '../components/Header.vue'
const assert = require('chai').assert

// Tests

describe('Header', () => {

  it('should render', () => {
    const vm = new Vue({
      template: '<div><app-header /></div>',
      components: {
        'app-header': Header,
      },
    }).$mount()
    const html = vm.$el.innerHTML
    assert.include(html, 'Header')
  })

})

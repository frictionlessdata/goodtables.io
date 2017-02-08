import Vue from 'vue'
import Footer from '../components/Footer.vue'
const assert = require('chai').assert

// Tests

describe('Footer', () => {

  it('should render', () => {
    const vm = new Vue({
      template: '<div><app-footer /></div>',
      components: {
        'app-footer': Footer,
      },
    }).$mount()
    const html = vm.$el.innerHTML
    assert.include(html, 'Footer')
  })

})

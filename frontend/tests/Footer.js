import Vue from 'vue'
import Footer from '../components/Footer.vue'
const assert = require('chai').assert

// Tests

describe('Footer', () => {

  it('should render', () => {
    const test = new Vue({render(h) {return h(Footer)}}).$mount()
    assert.include(test.$el.innerHTML, 'Open Knowledge International')
  })

})

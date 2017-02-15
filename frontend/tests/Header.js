import Vue from 'vue'
import Header from '../components/Header.vue'
const assert = require('chai').assert

// Tests

describe('Header', () => {

  it('should render', () => {
    const test = new Vue({render(h) {return h(Header)}}).$mount()
    assert.include(test.$el.innerHTML, 'Login')
  })

})

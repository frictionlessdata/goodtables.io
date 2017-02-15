import Vue from 'vue'
import Home from '../components/Home.vue'
const assert = require('chai').assert

// Tests

describe('Home', () => {

  it('should render', () => {
    const test = new Vue({render(h) {return h(Home)}}).$mount()
    assert.include(test.$el.innerHTML, 'Welcome')
  })

})

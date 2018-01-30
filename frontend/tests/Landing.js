import {should} from 'chai'
import {mount} from 'avoriaz'
import Landing from '../components/Landing.vue'
should()

// Tests

describe('Landing', () => {

  it('should contain correct text', () => {
    const wrapper = mount(Landing)
    wrapper.find('h1')[0].text().should.include('Have confidence in your data')
  })

})

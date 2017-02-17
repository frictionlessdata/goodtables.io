import {should} from 'chai'
import {mount} from 'avoriaz'
import Error500 from '../components/Error500.vue'
should()

// Tests

describe('Error500', () => {

  it('should contain correct text', () => {
    const wrapper = mount(Error500)
    wrapper.find('h1')[0].text().should.include('Error 500')
  })

})

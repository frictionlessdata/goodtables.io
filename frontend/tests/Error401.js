import {should} from 'chai'
import {mount} from 'avoriaz'
import Error401 from '../components/Error401.vue'
should()

// Tests

describe('Error401', () => {

  it('should contain correct text', () => {
    const wrapper = mount(Error401)
    wrapper.find('h1')[0].text().should.include('401')
  })

})

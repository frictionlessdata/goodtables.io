import {should} from 'chai'
import {mount} from 'avoriaz'
import Home from '../components/Home.vue'
should()

// Tests

describe('Home', () => {

  it('should contain correct text', () => {
    const wrapper = mount(Home)
    wrapper.find('h1')[0].text().should.include('Continuous data validation for everybody')
  })

})

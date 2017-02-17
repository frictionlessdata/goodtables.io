import {should} from 'chai'
import {mount} from 'avoriaz'
import Footer from '../components/Footer.vue'
should()

// Tests

describe('Footer', () => {

  it('should contain correct text', () => {
    const wrapper = mount(Footer)
    wrapper.text()
      .should.include('Open Knowledge International, 2017')
  })

})

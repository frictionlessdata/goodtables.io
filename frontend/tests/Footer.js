import {mount} from 'avoriaz'
import {should} from 'chai'; should()
import Footer from '../components/Footer.vue'

// Tests

describe('Footer', () => {

  it('should contain correct text', () => {
    const wrapper = mount(Footer)
    wrapper.text().trim().should.equal('Open Knowledge International, 2017')
  })

})

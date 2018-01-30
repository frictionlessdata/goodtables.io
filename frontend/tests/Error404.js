import {should} from 'chai'
import {mount} from 'avoriaz'
import Error404 from '../components/Error404.vue'
should()

// Tests

describe('Error404', () => {

  it('should contain correct text', () => {
    const wrapper = mount(Error404)
    wrapper.find('h1')[0].text().should.include('404')
  })

})

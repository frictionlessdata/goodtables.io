import {should} from 'chai'
import {mount} from 'avoriaz'
import ErrorGroup from '../components/ErrorGroup.vue'
should()

// Tests

describe('ErrorGroup', () => {

  it('should contain data', () => {
    const propsData = {errorGroup: {
      name: 'name',
      type: 'type',
      count: 1,
      rows: [],
    }}
    const wrapper = mount(ErrorGroup, {propsData})
    wrapper.text().should.include('name')
    wrapper.text().should.include('1')
  })

})

import {should} from 'chai'
import {mount} from 'avoriaz'
import ReportErrorGroup from '../components/ReportErrorGroup.vue'
should()

// Tests

describe('ReportErrorGroup', () => {

  it('should contain data', () => {
    const propsData = {errorGroup: {
      name: 'name',
      type: 'type',
      count: 1,
      rows: [],
    }}
    const wrapper = mount(ReportErrorGroup, {propsData})
    wrapper.text().should.include('name')
    wrapper.text().should.include('1')
  })

})

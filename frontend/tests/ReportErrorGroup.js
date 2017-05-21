import {should} from 'chai'
import {mount} from 'avoriaz'
import ReportErrorGroup from '../components/ReportErrorGroup.vue'
should()

// Tests

describe('ReportErrorGroup', () => {

  it('should contain data', () => {
    const propsData = {errorGroup: {
      code: 'blank-header',
      count: 1,
      rows: [],
      headers: [],
    }}
    const wrapper = mount(ReportErrorGroup, {propsData})
    wrapper.text().should.include('Blank Header')
    wrapper.text().should.include('1')
  })

})

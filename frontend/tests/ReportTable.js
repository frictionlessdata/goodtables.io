import {should} from 'chai'
import {mount} from 'avoriaz'
import ReportTable from '../components/ReportTable.vue'
import ReportErrorGroup from '../components/ReportErrorGroup.vue'
const report = require('./fixtures/report.json')
should()

// Tests

describe('ReportTable', () => {

  it('should contain ReportErrorGroup component', () => {
    const propsData = {table: report.tables[0]}
    const wrapper = mount(ReportTable, {propsData})
    wrapper.find(ReportErrorGroup).should.has.length(6)
    wrapper.find(ReportErrorGroup)[0].propsData().errorGroup.name.should.equal('blank-header')
    wrapper.find(ReportErrorGroup)[0].propsData().errorGroup.type.should.equal('type')
    wrapper.find(ReportErrorGroup)[0].propsData().errorGroup.count.should.equal(1)
  })

})

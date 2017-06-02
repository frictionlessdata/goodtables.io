import {should} from 'chai'
import {mount} from 'avoriaz'
import Report from '../components/Report.vue'
import ReportTable from '../components/ReportTable.vue'
const report = require('./fixtures/report.json')
should()

// Tests

describe('Report', () => {

  it('should contain ReportTable component', () => {
    const propsData = {report}
    const wrapper = mount(Report, {propsData})
    wrapper.find(ReportTable).should.has.length(1)
    wrapper.find(ReportTable)[0].propsData().table.valid.should.be.false
    wrapper.find(ReportTable)[0].propsData().tableNumber.should.be.equal(1)
    wrapper.find(ReportTable)[0].propsData().tablesCount.should.be.equal(1)
  })

})

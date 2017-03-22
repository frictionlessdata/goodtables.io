import {should} from 'chai'
import {mount} from 'avoriaz'
import Job from '../components/Job.vue'
import {Report} from 'goodtables-vue'
should()

// Tests

describe('Job', () => {

  it('should be empty if there is no report', () => {
    const propsData = {job: {}}
    const wrapper = mount(Job, {propsData})
    wrapper.text().should.include('There is an error in the job!')
  })

  it('should contain Report component if there is report', () => {
    const propsData = {
      job: {
        report: 'report',
      },
    }
    const wrapper = mount(Job, {propsData})
    wrapper.find(Report).should.has.length(1)
    wrapper.find(Report)[0].propsData().should.deep.equal({report: 'report'})
  })

})

import {should} from 'chai'
import {mount} from 'avoriaz'
import JobList from '../components/JobList.vue'
import Jobs from '../components/Jobs.vue'
should()

// Tests

describe('Jobs', () => {

  it('should contain headings', () => {
    const propsData = {}
    const wrapper = mount(Jobs, {propsData})
    wrapper.find('h1')[0].text().should.equal('All Jobs')
  })

  it('should have no jobs', () => {
    const propsData = {}
    const wrapper = mount(Jobs, {propsData})
    wrapper.text().should.include('No active or finished jobs.')
  })

  describe('[with jobs]', () => {

    it('should contain JobList', () => {
      const propsData = {
        jobs: [
          'job1',
          'job2',
        ],
      }
      const wrapper = mount(Jobs, {propsData})
      wrapper.find(JobList).should.has.length(1)
      wrapper.find(JobList)[0].propsData().should.deep.equal({jobs: ['job1', 'job2']})
    })

  })

})

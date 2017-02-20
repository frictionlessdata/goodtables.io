import {should} from 'chai'
import {mount} from 'avoriaz'
import JobList from '../components/JobList.vue'
import Dashboard from '../components/Dashboard.vue'
should()

// Tests

describe('Dashboard', () => {

  it('should contain headings', () => {
    const propsData = {
      githubJobs: [],
      s3Jobs: [],
    }
    const wrapper = mount(Dashboard, {propsData})
    wrapper.find('h1')[0].text().should.equal('Dashboard')
    wrapper.find('h2')[0].text().should.equal('Jobs')
    wrapper.find('h3')[0].text().should.equal('GitHub')
    wrapper.find('h3')[1].text().should.equal('Amazon S3')
  })

  describe('[with githubJobs]', () => {

    it('should contain JobList', () => {
      const propsData = {
        githubJobs: [
          'job1',
          'job2',
        ],
        s3Jobs: [],
      }
      const wrapper = mount(Dashboard, {propsData})
      wrapper.find(JobList).should.has.length(1)
      wrapper.find(JobList)[0].propsData().should.deep.equal({jobs: ['job1', 'job2']})
    })

  })

  describe('[with s3Jobs]', () => {

    it('should contain JobList', () => {
      const propsData = {
        githubJobs: [],
        s3Jobs: [
          'job1',
          'job2',
        ],
      }
      const wrapper = mount(Dashboard, {propsData})
      wrapper.find(JobList).should.has.length(1)
      wrapper.find(JobList)[0].propsData().should.deep.equal({jobs: ['job1', 'job2']})
    })

  })

})

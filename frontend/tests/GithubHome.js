import {should} from 'chai'
import {mount} from 'avoriaz'
import JobList from '../components/JobList.vue'
import GithubHome from '../components/GithubHome.vue'
should()

// Tests

describe('GithubHome', () => {

  it('should contain headings', () => {
    const propsData = {
      s3Jobs: [],
    }
    const wrapper = mount(GithubHome, {propsData})
    wrapper.find('h1')[0].text().should.equal('GitHub Jobs')
  })

  it('should have no jobs', () => {
    const propsData = {
      s3Jobs: [],
    }
    const wrapper = mount(GithubHome, {propsData})
    wrapper.text().should.include('No active or finished jobs.')
  })

  it('should contain org', () => {
    const propsData = {
      s3Jobs: [],
      org: 'org1',
    }
    const wrapper = mount(GithubHome, {propsData})
    wrapper.find('h2')[0].text().should.include('org1')
  })

  it('should contain org/repo', () => {
    const propsData = {
      s3Jobs: [],
      org: 'org1',
      repo: 'repo1',
    }
    const wrapper = mount(GithubHome, {propsData})
    wrapper.find('h2')[0].text().should.include('org1/repo1')
  })

  describe('[with jobs]', () => {

    it('should contain JobList', () => {
      const propsData = {
        jobs: [
          'job1',
          'job2',
        ],
      }
      const wrapper = mount(GithubHome, {propsData})
      wrapper.find(JobList).should.has.length(1)
      wrapper.find(JobList)[0].propsData().should.deep.equal({jobs: ['job1', 'job2']})
    })

  })

})

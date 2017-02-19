import {should} from 'chai'
import {mount} from 'avoriaz'
import JobList from '../components/JobList.vue'
should()

// Tests

describe('JobList', () => {

  it('should be empty', () => {
    const propsData = {}
    const wrapper = mount(JobList, {propsData})
    wrapper.find('.row').should.has.length(0)
  })

  describe('[with jobs]', () => {

    it('should contain JobList', () => {
      const propsData = {
        jobs: [
          {
            id: 'id1',
            status: 'success',
            integration_name: 'github',
            conf: {owner: 'owner', repo: 'repo', sha: 'sha'},
          },
          {
            id: 'id2',
            status: 'failed',
            integration_name: 's3',
            conf: {bucket: 'bucket'},
          },
        ],
      }
      const wrapper = mount(JobList, {propsData})
      wrapper.find('.row').should.has.length(2)
      wrapper.find('.row')[0].text().should.contain('Valid')
      wrapper.find('.row')[0].text().should.contain('owner/repo')
      wrapper.find('.row')[1].text().should.contain('Invalid')
      wrapper.find('.row')[1].text().should.contain('bucket')
    })

  })

})

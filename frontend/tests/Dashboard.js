import {should} from 'chai'
import {mount} from 'avoriaz'
import Dashboard from '../components/Dashboard.vue'
should()

// Tests

describe('Dashboard', () => {

  it('should contain headings', () => {
    /*
     * TODO: update once the Dashboard design is settled
    const propsData = {
      latestJobs: [],
    }
    const wrapper = mount(Dashboard, {propsData})
    wrapper.find('h1')[0].text().should.equal('Dashboard')
    wrapper.find('h2')[0].text().should.equal('Jobs')
    wrapper.find('h3')[0].text().should.equal('GitHub')
    wrapper.find('h3')[1].text().should.equal('Amazon S3')
    */
  })

  describe('[with sources]', () => {

    it.skip('should contain SourceList', () => {
      const propsData = {
        sources: [
          'source1',
          'source2',
        ],
      }
      const wrapper = mount(Dashboard, {propsData})
      wrapper
      // wrapper.find(SourceList).should.have.length(1)
      // wrapper.find(SourceList)[0].propsData().sources.should.deep.equal(['source1', 'source2'])
    })

  })

})

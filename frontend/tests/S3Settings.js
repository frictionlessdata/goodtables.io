import {should} from 'chai'
import {mount} from 'avoriaz'
import JobList from '../components/JobList.vue'
import S3Settings from '../components/S3Settings.vue'
should()

// Tests

describe('S3Settings', () => {

  it('should contain headings', () => {
    const propsData = {}
    const wrapper = mount(S3Settings, {propsData})
    wrapper.find('h1')[0].text().should.equal('Amazon S3')
    wrapper.find('h2')[0].text().should.equal('Buckets')
    wrapper.find('h2')[1].text().should.equal('Add Bucket')
  })

  it('should have no buckets', () => {
    const propsData = {buckets: []}
    const wrapper = mount(S3Settings, {propsData})
    wrapper.text().should.include('No buckets configured')
  })

  describe('[with buckets]', () => {

    it('should contain buckets', () => {
      const propsData = {
        buckets: [
          {name: 'name1'},
          {name: 'name2'},
        ],
      }
      const wrapper = mount(S3Settings, {propsData})
      wrapper.find('[href="/s3/settings/remove_bucket/name1"]').should.has.length(1)
      wrapper.find('[href="/s3/settings/remove_bucket/name2"]').should.has.length(1)
    })

  })

})

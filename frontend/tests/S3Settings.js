import axios from 'axios'
import {should} from 'chai'
import {mount} from 'avoriaz'
import AxiosMockAdapter from 'axios-mock-adapter'
import Messages from '../components/Messages.vue'
import S3Settings from '../components/S3Settings.vue'
should()

// Tests

describe('S3Settings', () => {
  let mockAxios

  beforeEach(() => {
    mockAxios = new AxiosMockAdapter(axios)
    mockAxios.onGet('/s3/api/bucket').reply(200, {
      buckets: [],
    })
  })

  afterEach(() => {
    mockAxios.restore()
  })

  it('should contain headings', (done) => {
    const wrapper = mount(S3Settings)
    setTimeout(() => {
      wrapper.find('h1')[0].text().should.equal('Amazon S3')
      wrapper.find('h2')[0].text().should.equal('Buckets')
      wrapper.find('h2')[1].text().should.equal('Add Bucket')
      done()
    })
  })

  it('should have no buckets', (done) => {
    const wrapper = mount(S3Settings)
    setTimeout(() => {
      wrapper.text().should.include('No buckets configured')
      done()
    })
  })

  it('should show buckets after loading', (done) => {
    mockAxios.reset()
    mockAxios.onGet('/s3/api/bucket').reply(200, {
      buckets: [
        {id: 'id1', name: 'name1', active: true},
        {id: 'id2', name: 'name2', active: false},
      ],
    })
    const wrapper = mount(S3Settings)
    wrapper.text().should.include('Loading buckets. Please wait..')
    setTimeout(() => {
      wrapper.text().should.include('name1')
      wrapper.text().should.include('name2')
      done()
    })
  })

})

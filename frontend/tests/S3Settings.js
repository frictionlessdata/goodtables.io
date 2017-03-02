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

  it('should have submit button', (done) => {
    const wrapper = mount(S3Settings)
    setTimeout(() => {
      wrapper.find('button')[0].text().should.include('Submit')
      done()
    })
  })

  it('should add bucket after submit button click', (done) => {
    mockAxios.onPost('/s3/api/bucket').replyOnce(200, {
      bucket: {
        id: 'id',
        name: 'name',
        active: true,
      },
      error: null,
    })
    const wrapper = mount(S3Settings)
    wrapper.vm.bucketName = 'name'
    wrapper.find('button')[0].simulate('click')
    setTimeout(() => {
      wrapper.text().should.include('name')
      done()
    })
  })

  it('should show error on submit button click error ', (done) => {
    mockAxios.onPost('/s3/api/bucket').replyOnce(200, {
      error: 'Bucket error',
    })
    const wrapper = mount(S3Settings)
    wrapper.vm.bucketName = 'bucket-name'
    wrapper.find('button')[0].simulate('click')
    setTimeout(() => {
      wrapper.find(Messages).should.has.length(1)
      wrapper.find(Messages)[0].propsData().messages
        .should.deep.equal([['danger', 'Bucket error']])
      done()
    })
  })

  // TODO: write this test after:
  // https://github.com/eddyerburgh/avoriaz/issues/6
  it.skip('should remove bucket after remove button click', () => {
    // ...
  })

})

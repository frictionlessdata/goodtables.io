import axios from 'axios'
import {should} from 'chai'
import {mount} from 'avoriaz'
import AxiosMockAdapter from 'axios-mock-adapter'
import Messages from '../components/Messages.vue'
import SettingsS3 from '../components/SettingsS3.vue'
should()

// Tests

describe('SettingsS3', () => {
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

  it('should have no buckets', (done) => {
    const wrapper = mount(SettingsS3)
    setTimeout(() => {
      wrapper.text().should.include('no active buckets')
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
    const wrapper = mount(SettingsS3)
    // wrapper.text().should.include('Loading buckets. Please wait..')
    setTimeout(() => {
      wrapper.text().should.include('name1')
      wrapper.text().should.include('name2')
      done()
    })
  })

  it('should have add button', (done) => {
    const wrapper = mount(SettingsS3)
    setTimeout(() => {
      wrapper.find('button.add')[0].trigger('click')
      wrapper.find('button.add')[0].text().should.include('Add')
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
    const wrapper = mount(SettingsS3)
    wrapper.vm.bucketName = 'name'
    wrapper.find('button.add')[0].trigger('click')
    setTimeout(() => {
      wrapper.text().should.include('name')
      done()
    })
  })

  it('should show error on submit button click error ', (done) => {
    mockAxios.onPost('/s3/api/bucket').replyOnce(200, {
      error: 'Bucket error',
    })
    const wrapper = mount(SettingsS3)
    wrapper.vm.bucketName = 'bucket-name'
    wrapper.find('button.add')[0].trigger('click')
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

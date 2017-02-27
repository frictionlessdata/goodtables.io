import axios from 'axios'
import {should} from 'chai'
import {mount} from 'avoriaz'
import AxiosMockAdapter from 'axios-mock-adapter'
import Messages from '../components/Messages.vue'
import GithubSettings from '../components/GithubSettings.vue'
should()

// Tests

describe('GithubSettings', () => {
  let mockAxios

  beforeEach(() => {
    mockAxios = new AxiosMockAdapter(axios)
    mockAxios.onGet('/github/api/repo').reply(200, {
      syncing: false,
      repos: [],
    })
  })

  afterEach(() => {
    mockAxios.restore()
  })

  it('should contain headings', (done) => {
    const wrapper = mount(GithubSettings)
    setTimeout(() => {
      wrapper.find('h1')[0].text().should.equal('GitHub')
      wrapper.find('h2')[0].text().should.equal('Repos')
      done()
    })
  })

  it('should have no repositories', (done) => {
    const wrapper = mount(GithubSettings)
    setTimeout(() => {
      wrapper.text().should.include('There are no synced repositories')
      done()
    })
  })

  it('should have sync account button', (done) => {
    const wrapper = mount(GithubSettings)
    setTimeout(() => {
      wrapper.find('.sync>.btn')[0].text().should.equal('Sync account')
      done()
    })
  })

  it('should not have syncing account message', (done) => {
    const wrapper = mount(GithubSettings)
    setTimeout(() => {
      wrapper.find(Messages).should.has.length(0)
      done()
    })
  })

  it('should have syncing account message on syncing', (done) => {
    mockAxios.reset()
    mockAxios.onGet('/github/api/repo').reply(200, {
      syncing: true,
      repos: [],
    })
    const wrapper = mount(GithubSettings)
    setTimeout(() => {
      wrapper.find(Messages).should.has.length(1)
      wrapper.find(Messages)[0].propsData().messages
        .should.deep.equal([['warning', 'Syncing account. Please wait..']])
      done()
    })
  })

  it('should show existent repos after loading', (done) => {
    mockAxios.reset()
    mockAxios.onGet('/github/api/repo').reply(200, {
      syncing: false,
      repos: [
        {id: 'id1', name: 'name1', active: true},
        {id: 'id2', name: 'name2', active: false},
      ],
    })
    const wrapper = mount(GithubSettings)
    wrapper.text().should.include('Loading repos. Please wait..')
    setTimeout(() => {
      wrapper.text().should.include('name1')
      wrapper.text().should.include('name2')
      done()
    })
  })

  it('should show error on sync account click error', (done) => {
    mockAxios.onGet('/github/api/sync_account').replyOnce(200, {
      error: 'Sync account error',
    })
    const wrapper = mount(GithubSettings)
    wrapper.find('.sync>.btn')[0].simulate('click')
    setTimeout(() => {
      wrapper.find(Messages).should.has.length(1)
      wrapper.find(Messages)[0].propsData().messages
        .should.deep.equal([['danger', 'Sync account error']])
      done()
    })
  })

  it('should work on sync account click success', (done) => {
    mockAxios.reset()
    mockAxios.onGet('/github/api/repo').replyOnce(200, {
      syncing: false,
      repos: [],
    })
    mockAxios.onGet('/github/api/repo').replyOnce(200, {
      syncing: true,
      repos: [],
    })
    mockAxios.onGet('/github/api/repo').replyOnce(200, {
      syncing: false,
      repos: [
        {id: 'id1', name: 'name1', active: true},
        {id: 'id2', name: 'name2', active: false},
      ],
    })
    mockAxios.onGet('/github/api/sync_account').replyOnce(200, {
      error: null,
    })
    // TODO: use fake timer from sinon.js
    const wrapper = mount(GithubSettings)
    wrapper.find('.sync>.btn')[0].simulate('click')
    setTimeout(() => {
      wrapper.find(Messages).should.has.length(1)
      wrapper.find(Messages)[0].propsData().messages
        .should.deep.equal([['warning', 'Syncing account. Please wait..']])
      done()
    }, 2000)
    setTimeout(() => {
      wrapper.text().should.include('name1')
      wrapper.text().should.include('name2')
      done()
    }, 4000)
  })

})

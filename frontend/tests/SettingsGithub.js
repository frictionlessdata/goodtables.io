import axios from 'axios'
import {should} from 'chai'
import {mount} from 'avoriaz'
import AxiosMockAdapter from 'axios-mock-adapter'
import Messages from '../components/Messages.vue'
import SettingsGithub from '../components/SettingsGithub.vue'
should()

// Tests

describe('SettingsGithub', () => {
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

  it('should have no repositories', (done) => {
    const wrapper = mount(SettingsGithub)
    setTimeout(() => {
      wrapper.text().should.include('no active repositories')
      done()
    })
  })

  it('should have sync account button', (done) => {
    const wrapper = mount(SettingsGithub)
    setTimeout(() => {
      wrapper.find('.refresh')[0].text().should.include('Refresh')
      done()
    })
  })

  it('should not have syncing account message', (done) => {
    const wrapper = mount(SettingsGithub)
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
    const wrapper = mount(SettingsGithub)
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
    const wrapper = mount(SettingsGithub)
    // wrapper.text().should.include('Loading repos. Please wait..')
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
    const wrapper = mount(SettingsGithub)
    wrapper.find('.refresh')[0].trigger('click')
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
    const wrapper = mount(SettingsGithub)
    wrapper.find('.refresh')[0].trigger('click')
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

  // TODO: recover this test after:
  // https://github.com/eddyerburgh/avoriaz/issues/6
  it.skip('should work on activate/deactivate repo click', (done) => {
    mockAxios.reset()
    mockAxios.onGet('/github/api/repo').reply(200, {
      syncing: false,
      repos: [
        {id: 'id', name: 'name', active: false},
      ],
    })
    mockAxios.onGet('/github/api/repo/id/activate').reply(200, {
      error: null,
    })
    mockAxios.onGet('/github/api/repo/id/deactivate').reply(200, {
      error: null,
    })
    const wrapper = mount(SettingsGithub)
    setTimeout(() => {
      wrapper.find('.repo>.btn')[0].text().should.include('Activate')
      wrapper.find('.repo>.btn')[0].trigger('click')
    }, 200)
    setTimeout(() => {
      wrapper.find('.repo>.btn')[0].text().should.include('Deactivate')
      wrapper.find('.repo>.btn')[0].trigger('click')
    }, 400)
    setTimeout(() => {
      wrapper.find('.repo>.btn')[0].text().should.include('Activate')
      done()
    }, 600)
  })

})

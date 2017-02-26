import axios from 'axios'
import {should} from 'chai'
import {mount} from 'avoriaz'
import AxiosMockAdapter from 'axios-mock-adapter'
import GithubSettings from '../components/GithubSettings.vue'
should()

// Tests

describe('GithubSettings', () => {
  let mockAxios

  beforeEach(() => {
    mockAxios = new AxiosMockAdapter(axios)
    mockAxios.onGet('/github/api/is_syncing_account').reply(200, {
      is_syncing_account: false,
    })
  })

  afterEach(() => {
    mockAxios.restore()
  })

  it('should contain headings', (done) => {
    const propsData = {}
    const wrapper = mount(GithubSettings, {propsData})
    setTimeout(() => {
      wrapper.find('h1')[0].text().should.equal('GitHub')
      wrapper.find('h2')[0].text().should.equal('Repos')
      done()
    })
  })

  it('should have no repositories', (done) => {
    const propsData = {repos: []}
    const wrapper = mount(GithubSettings, {propsData})
    setTimeout(() => {
      wrapper.text().should.include('There are no synced repositories')
      done()
    })
  })

  it('should have sync account button', (done) => {
    const propsData = {repos: []}
    const wrapper = mount(GithubSettings, {propsData})
    setTimeout(() => {
      wrapper.find('[href="/github/sync"]')[0].text().should.equal('Sync account')
      done()
    })
  })

  it('should not show syncing account', (done) => {
    const wrapper = mount(GithubSettings)
    setTimeout(() => {
      wrapper.text().should.not.include('Syncing account')
      done()
    })
  })

  it('should show syncing account on syncing', (done) => {
    mockAxios.reset()
    mockAxios.onGet('/github/api/is_syncing_account').reply(200, {
      is_syncing_account: true,
    })
    const wrapper = mount(GithubSettings)
    setTimeout(() => {
      wrapper.text().should.include('Syncing account')
      done()
    })
  })

  describe('[with repos]', () => {

    it('should contain repos', (done) => {
      const propsData = {
        repos: [
          {id: 'id1', name: 'name1', active: true},
          {id: 'id2', name: 'name2', active: false},
        ],
      }
      const wrapper = mount(GithubSettings, {propsData})
      setTimeout(() => {
        wrapper.find('[href="https://github.com/name1"]').should.has.length(1)
        wrapper.find('[href="https://github.com/name2"]').should.has.length(1)
        done()
      })
    })

  })

})

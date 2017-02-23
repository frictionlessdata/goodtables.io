import {should} from 'chai'
import {mount} from 'avoriaz'
import GithubSettings from '../components/GithubSettings.vue'
should()

// Tests

describe('GithubSettings', () => {

  it('should contain headings', () => {
    const propsData = {}
    const wrapper = mount(GithubSettings, {propsData})
    wrapper.find('h1')[0].text().should.equal('GitHub')
    wrapper.find('h2')[0].text().should.equal('Repos')
  })

  it('should have no repositories', () => {
    const propsData = {repos: []}
    const wrapper = mount(GithubSettings, {propsData})
    wrapper.text().should.include('There are no synced repositories')
  })

  it('should have sync account button', () => {
    const propsData = {repos: []}
    const wrapper = mount(GithubSettings, {propsData})
    wrapper.find('[href="/github/sync"]')[0].text().should.equal('Sync account')
  })

  it('should work with sync true', () => {
    const propsData = {
      sync: true,
    }
    const wrapper = mount(GithubSettings, {propsData})
    wrapper.text().should.include('Syncing account')
  })

  describe('[with repos]', () => {

    it('should contain repos', () => {
      const propsData = {
        repos: [
          {id: 'id1', name: 'name1', active: true},
          {id: 'id2', name: 'name2', active: false},
        ],
      }
      const wrapper = mount(GithubSettings, {propsData})
      wrapper.find('[href="https://github.com/name1"]').should.has.length(1)
      wrapper.find('[href="https://github.com/name2"]').should.has.length(1)
    })

  })

})

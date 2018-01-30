import {should} from 'chai'
import {mount} from 'avoriaz'
import App from '../components/App.vue'
should()

// Tests

describe('App', () => {

  it('should contain link to home', () => {
    const wrapper = mount(App)
    wrapper.find('[href="/"]')[0]
  })

  it('should contain login with github link', () => {
    const wrapper = mount(App)
    wrapper.find('[href$="/user/login/github"]')[0].text().trim()
      .should.equal('Log in')
  })

  describe('[with user]', () => {

    it('should contain manage sources link', () => {
      const propsData = {userName: 'userName'}
      const wrapper = mount(App, {propsData})
      wrapper.find('[href$="/settings"]')[0].text().trim()
        .should.equal('Manage Sources')
    })

    it('should contain logout link', () => {
      const propsData = {userName: 'userName'}
      const wrapper = mount(App, {propsData})
      wrapper.find('[href$="/user/logout"]')[0].text().trim()
        .should.equal('Log out')
    })

  })

})

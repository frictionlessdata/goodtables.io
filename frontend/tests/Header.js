import {should} from 'chai'
import {mount} from 'avoriaz'
import Header from '../components/Header.vue'
should()

// Tests

describe('Header', () => {

  it('should contain link to home', () => {
    const wrapper = mount(Header)
    wrapper.find('[href="/"]')[0]
  })

  it('should contain login with github link', () => {
    const wrapper = mount(Header)
    wrapper.find('[href$="/user/login/github"]')[0].text()
      .should.equal('Login with GitHub')
  })

  describe('[with user]', () => {

    it('should contain manage sources link', () => {
      const propsData = {userName: 'userName'}
      const wrapper = mount(Header, {propsData})
      wrapper.find('[href$="/settings"]')[0].text().should.equal('Manage Sources')
    })

    it('should contain logout link', () => {
      const propsData = {userName: 'userName'}
      const wrapper = mount(Header, {propsData})
      wrapper.find('[href$="/user/logout"]')[0].text().should.equal('Logout')
    })

  })

})

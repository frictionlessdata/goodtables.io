import {should} from 'chai'
import {mount} from 'avoriaz'
import Header from '../components/Header.vue'
should()

// Tests

describe('Header', () => {

  it('should contain link to home', () => {
    const wrapper = mount(Header)
    wrapper.find('[href="/"]')[0].text()
      .should.equal('goodtables.io')
  })

  it('should contain login with github link', () => {
    const wrapper = mount(Header)
    wrapper.find('[href="/user/login/github"]')[0].text()
      .should.equal('Login with GitHub')
  })

  describe('#userName', () => {

    it('should contain userName', () => {
      const propsData = {userName: 'userName'}
      const wrapper = mount(Header, {propsData})
      wrapper.text()
        .should.include(propsData.userName)
    })

    it('should contain logout link', () => {
      const propsData = {userName: 'userName'}
      const wrapper = mount(Header, {propsData})
      wrapper.find('[href="/user/logout"]')[0].text()
        .should.equal('Logout')
    })

  })

})

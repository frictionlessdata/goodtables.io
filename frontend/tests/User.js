import {should} from 'chai'
import {mount} from 'avoriaz'
import User from '../components/User.vue'
should()

// Tests

describe('User', () => {

  it('should contain heading', () => {
    const wrapper = mount(User)
    wrapper.find('h1')[0].text().should.include('User')
  })

  it('should contain userName', () => {
    const propsData = {userName: 'userName'}
    const wrapper = mount(User, {propsData})
    wrapper.text().should.include(propsData.userName)
  })

  it('should contain userEmail', () => {
    const propsData = {userEmail: 'userEmail'}
    const wrapper = mount(User, {propsData})
    wrapper.text().should.include(propsData.userEmail)
  })

})

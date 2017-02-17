import {should} from 'chai'
import {mount} from 'avoriaz'
import Messages from '../components/Messages.vue'
should()

// Tests

describe('Messages', () => {

  it('should be empty', () => {
    const wrapper = mount(Messages)
    wrapper.find('div').should.has.length(1)
    wrapper.find('div')[0].isEmpty().should.be.true
  })

  describe('[with messages]', () => {

    it('should contain messages', () => {
      const propsData = {messages: [
        ['category1', 'message1'],
        ['category2', 'message2'],
      ]}
      const wrapper = mount(Messages, {propsData})
      wrapper.find('.alert').should.has.length(2)
      wrapper.find('.alert')[0].hasClass('alert-category1').should.be.true
      wrapper.find('.alert')[1].hasClass('alert-category2').should.be.true
      wrapper.find('.alert')[0].text().should.include('message1')
      wrapper.find('.alert')[1].text().should.include('message2')
    })

  })

})

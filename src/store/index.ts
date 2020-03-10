import Vue from 'vue'
import Vuex from 'vuex'
import Parse from 'parse'

// I want to add Parse to the global space for debugging purposes
declare const window: any // eslint-disable-line @typescript-eslint/no-explicit-any

Vue.use(Vuex)

interface ObjectMap { [key: string]: Parse.Object }
Parse.serverURL = 'https://parseapi.back4app.com' // This is your Server URL
Parse.liveQueryServerURL = 'wss://grillporn.back4app.io'
window.Parse = Parse
Parse.initialize(
  'l6HsMGQ3ugnZcQOkiH1wG7Iy6IRKhx7RDvqQp8Vz', // This is your Application ID
  'OvkTMhO18uraIXwRbgqQnPSMVnXofU5cvvAt5uA7' // This is your Javascript key
)

let user: Parse.Object | undefined
let deviceSubscription: Parse.LiveQuerySubscription
const store = new Vuex.Store({
  state: {
    user: {
      loggedIn: false,
      username: '',
      email: ''
    },
    devices: {} as ObjectMap
  },
  mutations: {
    updateUser (state, data) {
      state.user.username = data.get('username')
      state.user.email = data.get('email')
      state.user.loggedIn = true
    },
    logout (state) {
      user = undefined
      state.user.username = ''
      state.user.email = ''
      state.user.loggedIn = false
    },
    upsertDevice (state, device) {
      const id: string = device.id
      if (id) {
        Vue.set(state.devices, id, device)
      }
    },
    removeDevice (state, device) {
      const id: string = device.id
      delete state.devices[id]
    }
  },
  actions: {
    async login ({ commit, dispatch }, { username = '', password = '' }) {
      try {
        user = await Parse.User.logIn(username, password)
        commit('updateUser', user)
        dispatch('bindDevices')
      } catch (ex) {
        commit('logout')
        deviceSubscription && deviceSubscription.unsubscribe()
        throw ex
      }
    },
    async logout ({ commit }) {
      await Parse.User.logOut()
      commit('logout')
    },
    checkSesssion ({ commit, dispatch }) {
      user = Parse.User.current()
      if (user) {
        commit('updateUser', user)
        dispatch('bindDevices')
      } else {
        commit('logout')
        deviceSubscription && deviceSubscription.unsubscribe()
      }
    },
    async bindDevices ({ commit, dispatch }) {
      const deviceQuery = new Parse.Query('Device')
      const devices = await deviceQuery.find()
      devices.forEach(device => commit('upsertDevice', device))
      deviceSubscription?.removeAllListeners() // eslint-disable-line no-unused-expressions
      deviceSubscription?.unsubscribe() // eslint-disable-line no-unused-expressions
      deviceSubscription = await deviceQuery.subscribe()
      deviceSubscription.on('create', (device) => {
        commit('upsertDevice', device)
      })
      deviceSubscription.on('update', (device) => {
        commit('upsertDevice', device)
      })
      deviceSubscription.on('delete', (device) => {
        commit('removeDevice', device)
      })
      deviceSubscription.once('close', async () => {
        deviceSubscription.removeAllListeners()
        await deviceSubscription.unsubscribe()
        setTimeout(() => dispatch('bindDevices'), 10 * 1000)
      })
    }
  },
  getters: {
    isLoggedIn: (state) => state.user.loggedIn
  },
  modules: {
  }
})
export default store

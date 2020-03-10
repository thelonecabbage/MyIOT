<template>
  <q-form ref="loginForm" @submit="doLogin">
    <div class="q-pa-md">
      <div class="q-gutter-sm row items-start">
        <q-input v-model="username" class="full-width" filled type="text" label="Login" />
        <q-input v-model="password" class="full-width" filled type="password" label="Password" />
        <q-btn label="Login" type="submit" class="full-width" color="primary"/>
      </div>
    </div>
  </q-form>
</template>
<script>
import { mapActions, mapGetters } from 'vuex'
export default {
  data: () => ({
    username: '',
    password: ''
  }),
  computed: {
    ...mapGetters(['isLoggedIn'])
  },
  methods: {
    ...mapActions(['login']),
    async doLogin () {
      const { username, password } = this
      await this.login({ username, password })
      if (this.isLoggedIn) {
        this.$router.push({ name: 'Devices' })
      }
    }
  }
}
</script>

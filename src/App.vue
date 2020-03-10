<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="glossy">
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          @click="leftDrawerOpen = !leftDrawerOpen"
          aria-label="Menu"
          icon="r_menu"
        />

        <q-toolbar-title>
          IoT Wrangler
        </q-toolbar-title>

        <div>v1.0.0</div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      content-class="bg-grey-2"
    >
      <q-list>
        <q-item-label header>Menu</q-item-label>
        <q-item clickable @click="doConnectDevice" :disabled="!isLoggedIn">
          <q-item-section avatar>
            <q-icon name="add_circle_outline" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Add a Device</q-item-label>
            <!-- <q-item-label caption>quasar.dev</q-item-label> -->
          </q-item-section>
        </q-item>
       <q-item clickable @click="doLogout" :v-if="!isLoggedIn">
          <q-item-section avatar>
            <q-icon name="logout" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Logout</q-item-label>
            <q-item-label caption>{{username || email}}</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view></router-view>
    </q-page-container>
  </q-layout>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import { mapState, mapActions, mapGetters } from 'vuex'
export default {
  name: 'LayoutDefault',

  components: {
    // HelloWorld
  },
  computed: {
    ...mapGetters(['isLoggedIn']),
    ...mapState({
      username: state => state.user.username,
      email: state => state.user.email
    })
  },
  data () {
    return {
      leftDrawerOpen: false
    }
  },
  methods: {
    ...mapActions(['logout']),
    async doLogout () {
      await this.logout()
      this.$router.push({ name: 'Login' })
    },
    doConnectDevice () {
      console.log('hello')
    }
  }
}
</script>

<style>
</style>

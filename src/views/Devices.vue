<template>
  <div class="home">
    <q-list bordered separator>
      <q-expansion-item v-for="device in devices" :key="device.id"
        expand-separator
        :icon="deviceType(device.get('type')).icon"
        :label="device.get('name') || device.id"
        :caption="device.get('updatedAt').toISOString() | timeago"
      >
        <component :is="deviceType(device.get('type')).component" :device="device"/>
      </q-expansion-item>
    </q-list>
  </div>
</template>

<script>
// @ is an alias to /src
import { mapState } from 'vuex'
import deviceTypes from '@/utils/deviceTypes'
export default {
  name: 'Devices',
  computed: {
    ...mapState(['devices'])
  },
  methods: {
    deviceType (type) {
      return {
        ...deviceTypes.default,
        ...deviceTypes[type]
      }
    }
  },
  components: {}
}
</script>

<template>
  <div class="text-center full-width q-pa-md q-gutter-sm ">
    <!-- <apexchart type="radialBar" height="350" :options="grillOptions" :series="grillSeries" /> -->
    <temp-control
      name="Grill"
      :temp="telemetry.grill"
      :target="settings.grillTarget"
      :max="settings.grillMax"
      icon="thermometer-half"
      @update:target="updateGrillTarget"/>
    <div class="text-center">
      <temp-control
        v-for="(probe, $index) in probeSeries" :key="probe.key"
        :name="probe.name"
        :temp="probe.temp"
        :target="probe.target"
        :icon="probe.icon"
        :max="250"
        :size="200"
        editable
        @update:target="updateProbeTarget($index, $event)"
        @update:nameicon="updateProbeNameIcon($index, $event)"/>
    </div>
  </div>
</template>
<script>
import TempControl from '@/components/TempControl'
// import { debounce } from 'lodash'

export default {
  components: { TempControl },
  props: {
    device: {
      type: Object,
      required: true
    }
  },
  data: () => ({

    // series: [67, 84]
  }),
  methods: {
    updateGrillTarget (temp) {
      const settings = {
        ...this.device.get('settings'),
        grillTarget: temp
      }
      this.device.set('settings', settings)
      this.device.save()
    },
    updateProbeTarget (idx, temp) {
      const settings = this.device.get('settings')
      settings.probeTargets[idx] = temp
      this.device.set('settings', settings)
      this.device.save()
    },
    updateProbeNameIcon (idx, [name, icon]) {
      const settings = this.device.get('settings')
      settings.probeNames[idx] = name
      settings.probeIcons[idx] = icon
      this.device.set('settings', settings)
      this.device.save()
    }
  },
  computed: {
    grillMax () {
      return this.settings.tempMax | 250
    },
    telemetry () {
      return this.device.get('telemetry')
    },
    settings () {
      return this.device.get('settings')
    },
    probeSeries () {
      return this.settings.probeTargets.map((target, idx) => {
        const temp = this.telemetry.probes[idx]
        const icon = this.settings.probeIcons[idx] || ''
        const name = this.settings.probeNames[idx] || `Probe ${idx + 1}`
        const delta = target - temp
        let colorIdx = Math.min(3, Math.round((100 * temp / target) / 25))
        colorIdx = delta >= 0 ? colorIdx : 4

        return {
          name,
          color: ['lime', 'yellow-14', 'amber', 'orange', 'red'][colorIdx],
          targetP: target / this.grillMax,
          tempP: temp / this.grillMax,
          delta,
          target,
          temp,
          icon
        }
      })
    }
  },
  filters: {
    temp (num) {
      return `${num}c`
    }
  }
}
</script>

<style lang="css" scoped>
h6 {
  margin-bottom: 0;
  margin-top: 20px;
}
.probe-label {
  padding-top: 0;
  margin-top: 0;
  line-height: .7;
  margin-left: 8px;

  /* border-top: 1px solid red; */
}
.probe-label .q-badge{
  font-weight: bold;
  text-shadow: 1px 1px 1px rgba(0, 0, 0, .2);
}
.q-linear-progress {
  background: rgba(0,0,0,0.035);
}
</style>

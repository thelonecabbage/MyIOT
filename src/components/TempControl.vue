<template>
<div class="inline-block relative">
    <q-knob
        show-value
        font-size="10px"
        class="q-ma-md"
        :value="target"
        @input="setTarget = $event"
        @change="updateTarget"
        :min="0"
        :max="max"
        :size="`${size}px`"
        :readonly="locked"
        :thickness="0.225"
        color="primary"
        track-color="grey-3">
        <q-circular-progress
          show-value
          font-size="10px"
          class="q-ma-md"
          :value="temp"
          :min="0"
          :max="max"
          :size="`${size*.8}px`"
          :thickness="0.3"
          :color="tempColor"
          :center-color="'white'"
          track-color="grey-3"

        >
        <div class="text-center label-text">
          <div class="q-mr-xs text-weight-bolder text-h6 text-capitalize" :class="['text-' + tempColor]">
            <q-icon :name="faIcon(icon)" class="q-mr-xs q-ml-xs" v-if="icon"/>
            <span class="inline-block">{{name}}</span>
          </div>
          <div class="text-subtitle2">{{temp | temperature}} / {{(setTarget || target) | temperature}}</div>
        </div>
        </q-circular-progress>
      </q-knob>
      <div
        class="btn-cap absolute-center"
        @click.capture.stop="openModal"></div>

      <q-dialog v-model="editModal" persistent>
        <q-card style="min-width: 350px">
          <q-card-section>
            <div class="text-h6">Edit</div>
          </q-card-section>

          <q-card-section class="q-pt-none">
            <q-input dense label="Sensor Name" v-model="editName" autofocus />
            <q-btn-toggle
                v-model="editIcon"
                dense
                toggle-color="primary"
                flat
                stack
                :options="iconOptions"
              />
          </q-card-section>
          <q-card-actions align="right" class="text-primary">
            <q-btn flat label="Cancel" v-close-popup />
            <q-btn flat label="Update" @click="$emit('update:nameicon', [editName, editIcon])" v-close-popup />
          </q-card-actions>
        </q-card>
      </q-dialog>
      <q-icon :name="locked ? 'lock' : 'lock_open'" size="25px" class="absolute-bottom-left" @click="locked=!locked"/>
    </div>
</template>
<script lang="ts">
import Vue from 'vue'
//     <q-icon name="fas fa-bacon"/>

const icons = [
  'thermometer-half',
  'bacon',
  // 'bread-loaf',
  // 'burrito',
  'hamburger',
  'hotdog',
  'drumstick-bite',
  'egg',
  'fish',
  'pizza-slice',
  'pepper-hot',
  'atom',
  'radiation',
  'poop',
  'fire',
  'fire-alt',
  'baby'
]
export default Vue.extend({
  props: {
    temp: {
      type: Number,
      required: true
    },
    target: {
      type: Number,
      required: true
    },
    max: {
      type: Number,
      default: 500
    },
    size: {
      type: Number,
      default: 300
    },
    name: {
      type: String,
      default: 'probe'
    },
    icon: {
      type: String,
      default: ''
    },
    editable: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    setTarget: 0,
    editName: '',
    editIcon: '',
    editModal: false,
    icons,
    locked: true
  }),
  methods: {
    updateTarget (ev) {
      this.setTarget = ev
      this.$emit('update:target', ev)
    },
    faIcon (name) {
      return `fa fa-${name}`
    },
    openModal () {
      if (this.editable && !this.locked) {
        this.editIcon = this.icon
        this.editName = this.name
        this.editModal = true
      }
    }
  },
  computed: {
    tempColor () {
      // const { target, setTarget, temp } = <{ target: number, setTarget: number, temp: number }> this
      const target: number = this.target
      // const setTarget: number = this.setTarget
      // const temp: number = this.temp
      // const target = this.setTarget || this.target
      const delta = target - this.temp as number
      let colorIdx = Math.min(4, Math.round((100 * this.temp / target) / 25)) - 1
      colorIdx = delta >= 0 ? colorIdx : 4
      return ['lime', 'yellow-14', 'amber', 'orange', 'red'][colorIdx]
    },
    iconOptions (): Array<object> {
      // const faIcon:any = this.faIcon
      return [
        {
          icon: this.faIcon('ban'),
          value: ''
        },
        ...this.icons.map(icon => ({
          icon: this.faIcon(icon),
          value: icon
        })
        )
      ]
    }
  },
  filters: {
    temperature (num: number) {
      return `${num}c`
    }
  }
})
</script>
<style scoped>
.inline-block {
  display: inline-block;
  position: relative;
}
.btn-cap {
  width: 50%;
  height: 50%;
  border-radius: 100%;
  /* border: 1px solid red; */
}
.label-text {
  max-width: 68%;
  max-height: 68%;
}
</style>

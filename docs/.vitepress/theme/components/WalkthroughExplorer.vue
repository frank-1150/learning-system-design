<script setup lang="ts">
import { computed, ref } from 'vue'
import { walkthroughs } from '../../content.mjs'

const props = defineProps<{ chapter: number }>()
const item = computed(() => walkthroughs[String(props.chapter)])
const active = ref(0)

function move(delta: number) {
  const count = item.value.steps.length
  active.value = (active.value + delta + count) % count
}
</script>

<template>
  <section v-if="item" class="walkthrough-explorer" tabindex="0" @keydown.left="move(-1)" @keydown.right="move(1)">
    <header>
      <div>
        <p class="eyebrow">INTERACTIVE WALKTHROUGH</p>
        <h2>{{ item.title }}</h2>
      </div>
      <span>{{ active + 1 }} / {{ item.steps.length }}</span>
    </header>
    <div class="mechanism-stage">
      <div class="system-node source">{{ item.steps[active].from }}</div>
      <div class="flow-line"><span>→</span></div>
      <div class="system-node focus">{{ item.steps[active].focus }}</div>
      <div class="flow-line"><span>→</span></div>
      <div class="system-node target">{{ item.steps[active].to }}</div>
    </div>
    <div class="step-copy">
      <p class="step-label">步骤 {{ active + 1 }}</p>
      <h3>{{ item.steps[active].label }}</h3>
      <p>{{ item.steps[active].detail }}</p>
      <p class="tradeoff"><strong>权衡：</strong>{{ item.steps[active].tradeoff }}</p>
    </div>
    <footer>
      <button type="button" aria-label="上一步" @click="move(-1)">←</button>
      <div class="step-dots">
        <button v-for="(_, index) in item.steps" :key="index" type="button" :class="{ active: index === active }" :aria-label="`跳到步骤 ${index + 1}`" @click="active = index" />
      </div>
      <button type="button" aria-label="下一步" @click="move(1)">→</button>
    </footer>
  </section>
</template>


<script setup lang="ts">
import { ref } from 'vue'

defineProps<{ title: string; open?: boolean }>()
const expanded = ref(false)
</script>

<template>
  <section class="answer-step" :class="{ expanded }">
    <button type="button" :aria-expanded="expanded" @click="expanded = !expanded">
      <span>{{ title }}</span>
      <span aria-hidden="true">{{ expanded ? '−' : '+' }}</span>
    </button>
    <div v-if="expanded || open" class="answer-step-body"><slot /></div>
  </section>
</template>


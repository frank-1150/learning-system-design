<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{ question: string; options: string[]; answer: number; explanation: string }>()
const selected = ref<number | null>(null)
</script>

<template>
  <section class="knowledge-check">
    <p class="eyebrow">KNOWLEDGE CHECK</p>
    <h3>{{ question }}</h3>
    <div class="check-options">
      <button
        v-for="(option, index) in options"
        :key="option"
        type="button"
        :class="{ selected: selected === index, correct: selected !== null && index === answer, wrong: selected === index && index !== answer }"
        @click="selected = index"
      >{{ option }}</button>
    </div>
    <p v-if="selected !== null" class="check-explanation">
      <strong>{{ selected === answer ? '回答正确。' : '再想一步。' }}</strong> {{ explanation }}
    </p>
  </section>
</template>


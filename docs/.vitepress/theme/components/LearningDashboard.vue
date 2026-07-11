<script setup lang="ts">
import { computed } from 'vue'
import { withBase } from 'vitepress'
import { chapters } from '../../content.mjs'
import { useProgress } from '../progress'

const { completed } = useProgress()
const parts = computed(() => {
  const groups = new Map<string, typeof chapters>()
  chapters.forEach((chapter) => {
    const list = groups.get(chapter.part) || []
    list.push(chapter)
    groups.set(chapter.part, list)
  })
  return [...groups.entries()]
})

const chapterDone = computed(() => chapters.filter((chapter) => completed.value.has(`chapter-${chapter.chapter}`)).length)
const questionDone = computed(() => chapters.flatMap((chapter) => chapter.questions).filter((question) => completed.value.has(`question-${question.slug}`)).length)
const totalDone = computed(() => chapterDone.value + questionDone.value)
const progressPercent = computed(() => Math.round(totalDone.value / 48 * 100))
const nextChapter = computed(() => chapters.find((chapter) => !completed.value.has(`chapter-${chapter.chapter}`)) || chapters[0])
</script>

<template>
  <main class="learning-dashboard">
    <header class="dashboard-header">
      <div>
        <p class="eyebrow">DESIGNING DATA-INTENSIVE APPLICATIONS</p>
        <h1>把系统设计原理，练成工程判断</h1>
        <p>12 章交互式导读，36 道产品、机制与事故题。沿着状态、顺序、故障和演化，完成一轮可检验的 DDIA 精读。</p>
      </div>
      <a class="continue-link" :href="withBase(nextChapter.walkthroughPath)">
        <span>继续学习</span>
        <strong>Ch{{ nextChapter.chapter }} · {{ nextChapter.titleZh }}</strong>
        <span aria-hidden="true">→</span>
      </a>
    </header>

    <section class="progress-band" aria-label="学习进度">
      <div><strong>{{ progressPercent }}%</strong><span>总进度</span></div>
      <div><strong>{{ chapterDone }}/12</strong><span>章节</span></div>
      <div><strong>{{ questionDone }}/36</strong><span>面试题</span></div>
      <div class="progress-track"><span :style="{ width: `${progressPercent}%` }" /></div>
    </section>

    <section v-for="([part, items], partIndex) in parts" :key="part" class="part-section">
      <header>
        <span class="part-number">0{{ partIndex + 1 }}</span>
        <div><p class="eyebrow">{{ part.split(' · ')[0] }}</p><h2>{{ part.split(' · ')[1] }}</h2></div>
      </header>
      <div class="chapter-list">
        <a v-for="chapter in items" :key="chapter.chapter" :href="withBase(chapter.walkthroughPath)" class="chapter-row">
          <span class="chapter-index">{{ String(chapter.chapter).padStart(2, '0') }}</span>
          <span class="chapter-title"><strong>{{ chapter.titleZh }}</strong><small>{{ chapter.titleEn }}</small></span>
          <span class="chapter-stats">3 题</span>
          <span class="chapter-state" :class="{ done: completed.has(`chapter-${chapter.chapter}`) }">{{ completed.has(`chapter-${chapter.chapter}`) ? '✓' : '→' }}</span>
        </a>
      </div>
    </section>
  </main>
</template>


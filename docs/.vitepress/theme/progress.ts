import { computed, onMounted, ref } from 'vue'

const STORAGE_KEY = 'ddia-progress:v1'
const completed = ref<Set<string>>(new Set())
let loaded = false

function load() {
  if (loaded || typeof window === 'undefined') return
  loaded = true
  try {
    const saved = JSON.parse(window.localStorage.getItem(STORAGE_KEY) || '[]')
    completed.value = new Set(Array.isArray(saved) ? saved : [])
  } catch {
    completed.value = new Set()
  }
}

function save() {
  if (typeof window === 'undefined') return
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify([...completed.value]))
}

export function useProgress(id?: string) {
  onMounted(load)
  const isComplete = computed(() => Boolean(id && completed.value.has(id)))
  const toggle = () => {
    if (!id) return
    const next = new Set(completed.value)
    next.has(id) ? next.delete(id) : next.add(id)
    completed.value = next
    save()
  }
  return { completed, isComplete, toggle }
}


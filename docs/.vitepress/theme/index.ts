import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import LearningDashboard from './components/LearningDashboard.vue'
import WalkthroughExplorer from './components/WalkthroughExplorer.vue'
import KnowledgeCheck from './components/KnowledgeCheck.vue'
import ProgressToggle from './components/ProgressToggle.vue'
import AnswerStep from './components/AnswerStep.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('LearningDashboard', LearningDashboard)
    app.component('WalkthroughExplorer', WalkthroughExplorer)
    app.component('KnowledgeCheck', KnowledgeCheck)
    app.component('ProgressToggle', ProgressToggle)
    app.component('AnswerStep', AnswerStep)
  }
} satisfies Theme


import { defineConfig } from 'vitepress'
import { chapters } from './content.mjs'

const chapterSidebar = chapters.map((chapter) => ({
  text: `Ch${chapter.chapter} ${chapter.titleZh}`,
  collapsed: true,
  items: [
    { text: '交互式导读', link: chapter.walkthroughPath },
    ...chapter.questions.map((question) => ({ text: question.shortTitle, link: question.path }))
  ]
}))

export default defineConfig({
  lang: 'zh-CN',
  title: 'DDIA 系统设计学习站',
  description: '用交互式导读和系统设计面试题精读 Designing Data-Intensive Applications',
  base: '/learning-system-design/',
  cleanUrls: true,
  lastUpdated: true,
  head: [
    ['meta', { name: 'theme-color', content: '#0f766e' }],
    ['meta', { name: 'og:type', content: 'website' }]
  ],
  markdown: { lineNumbers: true },
  themeConfig: {
    logo: '/logo.svg',
    nav: [
      { text: '学习路径', link: '/' },
      { text: '章节', link: '/chapters/' },
      { text: '面试题', link: '/questions/' },
      { text: '关于', link: '/about' }
    ],
    sidebar: {
      '/chapters/': [{ text: 'DDIA 第一版', items: chapterSidebar }],
      '/questions/': [{ text: '36 道系统设计题', items: chapterSidebar }]
    },
    search: { provider: 'local' },
    socialLinks: [{ icon: 'github', link: 'https://github.com/frank-1150/learning-system-design' }],
    outline: { label: '本页内容', level: [2, 3] },
    docFooter: { prev: '上一页', next: '下一页' },
    lastUpdated: { text: '最后更新' },
    returnToTopLabel: '回到顶部',
    sidebarMenuLabel: '目录',
    darkModeSwitchLabel: '主题',
    footer: {
      message: '学习笔记与原创实现采用 MIT；书中引用内容版权归原作者及出版社所有。',
      copyright: 'Copyright © 2026 Frank Luo'
    }
  }
})


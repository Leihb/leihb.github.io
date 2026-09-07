import { defineConfig } from 'vitepress'

import shared from './shared'
import zh from './zh'

// 单语站：zh 覆盖 shared，但 themeConfig 要合并而不是整块替换，
// 否则 shared 里的搜索、右侧目录、外链图标会丢。
export default defineConfig({
  ...shared,
  ...zh,
  themeConfig: {
    ...shared.themeConfig,
    ...zh.themeConfig,
  },
})

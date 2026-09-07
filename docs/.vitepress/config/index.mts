import { defineConfig } from 'vitepress'

import shared from './shared'
import zh from './zh'

export default defineConfig({
  ...shared,
  ...zh,
})

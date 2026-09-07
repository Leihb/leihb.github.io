# leihb.github.io

个人站：一个开源 agent（[octo-agent](https://github.com/open-octo/octo-agent)）、三本书、一些想法，还有屏幕之外的摄影和路亚。

基于 [Justin3go/justin3go.com](https://github.com/Justin3go/justin3go.com) 改造（代码 MIT 协议），VitePress + Vue 3。
他的文章、笔记、英文站、赞助页、人物素材和统计/评论/搜索配置已全部移除，只保留主题代码和首页分镜滚动的实现。

## 开发

```bash
pnpm i
pnpm docs:dev      # http://localhost:5173
pnpm docs:build    # 产物在 docs/.vitepress/dist
pnpm test          # 首页分镜动画的单测
```

## 改哪里

| 想改什么 | 在哪 |
| --- | --- |
| 站名、域名、作者、邮箱、GitHub | `docs/.vitepress/site.ts`，全站只此一处 |
| 首页文案、联系方式 | `docs/.vitepress/theme/components/ProfileHome.vue` 顶部的 `copy` 与 `socials` |
| 作品卡片与"更多项目" | `docs/.vitepress/theme/components/ProfileProjects.vue` |
| 时间线 | `docs/.vitepress/theme/components/ProfileTimeline.vue` |
| 分镜字幕 | `docs/.vitepress/theme/components/PaperJourney.vue` 的 `descriptions` |
| 博客文章 | `docs/posts/YYYY/MM/DD-slug.md`，frontmatter 要有 `title`、`date`、`tags`；正文里用两行 `<!-- DESC SEP -->` 夹住摘要 |
| 导航、页脚 | `docs/.vitepress/config/zh.ts` |
| 评论区（giscus） | 建好仓库、开 Discussions 后填 `Comment.vue` 的 repo / category id，再在 `theme/index.ts` 打开 `doc-after` |

## 首页滚动人物

`docs/public/paper-journey/*.png` 是六张 2×2 精灵图（intro / code / photo / fishing / walk / chat），
用阿里云百炼 qwen-image-2.0-pro 文生图生成，提示词在 `design/paper-journey-prompts/`。
生成结果是粉底 RGB，用 `scripts/key-sprites.py` 抠成透明底并压到 1024px 再放进来。
人物系统的设计说明见 `design/paper-journey.md`（沿用自原仓库）。

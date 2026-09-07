import path from "node:path";
import { writeFileSync } from "node:fs";
import { Feed } from "feed";
import { createContentLoader, type SiteConfig } from "vitepress";
import { site } from "../../site";

const hostname = site.url;

export async function createRssFileZH(config: SiteConfig) {
  const feed = new Feed({
    title: site.name,
    description: site.description,
    id: hostname,
    link: hostname,
    language: "zh-Hans",
    image: `${hostname}/og.png`,
    favicon: `${hostname}/favicon.svg`,
    copyright: `Copyright© ${site.since}-present ${site.author}`,
  });

  const posts = await createContentLoader("posts/**/*.md", {
    excerpt: true,
    render: true,
  }).load();

  posts.sort((a, b) => Number(+new Date(b.frontmatter.date) - +new Date(a.frontmatter.date)));

  for (const { url, excerpt, html, frontmatter } of posts) {
    // 仅保留最近 5 篇文章
    if (feed.items.length >= 5) {
      break;
    }

    feed.addItem({
      title: frontmatter.title,
      id: `${hostname}${url}`,
      link: `${hostname}${url}`,
      description: excerpt,
      content: html,
      author: [
        {
          name: site.author,
          email: site.email || undefined,
          link: hostname,
        },
      ],
      date: frontmatter.date,
    });
  }

  writeFileSync(path.join(config.outDir, "feed.xml"), feed.rss2(), "utf-8");
}

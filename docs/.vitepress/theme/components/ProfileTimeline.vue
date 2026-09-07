<template>
	<ol class="profile-timeline">
		<li v-for="(item, index) in items" :key="item.time" :class="{ current: index === 0 }">
			<span class="timeline-dot" aria-hidden="true"></span>
			<time>{{ item.time }}</time>
			<div>
				<strong>{{ item.title }}</strong>
				<p>{{ item.description }}</p>
			</div>
		</li>
	</ol>
</template>

<script setup lang="ts">
// 时间线：前半段学历与工作（Roy 2026-09-07 提供），后半段创作节点（日期来自各仓库 / 发布记录）。倒序展示，最新在上。
const items = [
	{ time: "2011 — 2015", title: "本科 · 信息管理与信息系统", description: "开始写代码。" },
	{ time: "2015 — 2017", title: "某外企 · 后端工程师", description: "第一份工作，从零开始做后端。" },
	{ time: "2017 — 2018", title: "某初创公司 · Rails 后端工程师", description: "小团队，什么都得自己上手。" },
	{ time: "2018 — 2022", title: "某大厂 · Go 后端工程师", description: "换到 Go，做大流量下的后端服务。" },
	{ time: "2022 — 至今", title: "某旅游行业独角兽 · 后端工程师", description: "白天写后端，业余做 agent、写书。" },
	{ time: "2026.05", title: "octo-agent 开源", description: "一个单二进制、自托管的 AI agent，在 open-octo 组织下开源。" },
	{ time: "2026.07", title: "开始写《笨办法学 Agent · 亲手打造一个 harness》", description: "不用框架，一个练习一个练习地把 harness 写出来。" },
	{ time: "2026.08", title: "第一本完结", description: "32 个练习全部完结，每个练习结束时手里的代码都能跑。" },
	{ time: "2026.09", title: "第二本发完，第三本开写", description: "《用 LangGraph 上线》Part 1 到 4 发完；《让 agent 替你干活》开始连载。" },
].reverse();
</script>

<style scoped>
.profile-timeline { list-style: none; padding: 0; margin: 0; }
.profile-timeline li { position: relative; margin: 0; padding: 0 0 30px 28px; border-left: 1px solid var(--vp-c-divider); }
.profile-timeline li:last-child { padding-bottom: 0; border-left-color: transparent; }
.timeline-dot { position: absolute; left: -4px; top: 5px; width: 7px; height: 7px; border: 1px solid var(--vp-c-text-3); border-radius: 50%; background: var(--vp-c-bg); }
.current .timeline-dot { background: var(--vp-c-brand-1); border-color: var(--vp-c-brand-1); box-shadow: 0 0 0 4px var(--vp-c-brand-soft); }
.profile-timeline time { display: block; margin-bottom: 8px; font: 10px var(--vp-font-family-mono); color: var(--vp-c-text-2); }
.current time { color: var(--vp-c-brand-1); }
.profile-timeline strong { font-size: 15px; line-height: 1.6; font-weight: 550; }
.profile-timeline p { margin: 7px 0 0; font-size: 13px; line-height: 1.8; color: var(--vp-c-text-2); }
@media (max-width: 640px) { .profile-timeline li { padding-left: 25px; } }
</style>

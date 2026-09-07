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
// 草稿：先放创作时间线（日期来自各仓库 / 发布记录）。学历与工作经历待 Roy 提供后补进来。
const items = [
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

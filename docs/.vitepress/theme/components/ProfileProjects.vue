<template>
	<div class="profile-projects" :class="{ 'is-motion-disabled': !props.motion || reducedMotion }">
		<div class="profile-project-grid">
			<a
				v-for="(project, index) in cardProjects"
				:key="project.name"
				class="profile-project-card"
				:href="project.url"
				target="_blank"
				rel="noopener noreferrer"
			>
				<div class="profile-project-media" @pointermove="handlePointerMove" @pointerleave="resetPointer">
					<img :src="withBase(project.image)" :alt="`${project.name} ${previewLabel}`" width="1200" height="675" loading="lazy" />
				</div>
				<div class="profile-project-copy">
					<div class="profile-project-caption" aria-hidden="true"><span class="profile-project-number">{{ String(index + 1).padStart(2, "0") }}</span><span class="profile-project-domain">{{ project.domain }}</span></div>
					<div class="profile-project-title">
						<strong>{{ project.name }}</strong>
						<span aria-hidden="true">↗</span>
					</div>
					<p>{{ project.description }}</p>
				</div>
			</a>
		</div>
		<section class="profile-more-projects" aria-labelledby="more-projects-title">
			<h3 id="more-projects-title">更多项目</h3>
			<ul class="profile-project-list">
				<li v-for="project in textProjects" :key="project.name">
					<a class="profile-project-row" :href="project.url" target="_blank" rel="noopener noreferrer">
						<span class="profile-project-row-copy">
							<span class="profile-project-row-name"><strong>{{ project.name }}</strong><span class="profile-project-row-arrow" aria-hidden="true">↗</span></span>
							<span class="profile-project-row-description">{{ project.description }}</span>
						</span>
					</a>
				</li>
			</ul>
		</section>
	</div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from "vue";
import { withBase } from "vitepress";

const props = withDefaults(defineProps<{ motion?: boolean }>(), {
	motion: true,
});

// 卡片项目：octo 是主线，三本书围着它。描述取自各仓库 README / GitHub 描述。
const cardProjects = [
	{ name: "octo-agent", domain: "octo-agent.dev", url: "https://octo-agent.dev", image: "/projects/octo-agent.png",
		description: "开箱即用的自托管 AI agent。一个 Go 二进制，任意模型，八个入口，数据不离开你的机器。" },
	{ name: "笨办法学 Agent · 亲手打造一个 harness", domain: "leihb.com", url: "https://leihb.com/learn-agent-the-hard-way/", image: "/projects/learn-agent.png",
		description: "不用框架，32 个练习亲手写出一个 agent harness 的每一层。系列第一本，已完结。" },
	{ name: "笨办法学 Agent · 用 LangGraph 上线", domain: "leihb.com", url: "https://leihb.com/langgraph-in-action/", image: "/projects/langgraph.png",
		description: "用 LangGraph 把场景 agent 做出来、放到线上，不需要先读第一本。系列第二本。" },
	{ name: "让 agent 替你干活", domain: "leihb.com", url: "https://leihb.com/octo-at-work/", image: "/projects/octo-at-work.png",
		description: "不写代码，用 octo 把活干完。给不写代码的打工人的本地 agent 实战书，系列第三本，连载中。" },
];

// 文字列表：围绕 octo 的扩展和几个 agent skill。
const textProjects = [
	{ name: "octo-vscode", url: "https://github.com/open-octo/octo-vscode", description: "octo 的 VS Code 扩展。" },
	{ name: "octo-obsidian", url: "https://github.com/open-octo/octo-obsidian", description: "octo 的 Obsidian 插件。" },
	{ name: "vision-helper", url: "https://github.com/Leihb/vision-helper", description: "给只会读文字的 agent 装眼睛：走任意 OpenAI 兼容的视觉接口描述图片，图里的文字逐字转写。" },
	{ name: "xiaohongshu-teardown", url: "https://github.com/Leihb/xiaohongshu-teardown", description: "让 Claude 看懂并拆解小红书笔记：硬字幕提成逐字稿，再拆钩子和叙事结构。" },
	{ name: "CodexGuide", url: "https://codexguide.ai", description: "面向初学者、创作者、开发者与团队的 Codex 实践指南。" },
	{ name: "WorkBuddyGuide", url: "https://workbuddy.homes/", description: "开源的 WorkBuddy 实战蓝皮书：教程、真实工作流、Skills、MCP、自动化与多智能体实践。" },
];

const previewLabel = "项目预览图";

const reducedMotion = ref(false);
let motionQuery: MediaQueryList | undefined;

function syncMotionPreference() {
	reducedMotion.value = motionQuery?.matches ?? false;
}

function handlePointerMove(event: PointerEvent) {
	if (!props.motion || reducedMotion.value || (event.pointerType && event.pointerType !== "mouse")) return;
	const media = event.currentTarget as HTMLElement | null;
	if (!media) return;

	const bounds = media.getBoundingClientRect();
	if (!bounds.width || !bounds.height) return;

	const x = Math.max(-0.5, Math.min(0.5, (event.clientX - bounds.left) / bounds.width - 0.5));
	const y = Math.max(-0.5, Math.min(0.5, (event.clientY - bounds.top) / bounds.height - 0.5));
	media.style.setProperty("--project-tilt-x", `${(-y * 6).toFixed(2)}deg`);
	media.style.setProperty("--project-tilt-y", `${(x * 6).toFixed(2)}deg`);
	media.style.setProperty("--project-shift-x", `${(x * 4).toFixed(2)}px`);
	media.style.setProperty("--project-shift-y", `${(y * 4).toFixed(2)}px`);
	media.style.setProperty("--project-scale", "1.018");
}

function resetPointer(event: PointerEvent) {
	const media = event.currentTarget as HTMLElement | null;
	if (!media) return;
	media.style.removeProperty("--project-tilt-x");
	media.style.removeProperty("--project-tilt-y");
	media.style.removeProperty("--project-shift-x");
	media.style.removeProperty("--project-shift-y");
	media.style.removeProperty("--project-scale");
}

onMounted(() => {
	motionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
	syncMotionPreference();
	motionQuery.addEventListener("change", syncMotionPreference);
});

onUnmounted(() => {
	motionQuery?.removeEventListener("change", syncMotionPreference);
});
</script>

<style scoped>
.profile-projects {
  width: 100%; max-width: 720px; margin: 36px auto 40px;
}
.profile-project-grid {
  display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 30px 24px;
}
.profile-more-projects { margin: 42px 6px 0; }
.profile-more-projects h3 {
  position: relative; display: inline-block; margin: 0 0 24px; padding: 0 2px 7px;
  color: var(--vp-c-text-1); font-size: 18px; font-weight: 550; line-height: 1.5; letter-spacing: -.02em;
}
.profile-more-projects h3::after {
  content: ''; position: absolute; left: 0; right: -5px; bottom: 2px; height: 5px;
  border-bottom: 2px solid color-mix(in srgb, var(--vp-c-brand-1) 45%, transparent);
  border-radius: 0 0 50% 35%; transform: rotate(-2deg);
}
.profile-project-list { display: grid; gap: 15px; list-style: none; margin: 0; padding: 0; }
.profile-project-list > li { margin: 0; padding: 0; }
.profile-project-row {
  display: grid; grid-template-columns: 12px minmax(0, 1fr); gap: 12px; align-items: baseline;
  padding: 3px 0; color: var(--vp-c-text-1); text-decoration: none !important;
}
.profile-project-row::before {
  content: ''; width: 10px; height: 5px; align-self: start; margin-top: 10px;
  border-top: 1px solid var(--vp-c-text-3); border-radius: 50%; transform: rotate(-12deg);
}
.profile-project-row-copy { min-width: 0; font-size: 13px; line-height: 1.95; }
.profile-project-row-name { display: inline-flex; align-items: baseline; gap: 6px; margin-right: 12px; }
.profile-project-row strong {
  font-size: 14px; font-weight: 550; line-height: 1.65;
  text-decoration: underline; text-decoration-style: dashed;
  text-decoration-color: color-mix(in srgb, var(--vp-c-text-3) 50%, transparent); text-underline-offset: 5px;
}
.profile-project-row-description { color: var(--vp-c-text-2); }
.profile-project-row-arrow { font-size: 12px; color: var(--vp-c-brand-1); }
.profile-project-row:hover strong, .profile-project-row:hover .profile-project-row-arrow { color: var(--vp-c-brand-1); }
.profile-project-row:focus-visible { outline: 2px solid var(--vp-c-brand-1); outline-offset: 3px; }
.profile-project-card {
  --card-angle: -1deg;
  --card-paper: color-mix(in srgb, var(--vp-c-bg-soft) 92%, var(--vp-c-text-1) 8%);
  position: relative; isolation: isolate; display: flex; flex-direction: column; min-width: 0;
  padding: 13px 13px 8px; color: var(--vp-c-text-1); cursor: pointer; text-decoration: none !important;
  transform: rotate(var(--card-angle));
  filter: drop-shadow(1px 3px 1px color-mix(in srgb, var(--vp-c-text-1) 12%, transparent));
  transition: transform .22s ease, filter .22s ease;
}
.profile-project-card:nth-child(2n) { --card-angle: 1deg; }
.profile-project-card:nth-child(3n) { --card-angle: -.55deg; }
.profile-project-card::before {
  content: ''; position: absolute; inset: 0; z-index: -1; pointer-events: none;
  background: repeating-linear-gradient(0deg, transparent 0 3px, color-mix(in srgb, var(--vp-c-text-1) 2%, transparent) 3px 4px), var(--card-paper);
  clip-path: polygon(0 2px,7% 0,15% 3px,24% 1px,34% 3px,43% 0,54% 2px,66% 0,77% 3px,88% 1px,100% 3px,calc(100% - 2px) 17%,100% 31%,calc(100% - 3px) 46%,100% 61%,calc(100% - 2px) 79%,100% calc(100% - 3px),91% 100%,82% calc(100% - 4px),71% 100%,60% calc(100% - 2px),49% 100%,38% calc(100% - 4px),27% 100%,16% calc(100% - 2px),7% 100%,0 calc(100% - 3px),2px 83%,0 66%,3px 49%,0 34%,2px 18%);
}
.profile-project-card::after {
  content: ''; position: absolute; top: -9px; left: 34%; width: 66px; height: 23px; z-index: 2; pointer-events: none;
  background: color-mix(in srgb, var(--vp-c-brand-1) 18%, var(--vp-c-bg-soft));
  opacity: .88; transform: rotate(-7deg);
  clip-path: polygon(3% 0,98% 2%,96% 18%,100% 35%,97% 52%,100% 72%,97% 100%,0 97%,3% 78%,0 58%,3% 38%,0 17%);
}
.profile-project-card:nth-child(2n)::after { left: 49%; transform: rotate(8deg); }
.profile-project-card:hover { transform: translateY(-4px) rotate(0); filter: drop-shadow(2px 6px 2px color-mix(in srgb, var(--vp-c-text-1) 15%, transparent)); }
.profile-project-card:active { transform: translateY(-1px) rotate(0); }
.profile-project-card:focus-visible { outline: 2px solid var(--vp-c-brand-1); outline-offset: 5px; }
.profile-project-media {
  position: relative; overflow: hidden; background: var(--vp-c-bg);
  --project-tilt-x: 0deg; --project-tilt-y: 0deg; --project-shift-x: 0px; --project-shift-y: 0px; --project-scale: 1;
}
.profile-project-media > img {
  display: block; width: 100%; aspect-ratio: 16 / 9; margin: 0; border: 0; border-radius: 0; object-fit: cover; cursor: inherit;
  transform: perspective(900px) rotateX(var(--project-tilt-x)) rotateY(var(--project-tilt-y)) translate3d(var(--project-shift-x), var(--project-shift-y), 0) scale(var(--project-scale));
  transform-origin: center; transition: transform 240ms cubic-bezier(.22,1,.36,1);
}
.profile-project-copy { display: flex; flex: 1; flex-direction: column; padding: 16px 6px 17px; }
.profile-project-caption { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; color: var(--vp-c-text-2); font: 10px/1.4 var(--vp-font-family-mono); letter-spacing: .02em; }
.profile-project-number { flex: 0 0 auto; color: var(--vp-c-brand-1); font-variant-numeric: tabular-nums; border-right: 1px solid var(--vp-c-divider); padding-right: 8px; }
.profile-project-domain { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.profile-project-title { display: flex; align-items: baseline; justify-content: space-between; gap: 8px; }
.profile-project-title strong { font-size: 15px; font-weight: 600; line-height: 1.4; overflow-wrap: anywhere; }
.profile-project-title span { flex: 0 0 auto; font-size: 16px; color: var(--vp-c-brand-1); }
.profile-project-card:hover .profile-project-title strong { color: var(--vp-c-brand-1); }
.profile-project-copy p { margin: 9px 0 0; font-size: 13px; line-height: 1.75; color: var(--vp-c-text-2); }
.profile-projects.is-motion-disabled .profile-project-media > img { transform: none; transition: none; }
.profile-projects.is-motion-disabled .profile-project-card { transition: none; }
@media (prefers-reduced-motion: reduce) { .profile-project-media > img { transform: none; transition: none; }.profile-project-card { transition: none; } }
@media (max-width: 640px) {
  .profile-projects { max-width: none; }
  .profile-project-grid { grid-template-columns: 1fr; gap: 29px; }
  .profile-more-projects { margin: 34px 4px 0; }
  .profile-more-projects h3 { margin-bottom: 20px; font-size: 17px; }
  .profile-project-row { gap: 10px; }
  .profile-project-row-description { display: block; margin-top: 4px; }
  .profile-project-card { --card-angle: -.5deg; }
  .profile-project-card:nth-child(2n) { --card-angle: .5deg; }
  .profile-project-copy { padding: 16px 8px 18px; }
}
</style>

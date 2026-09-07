// https://vitepress.dev/guide/custom-theme
import { h } from "vue";
import Theme from 'vitepress/theme' // https://vitepress.dev/zh/guide/extending-default-theme#using-different-fonts
// 引入组件库的少量全局样式变量
import 'tdesign-vue-next/es/style/index.css';

import "./style.css";
import Comment from "./components/Comment.vue";
import ImageViewer from "./components/ImageViewer.vue"
import GoBack from "./components/GoBack.vue";

export default {
	...Theme,
	Layout: () => {
		return h(Theme.Layout, null, {
			// https://vitepress.dev/guide/extending-default-theme#layout-slots
			// TODO(Roy): 评论区依赖 giscus，需要个人站仓库开 Discussions 后在 Comment.vue 填 repo/category id 再启用
			// "doc-after": () => h(Comment),
			"doc-top": () => h(ImageViewer),
			"aside-top": () => h(GoBack),
		});
	},

	enhanceApp({ app }: any) {
		app.component("Comment", Comment);
		app.component("ImageViewer", ImageViewer);
		app.component("GoBack", GoBack);
	},
};

import { createRouter, createWebHashHistory } from "vue-router";
import Wednesday from "../src/views/Wednesday.vue";
import Home from "../src/views/Home.vue";
import Friday from "../src/views/Friday.vue";
import Monday from "../src/views/Monday.vue";
import Saturday from "../src/views/Saturday.vue";
import Sunday from "../src/views/Sunday.vue";
import Thursday from "../src/views/Thursday.vue";
import Tuesday from "../src/views/Tuesday.vue";

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: "/",
      component: Home,
    },
    {
      path: "/1",
      component: Monday,
    },
    {
      path: "/2",
      component: Tuesday,
    },
    {
      path: "/3",
      component: Wednesday,
    },
    {
      path: "/4",
      component: Thursday,
    },
    {
      path: "/5",
      component: Friday,
    },
    {
      path: "/6",
      component: Saturday,
    },
    {
      path: "/7",
      component: Sunday,
    },
  ],
});

// 2. 导出路由实例
export default router;

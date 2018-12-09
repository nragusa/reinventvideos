import Vue from "vue";
import Router from "vue-router";
import Videos from "@/views/Videos.vue";

Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      name: "videos",
      component: Videos
    }
  ]
});

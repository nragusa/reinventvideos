import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import InstantSearch from "vue-instantsearch";

Vue.config.productionTip = false;
Vue.use(InstantSearch);

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");

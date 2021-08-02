import Vue from 'vue'
import Router from 'vue-router'
// Import all components
import Login from '../components/Login.vue';
import Mainmenu from '../components/Main_menu.vue';
import History from '../components/History.vue';
import Signup from '../components/Signup.vue';
Vue.use(Router)

// Define path
export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'login',
      component: Login,
      props: true,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      props: true,
    },
    {
      path: '/main_menu',
      name: 'main_menu',
      component: Mainmenu,
      props: true,
    },
    {
      path: '/history',
      name: 'history',
      component: History,
      props: true,
    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup,
    },
  ],
});



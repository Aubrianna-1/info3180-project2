import { createRouter, createWebHistory } from 'vue-router'
//views
import HomeView from '../views/HomeView.vue'
import ExploreView from '../views/ExploreView.vue'
//import Profile from '../views/Profile.vue'
import User from '../views/User'

//components
//import RegistrationFormView from '../views/RegistrationFormView.vue'
import RegistrationForm from '../components/RegistrationForm.vue'
//import LoginFormView from '../views/LoginFormView.vue'
import LoginForm from '../components/LoginForm.vue'
//import NewPostFormView from '../views/NewPostFormtView.vue'
import NewPostForm from '../components/NewPostForm.vue'


const token = localStorage.getItem("token")
// console.log(token)

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },

    //Added for Login, Logout, Register, explore page, posts, users
    {
      path: "/register",
      name: "register",
      component: RegistrationForm,
      //component: () => import("../views/RegistrationFormView.vue"),
      meta: {auth: false}
    },
    {
      path: "/login",
      name: "login",
      component: LoginForm,
      //component: () => import("../views/LoginView.vue"),
      meta: {auth: false}
    },
    {
      path: "/logout",
      name: "logout",
      component: LoginForm,
      //component: () => import("../views/LogoutView.vue"),
    },
    {
      path: "/explore",
      name: "explore",
      component: ExploreView,
      //component: () => import("../views/ExploreView.vue"),
      meta: {auth: true}
    },
    {
      path: "/users/:user_id",
      name: "users",
      component: User,
      //component: () => import("../views/User.vue"),
      meta: {auth: true}
    },
    {
      path: "/posts/new",
      name: "newpost",
      component: NewPostForm,
      //component: () => import("../views/NewPostFormView.vue"),
      meta: {auth: true}
    },

  ]
})

export default router

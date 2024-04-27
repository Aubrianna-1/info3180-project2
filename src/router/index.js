import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
//import RegisterFormView from '../views/RegistrationFormView.vue'
//import LoginFormView from '../views/LoginFormView.vue'
//import LogoutView from '../views/LogoutView.vue'
//import ExploreView from '../views/ExploreView.vue'
//import NewPostView from '../views/NewPostView.vue'
//import ProfileView from '../views/ProfileView.vue'

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
      //component: RegistrationFormView
      component: () => import("../views/RegistrationFormView.vue"),
    },
    {
      path: "/login",
      name: "login",
      //component: LoginView
      component: () => import("../views/LoginView.vue"),
    },
    {
      path: "/logout",
      name: "logout",
      //LogoutView
      component: () => import("../views/LogoutView.vue"),
    },
    {
      path: "/explore",
      name: "explore",
      //component: ExploreView
      component: () => import("../views/ExploreView.vue"),
    },
    {
      path: "/users/:user_id",
      name: "users",
      //component: User
      component: () => import("../views/User.vue"),
    },
    {
      path: "/posts/new",
      name: "newpost",
      //component: NewPostFormView
      component: () => import("../views/NewPostFormView.vue"),
    },

  ]
})

export default router

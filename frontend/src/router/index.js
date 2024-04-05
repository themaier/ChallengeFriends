import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignInView from '../views/SignInView.vue'
import SignUpView from '../views/SignUpView.vue'
import CreateChallengeView from '../views/CreateChallengeView.vue'
import TrendingView from '../views/TrendingView.vue'
import FriendsView from '../views/FriendsView.vue'
import CompletedChallengesView from '../views/CompletedChallengesView.vue'
import FriendsProfileView from '../views/FriendsProfileView.vue'
import { useStore } from '../stores/store.js'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/anmelden',
      name: 'signIn',
      component: SignInView
    },
    {
      path: '/registrieren',
      name: 'signUp',
      component: SignUpView,
    },
    {
      path: '/erstellen',
      name: 'create', 
      component: CreateChallengeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/freunde',
      name: 'friends',
      component: FriendsView,
      meta: { requiresAuth: true }
    },
    {
      path: '/trends',
      name: 'trending',
      component: TrendingView,
      meta: { requiresAuth: true }
    },
    {
      path: '/abgeschlossen',
      name: 'completed',
      component: CompletedChallengesView,
      meta: { requiresAuth: true }
    },
    {
      path: '/user/:id',
      name: 'friendProfile',
      component: FriendsProfileView,
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const store = useStore()
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (store.loggedIn) {
      next()
    } else {
      next({ name: 'signIn' })
    }
  } else {
    next()
  }
})

export default router

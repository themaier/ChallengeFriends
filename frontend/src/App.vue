
<template>
  <div class="d-flex flex-column min-vh-100">
  <header>
      <nav class="navbar bg-dark navbar-expand-lg" data-bs-theme="dark">
        <div class="container-fluid">
          <RouterLink class="navbar-brand" to="#">Challenge accepted</RouterLink>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
              <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                <li class="nav-item">
                  <RouterLink class="nav-link" aria-current="page" :to="{ name: 'home' }">Meine Challenges</RouterLink>
                </li>
                <li class="nav-item">
                  <RouterLink class="nav-link" :to="{ name: 'trending' }">Trending</RouterLink>
                </li>
                <li class="nav-item">
                  <RouterLink class="nav-link" :to="{ name: 'create' }">Challenge erstellen</RouterLink>
                </li>
                <li class="nav-item">
                  <RouterLink class="nav-link" :to="{ name: 'completed' }">Vergangene Challenges</RouterLink>
                </li>
                <li class="nav-item">
                  <RouterLink class="nav-link" :to="{ name: 'friends' }">Freunde</RouterLink>
                </li>
                <li class="nav-item" v-if="!store.isLinked">
                  <RouterLink class="btn btn-primary ms-lg-2 mt-2 mt-lg-0" :to="{ name: 'login' }">Anmelden</RouterLink>
                </li>
                <li class="nav-item" v-if="store.isLinked">
                  <RouterLink :to="{ name: 'home' }">
                    <button @click="logout" class="btn btn-danger ms-lg-2 mt-2 mt-lg-0">Abmelden</button>
                  </RouterLink>
                </li>
              </ul>
            </div>
        </div>
      </nav>
  </header>

  <main class="flex-fill">
    <RouterView />
  </main>
  <footer class="mt-auto bg-light" v-if="!store.isLinked">
      <div class="text-center p-3" style="background-color: rgba(0, 0, 0, 0.1);">
        <router-link :to="{ name: 'login' }">Login</router-link> um Freunde zu sehen
      </div>
    </footer>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import {useStore} from './stores/store'

const store = useStore()

function logout () {
  store.isLinked = false
  // localStorage.removeItem('loggedIn')
  // localStorage.removeItem('user')
  store.user = null
}
</script>
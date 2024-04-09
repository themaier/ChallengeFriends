
<template>
  <div class="d-flex flex-column min-vh-100">
    <header>
      <nav class="navbar bg-dark navbar-expand-lg" data-bs-theme="dark">
        <div class="container-fluid">
          <RouterLink class="navbar-brand" to="#">Challenge accepted</RouterLink>
          <button class="navbar-toggler" @click="isCollapsed = !isCollapsed"><span class="navbar-toggler-icon"></span></button>
          <div class="navbar-collapse" :class="{'collapse': isCollapsed}" ref="navbarCollapse">
            <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
              <li class="nav-item">
                <RouterLink class="nav-link" @click="isCollapsed = !isCollapsed" aria-current="page" :to="{ name: 'home' }">Meine Challenges</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" @click="isCollapsed = !isCollapsed" :to="{ name: 'trending' }">Trending</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" @click="isCollapsed = !isCollapsed" :to="{ name: 'create' }">Challenge erstellen</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" @click="isCollapsed = !isCollapsed" :to="{ name: 'completed' }">Vergangene Challenges</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" @click="isCollapsed = !isCollapsed" :to="{ name: 'friends' }">Freunde</RouterLink>
              </li>
              <li class="nav-item" v-if="!store.isLinked">
                <RouterLink class="btn btn-primary ms-lg-2 mt-2 mt-lg-0" @click="isCollapsed = !isCollapsed" :to="{ name: 'login' }">Anmelden</RouterLink>
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
import { useStore } from './stores/store'
import { ref } from 'vue';

const store = useStore()

const isCollapsed = ref(true);

function logout () {
  store.isLinked = false
  store.user = null
}
</script>
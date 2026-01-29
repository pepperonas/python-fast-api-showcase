<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <nav v-if="authStore.isAuthenticated" class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <router-link to="/" class="flex items-center px-2 py-2 text-gray-700 hover:text-gray-900">
              Task Management
            </router-link>
            <router-link to="/projects" class="flex items-center px-4 py-2 text-gray-700 hover:text-gray-900">
              Projekte
            </router-link>
            <router-link to="/tasks" class="flex items-center px-4 py-2 text-gray-700 hover:text-gray-900">
              Aufgaben
            </router-link>
          </div>
          <div class="flex items-center">
            <span class="text-gray-700 mr-4">{{ authStore.user?.full_name }}</span>
            <button
              @click="handleLogout"
              class="px-4 py-2 text-sm text-white bg-red-600 rounded hover:bg-red-700"
            >
              Abmelden
            </button>
          </div>
        </div>
      </div>
    </nav>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/application/stores'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

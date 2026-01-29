<template>
  <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="px-4 py-6 sm:px-0">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-3xl font-bold text-gray-900">Projekte</h1>
        <button
          @click="showCreateModal = true"
          class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
        >
          Neues Projekt
        </button>
      </div>

      <div v-if="projectStore.loading" class="text-center py-8">Lädt Projekte...</div>
      <div v-else-if="projectStore.projects.length === 0" class="text-center py-8 text-gray-500">
        Keine Projekte vorhanden
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="project in projectStore.projects"
          :key="project.id"
          class="bg-white shadow rounded-lg p-6 hover:shadow-lg transition-shadow cursor-pointer"
          @click="$router.push(`/projects/${project.id}`)"
        >
          <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ project.name }}</h3>
          <p v-if="project.description" class="text-gray-600 mb-4">{{ project.description }}</p>
          <p class="text-sm text-gray-500">Erstellt: {{ new Date(project.created_at).toLocaleDateString('de-DE') }}</p>
        </div>
      </div>
    </div>

    <!-- Create Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <h3 class="text-lg font-bold text-gray-900 mb-4">Neues Projekt erstellen</h3>
        <form @submit.prevent="handleCreate">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
            <input
              v-model="projectForm.name"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Beschreibung</label>
            <textarea
              v-model="projectForm.description"
              class="w-full px-3 py-2 border border-gray-300 rounded-md"
              rows="3"
            />
          </div>
          <div class="flex justify-end space-x-2">
            <button
              type="button"
              @click="showCreateModal = false"
              class="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
            >
              Abbrechen
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
            >
              Erstellen
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useProjectStore } from '@/application/stores'

const projectStore = useProjectStore()
const showCreateModal = ref(false)

const projectForm = reactive({
  name: '',
  description: ''
})

onMounted(async () => {
  await projectStore.fetchProjects()
})

async function handleCreate() {
  try {
    await projectStore.createProject(projectForm.name, projectForm.description)
    showCreateModal.value = false
    projectForm.name = ''
    projectForm.description = ''
  } catch (error) {
    alert('Fehler beim Erstellen des Projekts')
  }
}
</script>

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
          class="bg-white shadow rounded-lg p-6 hover:shadow-lg transition-shadow"
        >
          <div @click="$router.push(`/projects/${project.id}`)" class="cursor-pointer">
            <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ project.name }}</h3>
            <p v-if="project.description" class="text-gray-600 mb-4">{{ project.description }}</p>
            <p class="text-sm text-gray-500">Erstellt: {{ new Date(project.created_at).toLocaleDateString('de-DE') }}</p>
          </div>
          <div class="mt-4 flex space-x-2">
            <button
              @click.stop="editProject(project)"
              class="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Bearbeiten
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal || editingProject" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <h3 class="text-lg font-bold text-gray-900 mb-4">
          {{ editingProject ? 'Projekt bearbeiten' : 'Neues Projekt erstellen' }}
        </h3>
        <form @submit.prevent="handleSubmit">
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
              @click="closeModal"
              class="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
            >
              Abbrechen
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
            >
              {{ editingProject ? 'Aktualisieren' : 'Erstellen' }}
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
import type { Project } from '@/domain/models'

const projectStore = useProjectStore()
const showCreateModal = ref(false)
const editingProject = ref<Project | null>(null)

const projectForm = reactive({
  name: '',
  description: ''
})

onMounted(async () => {
  await projectStore.fetchProjects()
})

function editProject(project: Project) {
  editingProject.value = project
  projectForm.name = project.name
  projectForm.description = project.description || ''
}

function closeModal() {
  showCreateModal.value = false
  editingProject.value = null
  projectForm.name = ''
  projectForm.description = ''
}

async function handleSubmit() {
  try {
    if (editingProject.value) {
      await projectStore.updateProject(editingProject.value.id, {
        name: projectForm.name,
        description: projectForm.description
      })
    } else {
      await projectStore.createProject(projectForm.name, projectForm.description)
    }
    closeModal()
    // Refresh projects list
    await projectStore.fetchProjects()
  } catch (error) {
    console.error('Error saving project:', error)
    alert(editingProject.value ? 'Fehler beim Aktualisieren des Projekts' : 'Fehler beim Erstellen des Projekts')
  }
}
</script>

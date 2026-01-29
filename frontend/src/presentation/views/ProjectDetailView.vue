<template>
  <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="px-4 py-6 sm:px-0">
      <div v-if="loading" class="text-center py-8">Lädt...</div>
      <div v-else-if="project">
        <h1 class="text-3xl font-bold text-gray-900 mb-6">{{ project.name }}</h1>
        <p v-if="project.description" class="text-gray-600 mb-6">{{ project.description }}</p>

        <div class="mb-6">
          <button
            @click="showCreateTaskModal = true"
            class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
          >
            Neue Aufgabe
          </button>
        </div>

        <div v-if="tasks.length === 0" class="text-center py-8 text-gray-500">
          Keine Aufgaben in diesem Projekt
        </div>
        <div v-else class="bg-white shadow rounded-lg overflow-hidden">
          <ul class="divide-y divide-gray-200">
            <li v-for="task in tasks" :key="task.id" class="p-4">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="text-lg font-medium text-gray-900">{{ task.title }}</h3>
                  <p v-if="task.description" class="text-sm text-gray-500 mt-1">{{ task.description }}</p>
                </div>
                <span class="px-2 py-1 text-xs font-semibold rounded-full"
                      :class="getStatusClass(task.status)">
                  {{ task.status }}
                </span>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Create Task Modal -->
    <div v-if="showCreateTaskModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <h3 class="text-lg font-bold text-gray-900 mb-4">Neue Aufgabe erstellen</h3>
        <form @submit.prevent="handleCreateTask">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Titel</label>
            <input
              v-model="taskForm.title"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Beschreibung</label>
            <textarea
              v-model="taskForm.description"
              class="w-full px-3 py-2 border border-gray-300 rounded-md"
              rows="3"
            />
          </div>
          <div class="flex justify-end space-x-2">
            <button
              type="button"
              @click="showCreateTaskModal = false"
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
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useTaskStore } from '@/application/stores'
import { projectApi, taskApi } from '@/infrastructure/api'
import type { Project, Task } from '@/domain/models'

const route = useRoute()
const taskStore = useTaskStore()

const project = ref<Project | null>(null)
const tasks = ref<Task[]>([])
const loading = ref(true)
const showCreateTaskModal = ref(false)

const taskForm = reactive({
  title: '',
  description: ''
})

const projectId = computed(() => route.params.id as string)

onMounted(async () => {
  await loadProject()
  await loadTasks()
})

async function loadProject() {
  try {
    project.value = await projectApi.getProject(projectId.value)
  } catch (error) {
    console.error('Failed to load project', error)
  }
}

async function loadTasks() {
  try {
    tasks.value = await taskApi.getTasksByProject(projectId.value)
  } catch (error) {
    console.error('Failed to load tasks', error)
  } finally {
    loading.value = false
  }
}

async function handleCreateTask() {
  try {
    const newTask = await taskStore.createTask(
      taskForm.title,
      taskForm.description,
      projectId.value
    )
    tasks.value.push(newTask)
    showCreateTaskModal.value = false
    taskForm.title = ''
    taskForm.description = ''
  } catch (error) {
    alert('Fehler beim Erstellen der Aufgabe')
  }
}

function getStatusClass(status: string) {
  const classes: Record<string, string> = {
    todo: 'bg-gray-100 text-gray-800',
    in_progress: 'bg-yellow-100 text-yellow-800',
    done: 'bg-green-100 text-green-800',
    cancelled: 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}
</script>

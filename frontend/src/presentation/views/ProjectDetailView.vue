<template>
  <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="px-4 py-6 sm:px-0">
      <div v-if="loading" class="text-center py-8">Lädt...</div>
      <div v-else-if="project">
        <h1 class="text-3xl font-bold text-gray-900 mb-6">{{ project.name }}</h1>
        <p v-if="project.description" class="text-gray-600 mb-6">{{ project.description }}</p>

        <div class="mb-6 flex space-x-2">
          <button
            @click="showCreateTaskModal = true"
            class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
          >
            Neue Aufgabe
          </button>
          <button
            @click="showLinkTaskModal = true"
            class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
          >
            Aufgabe verlinken
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

    <!-- Link Task Modal -->
    <div v-if="showLinkTaskModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click.self="showLinkTaskModal = false">
      <div class="relative top-20 mx-auto p-6 border w-full max-w-md shadow-xl rounded-lg bg-white">
        <h3 class="text-xl font-bold text-gray-900 mb-4">Aufgabe verlinken</h3>
        <form @submit.prevent="handleLinkTask">
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-3">Aufgabe auswählen</label>
            <div v-if="allTasks.length === 0" class="text-sm text-gray-500 py-8 text-center border-2 border-dashed border-gray-300 rounded-lg bg-gray-50">
              <p>Keine verfügbaren Aufgaben zum Verlinken</p>
            </div>
            <div v-else class="max-h-64 overflow-y-auto border border-gray-200 rounded-lg">
              <div
                v-for="task in allTasks"
                :key="task.id"
                @click="linkTaskForm.taskId = task.id"
                class="px-4 py-3 border-b border-gray-100 hover:bg-indigo-50 cursor-pointer transition-colors"
                :class="{ 'bg-indigo-100 border-indigo-300': linkTaskForm.taskId === task.id }"
              >
                <div class="flex items-start">
                  <input
                    type="radio"
                    :value="task.id"
                    v-model="linkTaskForm.taskId"
                    class="mt-1 mr-3 text-indigo-600 focus:ring-indigo-500"
                  />
                  <div class="flex-1">
                    <div class="font-medium text-gray-900">{{ task.title }}</div>
                    <div v-if="task.description" class="text-sm text-gray-600 mt-1">
                      {{ task.description }}
                    </div>
                    <div class="flex items-center gap-3 mt-2">
                      <span class="text-xs px-2 py-1 rounded-full"
                            :class="{
                              'bg-gray-100 text-gray-700': task.status === 'todo',
                              'bg-yellow-100 text-yellow-700': task.status === 'in_progress',
                              'bg-green-100 text-green-700': task.status === 'done',
                              'bg-red-100 text-red-700': task.status === 'cancelled'
                            }">
                        {{ task.status }}
                      </span>
                      <span class="text-xs px-2 py-1 rounded-full bg-blue-100 text-blue-700">
                        {{ task.priority }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200">
            <button
              type="button"
              @click="showLinkTaskModal = false"
              class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors font-medium"
            >
              Abbrechen
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:bg-gray-300 disabled:text-gray-500 disabled:cursor-not-allowed transition-colors font-medium"
              :disabled="allTasks.length === 0 || !linkTaskForm.taskId"
            >
              Verlinken
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
const allTasks = ref<Task[]>([])
const loading = ref(true)
const showCreateTaskModal = ref(false)
const showLinkTaskModal = ref(false)

const taskForm = reactive({
  title: '',
  description: ''
})

const linkTaskForm = reactive({
  taskId: ''
})

const projectId = computed(() => route.params.id as string)

onMounted(async () => {
  await loadProject()
  await loadTasks()
  await loadAllTasks()
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

async function loadAllTasks() {
  try {
    allTasks.value = await taskApi.getAllTasks()
    // Filter out tasks that are already linked to this project or another project
    allTasks.value = allTasks.value.filter(task => !task.project_id || task.project_id === projectId.value)
  } catch (error) {
    console.error('Failed to load all tasks', error)
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
    await loadAllTasks()
  } catch (error) {
    alert('Fehler beim Erstellen der Aufgabe')
  }
}

async function handleLinkTask() {
  try {
    if (!linkTaskForm.taskId) {
      alert('Bitte wählen Sie eine Aufgabe aus')
      return
    }
    await taskStore.updateTask(linkTaskForm.taskId, {
      project_id: projectId.value
    })
    await loadTasks()
    await loadAllTasks()
    showLinkTaskModal.value = false
    linkTaskForm.taskId = ''
  } catch (error) {
    alert('Fehler beim Verlinken der Aufgabe')
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

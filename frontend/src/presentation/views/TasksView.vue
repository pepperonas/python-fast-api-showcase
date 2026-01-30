<template>
  <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="px-4 py-6 sm:px-0">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-3xl font-bold text-gray-900">Aufgaben</h1>
        <button
          @click="showCreateModal = true"
          class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
        >
          Neue Aufgabe
        </button>
      </div>

      <div v-if="taskStore.loading" class="text-center py-8">Lädt Aufgaben...</div>
      <div v-else-if="taskStore.tasks.length === 0" class="text-center py-8 text-gray-500">
        Keine Aufgaben vorhanden
      </div>
      <div v-else class="bg-white shadow rounded-lg overflow-hidden">
        <ul class="divide-y divide-gray-200">
          <li v-for="task in taskStore.tasks" :key="task.id" class="p-4 hover:bg-gray-50">
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <h3 class="text-lg font-medium text-gray-900">{{ task.title }}</h3>
                <p v-if="task.description" class="text-sm text-gray-500 mt-1">{{ task.description }}</p>
                <div class="mt-2 flex space-x-4">
                  <span class="text-xs text-gray-500">Status: {{ task.status }}</span>
                  <span class="text-xs text-gray-500">Priorität: {{ task.priority }}</span>
                </div>
              </div>
              <div class="flex space-x-2">
                <button
                  @click="editTask(task)"
                  class="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                  Bearbeiten
                </button>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal || editingTask" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <h3 class="text-lg font-bold text-gray-900 mb-4">
          {{ editingTask ? 'Aufgabe bearbeiten' : 'Neue Aufgabe erstellen' }}
        </h3>
        <form @submit.prevent="handleSubmit">
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
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Priorität</label>
            <select v-model="taskForm.priority" class="w-full px-3 py-2 border border-gray-300 rounded-md">
              <option value="low">Niedrig</option>
              <option value="medium">Mittel</option>
              <option value="high">Hoch</option>
              <option value="urgent">Dringend</option>
            </select>
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
              {{ editingTask ? 'Aktualisieren' : 'Erstellen' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useTaskStore } from '@/application/stores'
import type { Task } from '@/domain/models'

const taskStore = useTaskStore()
const showCreateModal = ref(false)
const editingTask = ref<Task | null>(null)

const taskForm = reactive({
  title: '',
  description: '',
  priority: 'medium'
})

onMounted(async () => {
  await taskStore.fetchTasks()
})

function editTask(task: Task) {
  editingTask.value = task
  taskForm.title = task.title
  taskForm.description = task.description || ''
  taskForm.priority = task.priority
}

function closeModal() {
  showCreateModal.value = false
  editingTask.value = null
  taskForm.title = ''
  taskForm.description = ''
  taskForm.priority = 'medium'
}

async function handleSubmit() {
  try {
    if (editingTask.value) {
      await taskStore.updateTask(editingTask.value.id, {
        title: taskForm.title,
        description: taskForm.description,
        priority: taskForm.priority
      })
    } else {
      await taskStore.createTask(
        taskForm.title,
        taskForm.description,
        undefined,
        taskForm.priority
      )
    }
    closeModal()
    // Refresh tasks list
    await taskStore.fetchTasks()
  } catch (error: any) {
    console.error('Error saving task:', error)
    const errorMessage = error?.response?.data?.detail || error?.message || 'Fehler beim Speichern der Aufgabe'
    alert(errorMessage)
  }
}
</script>

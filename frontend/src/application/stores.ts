/** Pinia stores for state management */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Task, Project, User, Notification } from '@/domain/models'
import {
  GetTasksUseCase,
  CreateTaskUseCase,
  UpdateTaskUseCase,
  GetProjectsUseCase,
  CreateProjectUseCase,
  RegisterUserUseCase,
  LoginUseCase,
  GetNotificationsUseCase
} from './useCases'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const isAuthenticated = computed(() => !!token.value && !!user.value)

  const loginUseCase = new LoginUseCase()
  const registerUseCase = new RegisterUserUseCase()

  async function login(email: string, password: string) {
    const response = await loginUseCase.execute(email, password)
    token.value = response.access_token
    user.value = response.user
    localStorage.setItem('token', response.access_token)
    return response
  }

  async function register(email: string, fullName: string, password: string) {
    const newUser = await registerUseCase.execute(email, fullName, password)
    // After registration, automatically log in
    return await login(email, password)
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    register,
    logout
  }
})

export const useTaskStore = defineStore('tasks', () => {
  const tasks = ref<Task[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const getTasksUseCase = new GetTasksUseCase()
  const createTaskUseCase = new CreateTaskUseCase()
  const updateTaskUseCase = new UpdateTaskUseCase()

  async function fetchTasks(projectId?: string) {
    loading.value = true
    error.value = null
    try {
      tasks.value = await getTasksUseCase.execute(projectId)
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch tasks'
    } finally {
      loading.value = false
    }
  }

  async function createTask(
    title: string,
    description?: string,
    projectId?: string,
    priority?: string
  ) {
    loading.value = true
    error.value = null
    try {
      const newTask = await createTaskUseCase.execute(title, description, projectId, priority)
      tasks.value.push(newTask)
      return newTask
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to create task'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateTask(taskId: string, updates: Partial<Task>) {
    loading.value = true
    error.value = null
    try {
      const updatedTask = await updateTaskUseCase.execute(taskId, updates)
      const index = tasks.value.findIndex(t => t.id === taskId)
      if (index !== -1) {
        tasks.value[index] = updatedTask
      }
      return updatedTask
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to update task'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask
  }
})

export const useProjectStore = defineStore('projects', () => {
  const projects = ref<Project[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const getProjectsUseCase = new GetProjectsUseCase()
  const createProjectUseCase = new CreateProjectUseCase()

  async function fetchProjects() {
    loading.value = true
    error.value = null
    try {
      projects.value = await getProjectsUseCase.execute()
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch projects'
    } finally {
      loading.value = false
    }
  }

  async function createProject(name: string, description?: string) {
    loading.value = true
    error.value = null
    try {
      const newProject = await createProjectUseCase.execute(name, description)
      projects.value.push(newProject)
      return newProject
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to create project'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    projects,
    loading,
    error,
    fetchProjects,
    createProject
  }
})

export const useNotificationStore = defineStore('notifications', () => {
  const notifications = ref<Notification[]>([])
  const loading = ref(false)
  const unreadCount = computed(() => notifications.value.filter(n => !n.read).length)

  const getNotificationsUseCase = new GetNotificationsUseCase()

  async function fetchNotifications(unreadOnly: boolean = false) {
    loading.value = true
    try {
      notifications.value = await getNotificationsUseCase.execute(unreadOnly)
    } catch (e) {
      console.error('Failed to fetch notifications', e)
    } finally {
      loading.value = false
    }
  }

  return {
    notifications,
    loading,
    unreadCount,
    fetchNotifications
  }
})

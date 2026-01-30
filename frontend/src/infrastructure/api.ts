/** API client for backend services */

import axios, { type AxiosInstance } from 'axios'
import type { Task, Project, User, Notification } from '@/domain/models'

// API base URLs for different services
// Use relative URLs when running in browser (via Nginx proxy), absolute URLs for development
const USER_SERVICE_URL = import.meta.env.VITE_USER_SERVICE_URL || ''
const TASK_SERVICE_URL = import.meta.env.VITE_TASK_SERVICE_URL || ''
const NOTIFICATION_SERVICE_URL = import.meta.env.VITE_NOTIFICATION_SERVICE_URL || ''

// Create axios instances with interceptors
function createApiClient(baseURL: string): AxiosInstance {
  const client: AxiosInstance = axios.create({
    baseURL,
    headers: {
      'Content-Type': 'application/json'
    }
  })

  // Request interceptor to add auth token
  client.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    },
    (error) => {
      return Promise.reject(error)
    }
  )

  // Response interceptor for error handling
  client.interceptors.response.use(
    (response) => response,
    (error) => {
      // Only redirect to login for 401 errors, but ignore during grace period after login
      // and ignore errors from browser extensions (like /api/v1/credentials)
      if (error.response?.status === 401) {
        const url = error.config?.url || ''
        // Ignore credentials endpoint (used by browser extensions)
        if (url.includes('/credentials')) {
          return Promise.reject(error)
        }
        // Check if we're in a grace period (just logged in)
        const loginTime = sessionStorage.getItem('loginTime')
        if (loginTime) {
          const timeSinceLogin = Date.now() - parseInt(loginTime)
          // Grace period: 5 seconds after login
          if (timeSinceLogin < 5000) {
            console.warn('401 error during grace period after login, ignoring logout:', url)
            return Promise.reject(error)
          }
        }
        localStorage.removeItem('token')
        sessionStorage.removeItem('loginTime')
        window.location.href = '/login'
      }
      return Promise.reject(error)
    }
  )

  return client
}

const userApiClient = createApiClient(USER_SERVICE_URL)
const taskApiClient = createApiClient(TASK_SERVICE_URL)
const notificationApiClient = createApiClient(NOTIFICATION_SERVICE_URL)

// Task API
export const taskApi = {
  async getAllTasks(): Promise<Task[]> {
    const response = await taskApiClient.get('/api/v1/tasks')
    return response.data
  },

  async getTask(taskId: string): Promise<Task> {
    const response = await taskApiClient.get(`/api/v1/tasks/${taskId}`)
    return response.data
  },

  async createTask(data: {
    title: string
    description?: string
    project_id?: string
    priority?: string
  }): Promise<Task> {
    const response = await taskApiClient.post('/api/v1/tasks', data)
    return response.data
  },

  async updateTask(taskId: string, updates: Partial<Task>): Promise<Task> {
    const response = await taskApiClient.put(`/api/v1/tasks/${taskId}`, updates)
    return response.data
  },

  async getTasksByProject(projectId: string): Promise<Task[]> {
    const response = await taskApiClient.get(`/api/v1/projects/${projectId}/tasks`)
    return response.data
  }
}

// Project API
export const projectApi = {
  async getAllProjects(): Promise<Project[]> {
    const response = await taskApiClient.get('/api/v1/projects')
    return response.data
  },

  async getProject(projectId: string): Promise<Project> {
    const response = await taskApiClient.get(`/api/v1/projects/${projectId}`)
    return response.data
  },

  async createProject(data: { name: string; description?: string }): Promise<Project> {
    const response = await taskApiClient.post('/api/v1/projects', data)
    return response.data
  },

  async updateProject(projectId: string, data: { name?: string; description?: string }): Promise<Project> {
    const response = await taskApiClient.put(`/api/v1/projects/${projectId}`, data)
    return response.data
  }
}

// User API
export const userApi = {
  async register(data: { email: string; full_name: string; password: string }): Promise<User> {
    const response = await userApiClient.post('/api/v1/auth/register', data)
    return response.data
  },

  async login(data: { email: string; password: string }): Promise<{ access_token: string; user: User }> {
    const response = await userApiClient.post('/api/v1/auth/login', data)
    return response.data
  },

  async getCurrentUser(): Promise<User> {
    const response = await userApiClient.get('/api/v1/users/me')
    return response.data
  }
}

// Notification API
export const notificationApi = {
  async getNotifications(unreadOnly: boolean = false): Promise<Notification[]> {
    const response = await notificationApiClient.get('/api/v1/notifications', {
      params: { unread_only: unreadOnly }
    })
    return response.data
  },

  async markAsRead(notificationId: string): Promise<Notification> {
    const response = await notificationApiClient.post(`/api/v1/notifications/${notificationId}/read`)
    return response.data
  }
}

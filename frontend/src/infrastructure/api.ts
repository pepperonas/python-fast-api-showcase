/** API client for backend services */

import axios, { type AxiosInstance } from 'axios'
import type { Task, Project, User, Notification } from '@/domain/models'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Create axios instance with interceptors
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add auth token
apiClient.interceptors.request.use(
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
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Task API
export const taskApi = {
  async getAllTasks(): Promise<Task[]> {
    const response = await apiClient.get('/api/v1/tasks')
    return response.data
  },

  async getTask(taskId: string): Promise<Task> {
    const response = await apiClient.get(`/api/v1/tasks/${taskId}`)
    return response.data
  },

  async createTask(data: {
    title: string
    description?: string
    project_id?: string
    priority?: string
  }): Promise<Task> {
    const response = await apiClient.post('/api/v1/tasks', data)
    return response.data
  },

  async updateTask(taskId: string, updates: Partial<Task>): Promise<Task> {
    const response = await apiClient.put(`/api/v1/tasks/${taskId}`, updates)
    return response.data
  },

  async getTasksByProject(projectId: string): Promise<Task[]> {
    const response = await apiClient.get(`/api/v1/projects/${projectId}/tasks`)
    return response.data
  }
}

// Project API
export const projectApi = {
  async getAllProjects(): Promise<Project[]> {
    const response = await apiClient.get('/api/v1/projects')
    return response.data
  },

  async getProject(projectId: string): Promise<Project> {
    const response = await apiClient.get(`/api/v1/projects/${projectId}`)
    return response.data
  },

  async createProject(data: { name: string; description?: string }): Promise<Project> {
    const response = await apiClient.post('/api/v1/projects', data)
    return response.data
  }
}

// User API
export const userApi = {
  async register(data: { email: string; full_name: string; password: string }): Promise<User> {
    const response = await apiClient.post('/api/v1/auth/register', data)
    return response.data
  },

  async login(data: { email: string; password: string }): Promise<{ access_token: string; user: User }> {
    const response = await apiClient.post('/api/v1/auth/login', data)
    return response.data
  },

  async getCurrentUser(): Promise<User> {
    const response = await apiClient.get('/api/v1/users/me')
    return response.data
  }
}

// Notification API
export const notificationApi = {
  async getNotifications(unreadOnly: boolean = false): Promise<Notification[]> {
    const response = await apiClient.get('/api/v1/notifications', {
      params: { unread_only: unreadOnly }
    })
    return response.data
  },

  async markAsRead(notificationId: string): Promise<Notification> {
    const response = await apiClient.post(`/api/v1/notifications/${notificationId}/read`)
    return response.data
  }
}

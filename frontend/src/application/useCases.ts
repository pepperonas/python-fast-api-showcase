/** Use cases for Task Management */

import type { Task, Project, User, Notification } from '@/domain/models'
import { taskApi, projectApi, userApi, notificationApi } from '@/infrastructure/api'

export class GetTasksUseCase {
  async execute(projectId?: string): Promise<Task[]> {
    if (projectId) {
      return await taskApi.getTasksByProject(projectId)
    }
    return await taskApi.getAllTasks()
  }
}

export class CreateTaskUseCase {
  async execute(
    title: string,
    description?: string,
    projectId?: string,
    priority?: string
  ): Promise<Task> {
    return await taskApi.createTask({
      title,
      description,
      project_id: projectId,
      priority: priority || 'medium'
    })
  }
}

export class UpdateTaskUseCase {
  async execute(
    taskId: string,
    updates: Partial<Task>
  ): Promise<Task> {
    return await taskApi.updateTask(taskId, updates)
  }
}

export class GetProjectsUseCase {
  async execute(): Promise<Project[]> {
    return await projectApi.getAllProjects()
  }
}

export class CreateProjectUseCase {
  async execute(name: string, description?: string): Promise<Project> {
    return await projectApi.createProject({ name, description })
  }
}

export class RegisterUserUseCase {
  async execute(email: string, fullName: string, password: string): Promise<User> {
    return await userApi.register({ email, full_name: fullName, password })
  }
}

export class LoginUseCase {
  async execute(email: string, password: string): Promise<{ access_token: string; user: User }> {
    return await userApi.login({ email, password })
  }
}

export class GetNotificationsUseCase {
  async execute(unreadOnly: boolean = false): Promise<Notification[]> {
    return await notificationApi.getNotifications(unreadOnly)
  }
}

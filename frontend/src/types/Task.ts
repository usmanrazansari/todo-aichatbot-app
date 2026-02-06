/**
 * Task type definition for the Todo application
 */

export interface Task {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}

export interface TaskCreateData {
  title: string;
  description?: string;
  completed?: boolean;
}

export interface TaskUpdateData {
  title?: string;
  description?: string;
  completed?: boolean;
}
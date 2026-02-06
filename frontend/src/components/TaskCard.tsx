/**
 * TaskCard component to display individual tasks
 */

import React from 'react';
import { Task } from '../types/Task';
import { apiClient } from '../services/api';
import { getUserIdFromToken } from '../services/auth';

interface TaskCardProps {
  task: Task;
  onTaskUpdate: () => void;
  onTaskDelete: () => void;
}

const TaskCard: React.FC<TaskCardProps> = ({ task, onTaskUpdate, onTaskDelete }) => {
  const userId = getUserIdFromToken();

  const handleToggleComplete = async () => {
    try {
      if (!userId) {
        throw new Error('User not authenticated');
      }
      await apiClient.patch(`/api/${userId}/tasks/${task.id}/complete`);
      onTaskUpdate(); // Refresh the task list
    } catch (error) {
      console.error('Error toggling task completion:', error);
      alert('Failed to update task completion status');
    }
  };

  const handleDelete = async () => {
    if (window.confirm(`Are you sure you want to delete "${task.title}"?`)) {
      try {
        if (!userId) {
          throw new Error('User not authenticated');
        }
        await apiClient.delete(`/api/${userId}/tasks/${task.id}`);
        onTaskDelete(); // Refresh the task list
      } catch (error) {
        console.error('Error deleting task:', error);
        alert('Failed to delete task');
      }
    }
  };

  return (
    <div className={`border rounded-lg p-4 mb-3 shadow-sm ${task.completed ? 'bg-green-50' : 'bg-white'}`}>
      <div className="flex justify-between items-start">
        <div>
          <h3 className={`text-lg font-semibold ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
            {task.title}
          </h3>
          {task.description && (
            <p className={`mt-1 ${task.completed ? 'line-through text-gray-500' : 'text-gray-600'}`}>
              {task.description}
            </p>
          )}
          <p className="text-xs text-gray-400 mt-2">
            Created: {new Date(task.created_at).toLocaleString()}
          </p>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={handleToggleComplete}
            className={`px-3 py-1 rounded text-sm ${
              task.completed
                ? 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200'
                : 'bg-blue-100 text-blue-800 hover:bg-blue-200'
            }`}
          >
            {task.completed ? 'Undo' : 'Complete'}
          </button>
          <button
            onClick={handleDelete}
            className="px-3 py-1 bg-red-100 text-red-800 rounded text-sm hover:bg-red-200"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
};

export default TaskCard;
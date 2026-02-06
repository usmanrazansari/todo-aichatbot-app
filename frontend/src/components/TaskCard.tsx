/**
 * TaskCard component to display individual tasks
 */

import React, { useState } from 'react';
import { Task } from '../types/Task';
import { apiClient } from '../services/api';
import { getUserIdFromToken } from '../services/auth';

interface TaskCardProps {
  task: Task;
  onTaskUpdate: () => void;
  onTaskDelete: () => void;
  onEdit?: (task: Task) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({ task, onTaskUpdate, onTaskDelete, onEdit }) => {
  const userId = getUserIdFromToken();
  const [isDeleting, setIsDeleting] = useState(false);
  const [isToggling, setIsToggling] = useState(false);

  const handleToggleComplete = async () => {
    try {
      if (!userId) {
        throw new Error('User not authenticated');
      }
      setIsToggling(true);
      await apiClient.patch(`/api/${userId}/tasks/${task.id}/complete`);
      onTaskUpdate();
    } catch (error) {
      console.error('Error toggling task completion:', error);
      alert('Failed to update task completion status');
    } finally {
      setIsToggling(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm(`Are you sure you want to delete "${task.title}"?`)) {
      try {
        if (!userId) {
          throw new Error('User not authenticated');
        }
        setIsDeleting(true);
        await apiClient.delete(`/api/${userId}/tasks/${task.id}`);
        onTaskDelete();
      } catch (error) {
        console.error('Error deleting task:', error);
        alert('Failed to delete task');
        setIsDeleting(false);
      }
    }
  };

  return (
    <div className={`border rounded-lg p-5 mb-4 shadow-md transition-all duration-200 hover:shadow-lg ${
      task.completed ? 'bg-gradient-to-r from-green-50 to-emerald-50 border-green-200' : 'bg-white border-gray-200'
    }`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <button
              onClick={handleToggleComplete}
              disabled={isToggling}
              className={`flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all ${
                task.completed
                  ? 'bg-green-500 border-green-500'
                  : 'border-gray-300 hover:border-indigo-500'
              } ${isToggling ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
            >
              {task.completed && (
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                </svg>
              )}
            </button>
            <h3 className={`text-lg font-semibold ${
              task.completed ? 'line-through text-gray-500' : 'text-gray-900'
            }`}>
              {task.title}
            </h3>
          </div>

          {task.description && (
            <p className={`ml-9 text-sm ${
              task.completed ? 'line-through text-gray-400' : 'text-gray-600'
            }`}>
              {task.description}
            </p>
          )}

          <div className="ml-9 mt-3 flex items-center gap-4 text-xs text-gray-400">
            <span className="flex items-center gap-1">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {new Date(task.created_at).toLocaleDateString()}
            </span>
            {task.completed && (
              <span className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">
                Completed
              </span>
            )}
          </div>
        </div>

        <div className="flex gap-2 ml-4">
          {onEdit && (
            <button
              onClick={() => onEdit(task)}
              className="p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
              title="Edit task"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </button>
          )}

          <button
            onClick={handleDelete}
            disabled={isDeleting}
            className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-50"
            title="Delete task"
          >
            {isDeleting ? (
              <svg className="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            ) : (
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default TaskCard;
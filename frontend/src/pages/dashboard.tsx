/**
 * Dashboard page to display user's tasks
 */

import React, { useState, useEffect } from 'react';
import { Task } from '../types/Task';
import TaskCard from '../components/TaskCard';
import TaskForm from '../components/TaskForm';
import { apiClient } from '../services/api';
import { getUserIdFromToken } from '../services/auth';

const DashboardPage: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [showForm, setShowForm] = useState<boolean>(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [error, setError] = useState<string | null>(null);

  const userId = getUserIdFromToken();

  useEffect(() => {
    if (userId) {
      fetchTasks();
    }
  }, [userId]);

  const fetchTasks = async () => {
    if (!userId) {
      setError('User not authenticated');
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      const response = await apiClient.get(`/api/${userId}/tasks`);
      setTasks(response.data);
      setError(null);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      setError('Failed to load tasks. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleTaskSubmit = () => {
    setEditingTask(null);
    setShowForm(false);
    fetchTasks(); // Refresh the task list
  };

  const handleTaskDelete = () => {
    fetchTasks(); // Refresh the task list
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setShowForm(true);
  };

  if (!userId) {
    return (
      <div className="container mx-auto p-4">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
          <strong className="font-bold">Authentication Error! </strong>
          <span className="block sm:inline">Please log in to access your tasks.</span>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">My Tasks</h1>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
          <span className="block sm:inline">{error}</span>
        </div>
      )}

      <div className="mb-6">
        <button
          onClick={() => {
            setEditingTask(null);
            setShowForm(!showForm);
          }}
          className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          {showForm ? 'Cancel' : 'Create New Task'}
        </button>
      </div>

      {showForm && (
        <TaskForm
          task={editingTask || undefined}
          onSubmit={handleTaskSubmit}
          onCancel={() => {
            setEditingTask(null);
            setShowForm(false);
          }}
        />
      )}

      {loading ? (
        <div className="text-center py-10">
          <p>Loading tasks...</p>
        </div>
      ) : (
        <div>
          {tasks.length === 0 ? (
            <div className="text-center py-10">
              <p className="text-gray-500">No tasks yet. Create your first task!</p>
            </div>
          ) : (
            <div>
              <h2 className="text-xl font-semibold mb-4">
                {tasks.filter(t => !t.completed).length} pending, {tasks.filter(t => t.completed).length} completed
              </h2>
              <div>
                {tasks.map((task) => (
                  <TaskCard
                    key={task.id}
                    task={task}
                    onTaskUpdate={fetchTasks}
                    onTaskDelete={handleTaskDelete}
                  />
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default DashboardPage;
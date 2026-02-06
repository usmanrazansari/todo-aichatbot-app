/**
 * Home page for the Todo application
 */

import React from 'react';
import { isAuthenticated } from '../services/auth';

const HomePage: React.FC = () => {
  // Redirect to dashboard if user is authenticated
  if (isAuthenticated()) {
    typeof window !== 'undefined' && (window.location.href = '/dashboard');
    return null; // Render nothing while redirecting
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Welcome to Todo App
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Manage your tasks efficiently and securely
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <div className="space-y-6">
            <div>
              <p className="text-gray-600">
                This is a secure todo application where you can manage your personal tasks.
              </p>
              <p className="mt-4 text-gray-600">
                To get started, please sign in to your account or create a new one.
              </p>
            </div>

            <div className="flex flex-col space-y-4">
              <a
                href="/login"
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Sign In
              </a>

              <a
                href="/register"
                className="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Create Account
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
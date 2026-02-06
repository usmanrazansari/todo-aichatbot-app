/**
 * Home page for the Todo application
 */

import React, { useEffect, useState } from 'react';
import { isAuthenticated } from '../services/auth';

const HomePage: React.FC = () => {
  const [isAuth, setIsAuth] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check authentication on client side only
    if (typeof window !== 'undefined') {
      const authenticated = isAuthenticated();
      setIsAuth(authenticated);
      setIsLoading(false);

      if (authenticated) {
        window.location.href = '/dashboard';
      }
    }
  }, []);

  if (isLoading) {
    return null; // Or a loading spinner
  }

  if (isAuth) {
    return null; // Redirecting
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-100 via-purple-50 to-pink-100">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto">
          <div className="relative z-10 pb-8 sm:pb-16 md:pb-20 lg:pb-28 xl:pb-32">
            <main className="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
              <div className="text-center">
                <div className="mb-8">
                  <span className="text-8xl">📝</span>
                </div>
                <h1 className="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
                  <span className="block">Welcome to</span>
                  <span className="block text-indigo-600">Todo App</span>
                </h1>
                <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
                  Manage your tasks efficiently and securely. Stay organized, boost productivity, and never miss a deadline.
                </p>

                {/* Features */}
                <div className="mt-10 max-w-4xl mx-auto grid grid-cols-1 gap-6 sm:grid-cols-3">
                  <div className="bg-white rounded-lg shadow-md p-6 transform hover:scale-105 transition-transform duration-200">
                    <div className="text-3xl mb-3">✅</div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Easy Task Management</h3>
                    <p className="text-sm text-gray-600">Create, update, and organize your tasks with a simple, intuitive interface</p>
                  </div>

                  <div className="bg-white rounded-lg shadow-md p-6 transform hover:scale-105 transition-transform duration-200">
                    <div className="text-3xl mb-3">🔒</div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Secure & Private</h3>
                    <p className="text-sm text-gray-600">Your tasks are private and secure. Only you can access your data</p>
                  </div>

                  <div className="bg-white rounded-lg shadow-md p-6 transform hover:scale-105 transition-transform duration-200">
                    <div className="text-3xl mb-3">⚡</div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Fast & Responsive</h3>
                    <p className="text-sm text-gray-600">Lightning-fast performance with real-time updates across all devices</p>
                  </div>
                </div>

                {/* CTA Buttons */}
                <div className="mt-10 flex flex-col sm:flex-row gap-4 justify-center items-center">
                  <a
                    href="/register"
                    className="w-full sm:w-auto inline-flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 md:py-4 md:text-lg md:px-10 shadow-lg transform hover:scale-105 transition-all duration-200"
                  >
                    Get Started Free
                    <svg className="ml-2 -mr-1 w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                  </a>

                  <a
                    href="/login"
                    className="w-full sm:w-auto inline-flex items-center justify-center px-8 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 md:py-4 md:text-lg md:px-10 shadow-md transform hover:scale-105 transition-all duration-200"
                  >
                    Sign In
                  </a>
                </div>

                {/* Demo Notice */}
                <div className="mt-8 inline-flex items-center px-4 py-2 bg-yellow-50 border border-yellow-200 rounded-full">
                  <svg className="w-5 h-5 text-yellow-600 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                  </svg>
                  <span className="text-sm text-yellow-800 font-medium">Demo Mode: Use any email to try the app</span>
                </div>
              </div>
            </main>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-20">
        <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
          <p className="text-center text-gray-500 text-sm">
            © 2026 Todo App. Built with Next.js and FastAPI.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
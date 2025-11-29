// frontend/src/main.jsx

import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import App from './App.jsx';
import './index.css'; // Your main CSS file (where Tailwind directives are located)

import HomePage from './pages/HomePage.jsx';
// Import the page components we created
import LoginPage from './pages/LoginPage.jsx';
import SignupPage from './pages/SignupPage.jsx';
// Placeholder Home Page Component
 

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      {/* The App component provides the layout (Navbar/Footer) */}
      <App>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          
          {/* Fallback 404 Route */}
          <Route path="*" element={<h1 className="text-4xl text-red-500 text-center py-10">404 - Page Not Found</h1>} />
        </Routes>
      </App>
    </BrowserRouter>
  </React.StrictMode>,
);
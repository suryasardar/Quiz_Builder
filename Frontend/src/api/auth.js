// frontend/src/api/auth.js
// Assuming this base URL matches your Flask server
const API_URL = 'http://127.0.0.1:5000/api/auth'; 

// --- Registration Function (Existing) ---
export async function register(username, email, password) {
  // ... (Your existing registration fetch logic) ...
  // Ensure the fetch call structure is correct to handle errors from Flask
  const response = await fetch(`${API_URL}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, email, password }),
  });
  
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.message || 'Registration failed.');
  }

  return data;
}

// --- Login Function (New) ---
export async function login(username, password) {
  const response = await fetch(`${API_URL}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password }),
  });
  
  const data = await response.json();

  if (!response.ok) {
    // Flask returns 401 Unauthorized for bad credentials
    throw new Error(data.message || 'Login failed: Invalid credentials.');
  }

  return data; // Returns { message: 'Login successful', username: '...' }
}

// You would also add an export for the logout function here
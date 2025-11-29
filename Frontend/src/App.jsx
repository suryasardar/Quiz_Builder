// frontend/src/App.jsx

import Navbar from './components/Navbar';
import Footer from './components/Footer';

// App is now the main layout container that accepts pages as 'children'
function App({ children }) {
  // Use Tailwind flex-col layout to ensure the footer is pushed to the bottom
  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <Navbar />
      
      {/* Main content area, grows to fill the remaining vertical space */}
      <main className="flex-grow container mx-auto p-4 sm:p-6 lg:p-8">
        {children}
      </main>
      
      <Footer />
    </div>
  );
}
export default App;
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="text-2xl font-bold text-indigo-600">
              QuizApp
            </Link>
          </div>
          <div className="flex items-center space-x-4">
            <Link 
              to="/signup" 
              className="px-3 py-2 rounded-md text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 transition duration-150"
            >
              Sign Up
            </Link>
            <Link 
              to="/login" 
              className="px-3 py-2 rounded-md text-sm font-medium text-indigo-600 border border-indigo-600 hover:bg-indigo-50 transition duration-150"
            >
              Log In
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
export default Navbar;
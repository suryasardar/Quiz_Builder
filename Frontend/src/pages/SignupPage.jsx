import React, { useState } from 'react';
// import { register } from '../api/auth'; // Import your API call
import { Link } from 'react-router-dom';

function SignupPage() {
    const [formData, setFormData] = useState({ username: '', email: '', password: '' });
    // ... rest of your state and handleChange/handleSubmit functions

    const handleSubmit = (e) => {
        e.preventDefault();
        // Here you would call your register API function
        console.log("Attempting to register:", formData);
    };

    return (
        <div className="flex justify-center items-center py-12">
            <div className="w-full max-w-md bg-white p-8 md:p-10 shadow-xl rounded-2xl border border-gray-100">
                <h2 className="text-4xl font-extrabold mb-2 text-center text-gray-900">
                    Create Account
                </h2>
                <p className="text-center text-gray-500 mb-8">
                    Start building your quizzes today!
                </p>

                <form onSubmit={handleSubmit} className="space-y-6">
                    {/* Username Input */}
                    <div>
                        <input
                            type="text"
                            name="username"
                            placeholder="Username"
                            className="w-full p-3 border border-gray-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500"
                            onChange={() => {}} // Use your actual handler
                            required
                        />
                    </div>
                    
                    {/* Email Input */}
                    <div>
                        <input
                            type="email"
                            name="email"
                            placeholder="Email Address"
                            className="w-full p-3 border border-gray-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500"
                            onChange={() => {}}
                            required
                        />
                    </div>

                    {/* Password Input */}
                    <div>
                        <input
                            type="password"
                            name="password"
                            placeholder="Password"
                            className="w-full p-3 border border-gray-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500"
                            onChange={() => {}}
                            required
                        />
                    </div>

                    {/* Submit Button */}
                    <button
                        type="submit"
                        className="w-full py-3 px-4 bg-indigo-600 text-white font-semibold rounded-xl hover:bg-indigo-700 transition duration-200 shadow-md"
                    >
                        Sign Up
                    </button>
                </form>

                <p className="mt-6 text-center text-sm text-gray-500">
                    Already have an account?{' '}
                    <Link to="/login" className="font-medium text-indigo-600 hover:text-indigo-500">
                        Log In
                    </Link>
                </p>
            </div>
        </div>
    );
}

export default SignupPage;
import React, { useState } from 'react';
import { dummyQuizData } from '../data/dummyQuizData'; // Import the dummy data
// import dummyQuizData from '../data/dummyQuizData.jsx';

function HomePage() {
    const [topicInput, setTopicInput] = useState('');
    const [quizData, setQuizData] = useState(null); // Will hold the 20 MCQs
    const [loading, setLoading] = useState(false);

    // Function to simulate the API call to the backend
    const generateQuiz = (e) => {
        e.preventDefault();
        if (!topicInput.trim()) return;

        setLoading(true);
        setQuizData(null); 
        
        // --- SIMULATE BACKEND API CALL ---
        // In a real app, this is where you'd use fetch/axios:
        // const response = await fetch('/api/generate-mcqs', { topic: topicInput });
        
        // Simulate a 1-2 second delay for the backend to "generate" the quiz
        setTimeout(() => {
            // Load the dummy data upon successful "generation"
            setQuizData(dummyQuizData);
            setLoading(false);
            // Scroll to the quiz section for a better UX
            document.getElementById('quiz-section')?.scrollIntoView({ behavior: 'smooth' });
        }, 1500);
    };
    
    // Function to calculate the required score for 10 marks
    const requiredQuestions = 10;
    
    // Function to display an MCQ item
    const renderMcqItem = (mcq) => (
        <div key={mcq.id} className="p-5 bg-white shadow-lg rounded-xl border border-gray-100">
            <p className="text-lg font-semibold text-gray-800 mb-3">
                {mcq.id}. {mcq.question}
            </p>
            <div className="space-y-2">
                {mcq.options.map((option, index) => (
                    <div key={index} className="flex items-center">
                        {/* Using text-indigo-600 for the radio buttons/options */}
                        <input
                            type="radio"
                            name={`q-${mcq.id}`}
                            id={`q-${mcq.id}-opt-${index}`}
                            className="text-indigo-600 focus:ring-indigo-500"
                            disabled // Disable inputs for viewing mode
                        />
                        <label 
                            htmlFor={`q-${mcq.id}-opt-${index}`} 
                            className="ml-3 text-base text-gray-700"
                        >
                            {option}
                        </label>
                    </div>
                ))}
            </div>
        </div>
    );

    return (
        <div className="space-y-12">
            {/* Chatbot Input Area - Blue and White Theme */}
            <div className="w-full max-w-2xl mx-auto py-12 px-4">
                <h1 className="text-4xl font-extrabold text-indigo-600 mb-4 text-center">
                    Quiz Generator
                </h1>
                <p className="text-center text-gray-600 mb-8">
                    Enter a topic to generate 20 Multiple Choice Questions (MCQs).
                </p>

                <form onSubmit={generateQuiz} className="flex space-x-3">
                    <input
                        type="text"
                        placeholder="e.g., Python Flask APIs"
                        value={topicInput}
                        onChange={(e) => setTopicInput(e.target.value)}
                        className="flex-grow p-3 border border-gray-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 shadow-sm"
                        disabled={loading}
                    />
                    <button
                        type="submit"
                        className="px-6 py-3 bg-indigo-600 text-white font-semibold rounded-xl hover:bg-indigo-700 transition duration-200 shadow-md disabled:bg-indigo-400"
                        disabled={loading}
                    >
                        {loading ? 'Generating...' : 'Generate Quiz'}
                    </button>
                </form>
            </div>

            {/* Quiz Display Area */}
            {loading && (
                <div className="text-center text-indigo-600 text-lg">
                    <p>Fetching 20 MCQs on "{topicInput}"...</p>
                </div>
            )}
            
            {quizData && (
                <div id="quiz-section" className="w-full max-w-4xl mx-auto space-y-8 p-4">
                    <div className="text-center p-6 bg-indigo-50 rounded-xl shadow-inner border border-indigo-200">
                        <h2 className="text-3xl font-bold text-indigo-800 mb-2">
                            Generated Quiz: {quizData[0]?.topic || 'New Topic'}
                        </h2>
                        <p className="text-lg text-indigo-700">
                            Total Questions: {quizData.length} | Test Requirement: Answer {requiredQuestions} Questions Correctly for 10 Marks.
                        </p>
                    </div>

                    <div className="space-y-6">
                        {quizData.map(renderMcqItem)}
                    </div>
                    
                    <div className="pt-8 text-center">
                        <button
                            className="px-8 py-3 bg-indigo-600 text-white font-bold text-lg rounded-xl hover:bg-indigo-700 transition duration-200 shadow-2xl"
                        >
                            Submit Test
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default HomePage;
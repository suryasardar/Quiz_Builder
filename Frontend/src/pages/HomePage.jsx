import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';

// 1. Initialize SocketIO client outside the component
// Connects to the Flask server running SocketIO
const socket = io('http://127.0.0.1:5000'); 

function HomePage() {
    const [topicInput, setTopicInput] = useState('');
    const [quizData, setQuizData] = useState([]); // Array to store streamed questions
    const [loading, setLoading] = useState(false);
    const [statusMessage, setStatusMessage] = useState('');

    useEffect(() => {
        // --- SocketIO Event Listeners ---
        
        // This runs only once when the component mounts
        socket.on('connect', () => {
            console.log('Connected to Flask SocketIO');
        });

        socket.on('new_question', (question) => {
            // 2. Add the new streamed question to the quizData array
            setQuizData(prevData => [...prevData, question]);
            // Optional: You can add logic here to scroll to the bottom
        });
        
        socket.on('quiz_status', (data) => {
            // 3. Update status messages and loading state based on backend events
            setStatusMessage(data.message);
            if (data.stage === 'START') {
                setLoading(true);
            } else if (data.stage === 'DONE' || data.stage === 'ERROR') {
                setLoading(false);
            }
        });
        
        socket.on('disconnect', () => {
            console.log('Disconnected from SocketIO');
            setLoading(false);
            setStatusMessage('Connection lost. Please refresh.');
        });

        // Cleanup function: remove listeners when the component unmounts
        return () => {
            socket.off('connect');
            socket.off('new_question');
            socket.off('quiz_status');
            socket.off('disconnect');
        };
    }, []); // Empty dependency array means this runs on mount/unmount only

    const generateQuiz = (e) => {
        e.preventDefault();
        if (!topicInput.trim()) return;

        // Clear previous state before starting
        setQuizData([]); 
        setStatusMessage('Requesting quiz generation...');
        setLoading(true);

        // 4. Emit the event to the Flask backend
        socket.emit('generate_quiz', { topic: topicInput });
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
                {/* Ensure mcq.options is an array before mapping */}
                {(mcq.options || []).map((option, index) => (
                    <div key={index} className="flex items-center">
                        <input
                            type="radio"
                            name={`q-${mcq.id}`}
                            id={`q-${mcq.id}-opt-${index}`}
                            className="text-indigo-600 focus:ring-indigo-500"
                            disabled // Disabled for initial viewing/streaming mode
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
            {/* Chatbot Input Area */}
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

            {/* Status and Loading Display */}
            {(loading || statusMessage) && (
                <div className="text-center text-indigo-600 text-lg">
                    <p className="p-4 bg-indigo-50 rounded-lg">{statusMessage}</p>
                </div>
            )}
            
            {/* Quiz Display Area - Shows questions as they stream in */}
            {quizData.length > 0 && (
                <div id="quiz-section" className="w-full max-w-4xl mx-auto space-y-8 p-4">
                    <div className="text-center p-6 bg-indigo-50 rounded-xl shadow-inner border border-indigo-200">
                        <h2 className="text-3xl font-bold text-indigo-800 mb-2">
                            Generated Quiz
                        </h2>
                        <p className="text-lg text-indigo-700">
                            Total Questions Generated: {quizData.length} | Test Requirement: Answer {requiredQuestions} Questions Correctly for 10 Marks.
                        </p>
                    </div>

                    <div className="space-y-6">
                        {quizData.map(renderMcqItem)}
                    </div>
                    
                    {/* Only show the Submit button once the loading/streaming is done */}
                    {!loading && quizData.length >= 20 && (
                        <div className="pt-8 text-center">
                            <button
                                className="px-8 py-3 bg-indigo-600 text-white font-bold text-lg rounded-xl hover:bg-indigo-700 transition duration-200 shadow-2xl"
                            >
                                Submit Test
                            </button>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default HomePage;
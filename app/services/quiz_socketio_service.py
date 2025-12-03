# app/services/quiz_socketio_service.py (REVISED FOR RELIABILITY)

from app import socketio, db
from flask import current_app
from flask_socketio import emit
from google import genai
from google.genai import types
import json
# import re # No longer needed for this method

# Global counter (still used for frontend ID assignment)
question_counter = 0

@socketio.on('generate_quiz')
def handle_generate_quiz(data):
    global question_counter
    question_counter = 0 
    
    topic = data.get('topic', 'General Knowledge')
    print(f"--- SOCKETIO: Received request to generate quiz on: {topic} ---")
    
    emit('quiz_status', {'message': f'Starting quiz generation on topic: {topic}', 'stage': 'START'})
    print(f"Starting quiz generation on topic: {topic}")
    
    try:
        client = genai.Client(api_key=current_app.config['GEMINI_API_KEY'])
        
        # 1. Define Prompt: Still need specific JSON instructions
        prompt = f"""
        Generate exactly 20 challenging multiple-choice questions (MCQs) on the topic of "{topic}".
        Each question must have exactly 4 options.
        The output MUST be a JSON array, where each object has these fields: 
        "question", "options" (an array of 4 strings), and "correct_index" (the 0-based index of the correct option). 
        ONLY output the raw JSON array. DO NOT include any introductory or concluding text.
        """
        
        # 2. Call non-streaming generate_content for reliability
        emit('quiz_status', {'message': 'Generating 20 MCQs (Wait time may be up to 15s)...', 'stage': 'GENERATING'})
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )

        # 3. Get the full response text
        full_json_text = response.text.strip()
        
        # 4. Clean up common LLM artifacts (like code fences)
        if full_json_text.startswith('```json'):
            full_json_text = full_json_text.strip('```json').strip()
        if full_json_text.endswith('```'):
            full_json_text = full_json_text.rstrip('```').strip()
            
        # 5. Parse the entire JSON array at once (Most reliable method)
        all_questions = json.loads(full_json_text)
        
        # 6. Process and Emit Questions sequentially (Simulating stream speed)
        for question in all_questions:
            question_counter += 1
            question['id'] = question_counter
            
            # Emit the question immediately after generating its ID
            emit('new_question', question)
            
            # Optional: Add a small sleep to simulate streaming if needed, but not required for function
            # time.sleep(0.1) 

        # 7. Final Completion Status
        emit('quiz_status', {'message': f'Quiz generation complete. {question_counter} questions loaded.', 'stage': 'DONE'})

    except json.JSONDecodeError as e:
        print(f"--- CRITICAL JSON PARSE ERROR ---: {e}")
        print(f"--- FAILED TEXT START: {full_json_text[:200]}...")
        emit('quiz_status', {'message': 'Error: Failed to parse LLM response into JSON. See server logs.', 'stage': 'ERROR'})
    
    except Exception as e:
        print(f"Gemini API Error: {e}")
        emit('quiz_status', {'message': f'Error generating quiz: {str(e)}', 'stage': 'ERROR'})
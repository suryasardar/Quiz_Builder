# app/services/quiz_socketio_service.py

from app import socketio, db
from flask import current_app
from flask_socketio import emit
from google import genai
from google.genai import types
import json
import re # For cleaning/parsing LLM output

# Global counter to track emitted questions (for ID generation)
question_counter = 0

@socketio.on('generate_quiz')
def handle_generate_quiz(data):
    """
    Handles the 'generate_quiz' event from the client, calls the LLM, 
    and streams back the questions one by one.
    """
    global question_counter
    question_counter = 0 # Reset counter for a new quiz
    
    # 1. Input Validation and Setup
    topic = data.get('topic', 'General Knowledge')
    print(f"--- SOCKETIO: Received request to generate quiz on: {topic} ---") # <--- ADD THIS LINE
    user_id = 1 # Placeholder: In a real app, retrieve user_id from session/token
    
    # Notify client that processing has started
    emit('quiz_status', {'message': f'Starting quiz generation on topic: {topic}', 'stage': 'START'})
    print(f"Starting quiz generation on topic: {topic}")
    try:
        # 2. Initialize Gemini Client
        client = genai.Client(api_key=current_app.config['GEMINI_API_KEY'])
        
        # 3. Define Prompt for LLM
        # IMPORTANT: We ask for JSON and use a very specific structure
        prompt = f"""
        Generate exactly 20 challenging multiple-choice questions (MCQs) on the topic of "{topic}".
        
        Each question must have exactly 4 options.
        The output MUST be a JSON array, where each object has these fields: 
        "question", "options" (an array of 4 strings), and "correct_index" (the 0-based index of the correct option). 
        
        ONLY output the raw JSON array. DO NOT include any introductory or concluding text.
        """
        
        # 4. Call Gemini Streaming API
        # Using gemini-2.5-flash for fast response
        response_stream = client.models.generate_content_stream(
            model='gemini-2.5-flash',
            contents=prompt,
        )

        # 5. Process and Stream Output
        # This part handles the streaming and parsing of the incoming JSON fragments.
        full_json_string = ""
        for chunk in response_stream:
            # Append the text chunk
            full_json_string += chunk.text

            # Try to extract the currently complete JSON object(s)
            # We look for complete question objects (ending with '}') followed by a comma or ']')
            
            # Simple RegEx to capture complete JSON objects within the stream
            # This logic is simplified; robust JSON streaming parsers are often preferred.
            match = re.search(r'(\{.*?\})\s*[,\]]', full_json_string)
            
            if match:
                json_object_str = match.group(1)
                
                try:
                    question_data = json.loads(json_object_str)
                    
                    # 6. Store Question in DB (Simplified)
                    # In a real app, you would save the Quiz record first, then save questions here.
                    # For now, we focus on the streaming UX.
                    
                    question_counter += 1
                    question_data['id'] = question_counter
                    question_data['is_streaming'] = True # Frontend flag

                    # 7. Stream the Question to the Frontend
                    emit('new_question', question_data)
                    
                    # Remove the processed object from the string
                    full_json_string = full_json_string[match.end(1):].strip()
                    if full_json_string.startswith(','):
                        full_json_string = full_json_string[1:].strip()
                    
                except json.JSONDecodeError:
                    # Ignore partial or invalid JSON fragments for now
                    pass

        # 8. Final Cleanup (if any questions were left or to signal completion)
        emit('quiz_status', {'message': 'Quiz generation complete.', 'stage': 'DONE'})

    except Exception as e:
        print(f"Gemini API Error: {e}")
        emit('quiz_status', {'message': f'Error generating quiz: {str(e)}', 'stage': 'ERROR'})

# Register the service handler in the app/services/__init__.py if needed
# For now, the import in app/__init__.py is sufficient to load this module.
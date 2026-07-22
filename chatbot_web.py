from flask import Flask, render_template, request, jsonify
import os
from anthropic import Anthropic

app = Flask(__name__)

# Initialize Anthropic client
client = Anthropic()

# Store conversation history for multi-turn conversations
conversation_history = []

def load_prompt():
    """Load the prompt from prompt.txt file"""
    try:
        with open("prompt.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "you're a marketing assistant"

def get_claude_response(user_message):
    """Get response from Claude API"""
    try:
        # Add user message to conversation history
        conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Get system prompt
        system_prompt = load_prompt()
        
        # Call Claude API
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system_prompt,
            messages=conversation_history
        )
        
        # Extract response text
        assistant_message = response.content[0].text
        
        # Add assistant response to conversation history
        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    except Exception as e:
        return f"Error communicating with Claude: {str(e)}"

@app.route('/')
def index():
    prompt = load_prompt()
    return render_template('index.html', prompt=prompt)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400
    
    bot_response = get_claude_response(user_message)
    return jsonify({'response': bot_response})

@app.route('/clear', methods=['POST'])
def clear_chat():
    """Clear conversation history"""
    global conversation_history
    conversation_history = []
    return jsonify({'status': 'cleared'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

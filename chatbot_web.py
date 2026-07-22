from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

def load_prompt():
    """Load the prompt from prompt.txt file"""
    try:
        with open("prompt.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "you're a marketing assistant"

def get_marketing_response(user_input):
    """Generate a marketing-themed response"""
    user_input_lower = user_input.lower()
    
    responses = {
        "hi": "Hello! I'm here to help you with your marketing needs. What would you like assistance with?",
        "help": "I can help you with marketing strategies, content creation, campaign planning, and customer engagement tips!",
        "price": "I'd be happy to discuss pricing! What product or service are you looking to market?",
        "campaign": "Great! Tell me more about your campaign goals, target audience, and budget.",
        "content": "Content is key! I can help you create engaging copy for social media, emails, blogs, and more.",
    }
    
    for keyword, response in responses.items():
        if keyword in user_input_lower:
            return response
    
    return f"That's interesting! As your marketing assistant, I can help you with: strategy, content, campaigns, SEO, social media, email marketing, and customer engagement. What interests you most?"

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
    
    bot_response = get_marketing_response(user_message)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

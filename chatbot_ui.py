import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import time

class ChatbotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Marketing Assistant Chatbot")
        self.root.geometry("600x700")
        self.root.configure(bg="#f0f0f0")
        
        # Load prompt from file
        self.prompt = self.load_prompt()
        
        # Create header
        self.header = tk.Label(
            root, 
            text="Marketing Assistant", 
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=10
        )
        self.header.pack(fill=tk.X)
        
        # Create chat display area
        self.chat_display = scrolledtext.ScrolledText(
            root,
            state=tk.DISABLED,
            height=20,
            width=70,
            font=("Arial", 10),
            bg="white",
            fg="#333333",
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure tags for styling
        self.chat_display.tag_config("user", foreground="#0084ff", font=("Arial", 10, "bold"))
        self.chat_display.tag_config("bot", foreground="#1abc9c", font=("Arial", 10, "bold"))
        self.chat_display.tag_config("system", foreground="#e74c3c", font=("Arial", 9, "italic"))
        
        # Create input frame
        input_frame = tk.Frame(root, bg="#f0f0f0")
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Create input field
        self.input_field = tk.Entry(
            input_frame,
            font=("Arial", 10),
            bg="white",
            fg="#333333",
            relief=tk.FLAT,
            borderwidth=1
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.input_field.bind("<Return>", lambda e: self.send_message())
        
        # Create send button
        self.send_button = tk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            bg="#2c3e50",
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20
        )
        self.send_button.pack(side=tk.RIGHT)
        
        # Create clear button
        self.clear_button = tk.Button(
            input_frame,
            text="Clear",
            command=self.clear_chat,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20
        )
        self.clear_button.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Display system message
        self.display_message("System", f"Prompt loaded: {self.prompt}", "system")
        self.display_message("Bot", "Hello! I'm your marketing assistant. How can I help you today?", "bot")
    
    def load_prompt(self):
        """Load the prompt from prompt.txt file"""
        try:
            with open("prompt.txt", "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return "you're a marketing assistant"
    
    def send_message(self):
        """Handle sending a message"""
        user_input = self.input_field.get().strip()
        
        if not user_input:
            messagebox.showwarning("Warning", "Please enter a message!")
            return
        
        # Display user message
        self.display_message("You", user_input, "user")
        self.input_field.delete(0, tk.END)
        
        # Simulate bot response in a separate thread
        threading.Thread(target=self.generate_response, args=(user_input,), daemon=True).start()
    
    def generate_response(self, user_input):
        """Generate a bot response (simulated)"""
        # Simulate processing time
        time.sleep(0.5)
        
        # In a real implementation, this would call your AI/ML model
        # For now, it's a placeholder response
        response = self.get_marketing_response(user_input)
        self.display_message("Bot", response, "bot")
    
    def get_marketing_response(self, user_input):
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
    
    def display_message(self, sender, message, tag=""):
        """Display a message in the chat"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: ", tag)
        self.chat_display.insert(tk.END, f"{message}\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def clear_chat(self):
        """Clear the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.display_message("System", "Chat cleared.", "system")


def main():
    root = tk.Tk()
    app = ChatbotUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

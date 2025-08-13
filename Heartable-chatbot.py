# Heartable Chatbot using Tkinter and OpenRouter.ai API
# Author: Sumit Kumar
# University: SBSSU, URN: 23303325, CSE'D' Student
# All copyright reserved to Sumit Kumar

import tkinter as tk
from tkinter import scrolledtext, font
import threading
import requests
import time
# Get api from openrouter.ai
API_KEY = "Enter Your Api Key"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_ID = "openai/gpt-4o"

class HeartableChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("💖 Heartable Chatbot")
        self.root.geometry("600x700")
        self.root.configure(bg="#0f0f0f")

        # Fonts
        self.default_font = font.Font(family="Helvetica", size=12)
        self.italic_font = font.Font(family="Helvetica", size=12, slant="italic")

        # Title label
        self.title_label = tk.Label(root, text="💖 Heartable Chatbot", font=("Helvetica", 20, "bold"),
                                    fg="#00FF00", bg="#0f0f0f")
        self.title_label.pack(pady=10)

        # Chat area
        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=self.default_font)
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.configure(state='disabled', bg="#1a1a1a", fg="#ffffff")

        # Entry frame
        self.entry_frame = tk.Frame(root, bg="#0f0f0f")
        self.entry_frame.pack(padx=10, pady=5, fill=tk.X)

        # Entry widget
        self.entry_msg = tk.Entry(self.entry_frame, font=("Helvetica", 14), bg="#1a1a1a", fg="#ffffff", insertbackground="white")
        self.entry_msg.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))
        self.entry_msg.bind("<Return>", self.send_message)

        # Send button
        self.send_btn = tk.Button(self.entry_frame, text="Send", command=self.send_message, bg="#00FF00", fg="#000000")
        self.send_btn.pack(side=tk.RIGHT)

        # Footer
        self.footer_label = tk.Label(root, text="Created by Sumit Kumar, SBSSU University, URN 23303325, CSE'D' Student",
                                     font=("Helvetica", 8, "bold"), fg="#00FF00", bg="#0f0f0f")
        self.footer_label.pack(side=tk.BOTTOM, pady=5)

        # Welcome animation
        self.show_welcome_animation()

    def show_welcome_animation(self):
        welcome_text = "Welcome to Heartable! 💖\nYour AI companion powered by OpenRouter.ai\n\n"
        self.chat_area.configure(state='normal')
        for char in welcome_text:
            self.chat_area.insert(tk.END, char)
            self.chat_area.update()
            time.sleep(0.02)
        self.chat_area.configure(state='disabled')

    def send_message(self, event=None):
        user_msg = self.entry_msg.get().strip()
        if not user_msg:
            return
        self.entry_msg.delete(0, tk.END)
        self.display_message(f"You: {user_msg}\n")
        threading.Thread(target=self.get_bot_response, args=(user_msg,)).start()

    def display_message(self, message, color="#ffffff", font_style=None):
        self.chat_area.configure(state='normal')
        tag_name = f"tag_{time.time()}"
        self.chat_area.insert(tk.END, message, (tag_name,))
        self.chat_area.tag_config(tag_name, foreground=color, font=font_style or self.default_font)
        self.chat_area.see(tk.END)
        self.chat_area.configure(state='disabled')

    # Typing animation
    def typing_animation(self):
        self.typing_tag = f"Heartable is typing...\n"
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, self.typing_tag, ("typing",))
        self.chat_area.tag_config("typing", foreground="#888888", font=self.italic_font)
        self.chat_area.see(tk.END)
        self.chat_area.configure(state='disabled')

    def remove_typing_animation(self):
        self.chat_area.configure(state='normal')
        content = self.chat_area.get("1.0", tk.END)
        content = content.replace(self.typing_tag, "")
        self.chat_area.delete("1.0", tk.END)
        self.chat_area.insert(tk.END, content)
        self.chat_area.configure(state='disabled')

    def get_bot_response(self, user_msg):
        self.typing_animation()

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL_ID,
            "messages": [
                {"role": "system", "content": "You are Heartable, a friendly AI chatbot created by Sumit Kumar."},
                {"role": "user", "content": user_msg}
            ],
            "max_tokens": 500
        }

        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=15)
            data = response.json()
            print("Full API response:", data)

            bot_reply = "Sorry, I could not respond."
            if "choices" in data and len(data["choices"]) > 0:
                msg_data = data["choices"][0].get("message")
                if msg_data and "content" in msg_data:
                    bot_reply = msg_data["content"]

        except Exception as e:
            bot_reply = "Error connecting to Heartable server. Please try again."
            print("API Error:", e)

        self.remove_typing_animation()
        self.display_message(f"Heartable: {bot_reply}\n", color="#00FF00")


if __name__ == "__main__":
    root = tk.Tk()
    app = HeartableChatbot(root)
    root.mainloop()

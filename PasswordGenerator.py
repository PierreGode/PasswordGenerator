import tkinter as tk
from tkinter import messagebox
import string
import random
import pyperclip
import threading
from transformers import pipeline

# Splash Screen Function
def show_splash_screen(duration, on_close_callback):
    splash_root = tk.Tk()
    splash_root.title("Loading...")
    splash_root.geometry("300x150")  # Width x Height
    center_window(splash_root, 300, 150)
    splash_label = tk.Label(splash_root, text="Please wait, loading...", font=("Arial", 14))
    splash_label.pack(expand=True)
    # Close the splash screen after the background tasks are done.
    def close_splash():
        splash_root.destroy()
        on_close_callback()  # Call the callback to open main window

    # The after() method schedules the splash screen to close after a minimum duration.
    # The actual closing might be delayed if the background tasks are not done.
    splash_root.after(duration, close_splash)
    splash_root.mainloop()

def center_window(root, width, height):
    # Calculate position x, y to center the window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

# Generator initialization for lazy loading
generator = None

def load_model():
    global generator
    if generator is None:
        # Lazy loading of the model
        generator = pipeline('text-generation', model='distilgpt2', truncation=True)
    return generator

# Generate a word pool from the model
word_pool = []

def generate_word_pool(size=15):
    global word_pool
    generator = load_model()  # Ensure the generator is loaded
    prompt = " "
    generated = generator(prompt, max_length=50, num_return_sequences=size)
    for item in generated:
        sentence = item['generated_text']
        words = sentence.split()
        for word in words:
            clean_word = ''.join(e for e in word if e.isalnum())
            if clean_word:
                word_pool.append(clean_word)
    word_pool = list(set(word_pool))  # Remove duplicates

def start_background_tasks(callback):
    def background_job():
        load_model()
        generate_word_pool()
        callback()  # Signal when the background job is done

    threading.Thread(target=background_job, daemon=True).start()

# Deferred opening of the main window until the background tasks are done
def open_main_window():
    main_window()

def main_window():
    window = tk.Tk()
    window.title("Password Generator")
    window.config(padx=20, pady=20, bg="#f0f0f0")
    center_window(window, 600, 400)
    # Your main window code here...
    window.mainloop()

if __name__ == "__main__":
    # Call to show the splash screen, with a minimum duration of 1500 milliseconds,
    # and pass open_main_window as the callback to be executed once the splash and
    # background jobs are done.
    show_splash_screen(1500, lambda: start_background_tasks(open_main_window))
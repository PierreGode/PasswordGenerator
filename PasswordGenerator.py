import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import string
import random
import pyperclip
import threading
from transformers import pipeline
import time

def splash_screen():
    def simulate_loading(root):
        for i in range(101):
            progress_bar['value'] = i
            root.update_idletasks()  # Update the GUI
            time.sleep(0.05)  # Simulate loading
        root.after(1000, lambda: close_splash(root))  # Close the splash screen after 1 second

    def close_splash(root):
        root.destroy()
        open_main_app()  # Open the main app after closing the splash screen

    splash_root = tk.Tk()
    splash_root.title("Splash Screen")

    # Configure window size and position
    window_width = 300
    window_height = 150
    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()
    x = (screen_width / 2) - (window_width / 2)
    y = (screen_height / 2) - (window_height / 2)
    splash_root.geometry("%dx%d+%d+%d" % (window_width, window_height, x, y))

    # Create a label for the loading text
    loading_label = ttk.Label(splash_root, text="Password generator loading...", font=("Arial", 12))
    loading_label.pack(pady=10)

    # Create a progress bar
    progress_bar = ttk.Progressbar(splash_root, orient="horizontal", length=200, mode="determinate")
    progress_bar.pack(pady=10)

    # Simulate loading
    splash_root.after(100, lambda: simulate_loading(splash_root))

    splash_root.mainloop()

def open_main_app():
    def async_load_model_and_generate_pool(status_label):
        load_model()
        generate_word_pool()
        # Update the UI on completion
        status_label.config(text="Model loaded, word pool ready.", fg="green")

    def load_model():
        global generator
        if generator is None:
            generator = pipeline('text-generation', model='tiny-text-gen-model', truncation=True)
        return generator

    def generate_word_pool(size=15):
        global word_pool
        # Ensure the generator is loaded before trying to generate the word pool
        if generator is None:
            load_model()
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

    def onClickHelp():
        messagebox.showinfo("Password Generator Help", "1. Choose password length (minimum 10 characters).\n2. Select options for including special characters, sentence-based password, and auto-copying to clipboard.\n3. Click 'Generate Password'.")

    def onClickAbout():
        messagebox.showinfo("About Password Generator", "Created by Pierre Gode, 2022.\nUpdated with AI-based Word Pool, 2024.")

    def generateSentenceBasedPassword(length, include_special_chars=False):
        if not word_pool:
            messagebox.showinfo("Please wait", "The word pool is still loading. Please try again in a few moments.")
            return ""
        password = ""
        while len(password) < length:
            password += random.choice(word_pool)
        password = password[:length]  # Ensure the desired length
        if include_special_chars:
            special_chars = string.punctuation
            for _ in range(min(5, length // 5)):
                pos = random.randint(1, len(password) - 2)
                password = password[:pos] + random.choice(special_chars) + password[pos:]
        return password

    def assessPasswordStrength(password):
        length = len(password)
        has_lower = any(char.islower() for char in password)
        has_upper = any(char.isupper() for char in password)
        has_digit = any(char.isdigit() for char in password)
        has_special = any(char in string.punctuation for char in password)
        
        if length >= 12 and has_lower and has_upper and has_digit and has_special:
            return "Very Strong"
        elif length >= 10 and has_lower and has_upper and (has_digit or has_special):
            return "Strong"
        else:
            return "Weak"

    def updatePasswordStrengthDisplay(strength):
        colors = {"Weak": "#ff9900", "Strong": "#00ff00", "Very Strong": "#006400"}
        passwordStrengthLabel.config(text=f"Password Strength: {strength}", fg=colors[strength])

    def passwordGenerator():
        copyBtn.config(text="Copy to Clipboard")
        include_special_chars = specialChars.get() == 1
        try:
            length = int(charInput.get())
            if length < 10:
                messagebox.showwarning("Invalid Input", "Password length must be at least 10.")
                return
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid number.")
            return
        
        strength = "Weak"
        while strength not in ["Strong", "Very Strong"]:
            if passwordType.get() == "Sentence":
                password = generateSentenceBasedPassword(length, include_special_chars)
            else:
                password_chars = string.ascii_letters + string.digits
                if include_special_chars:
                    password_chars += string.punctuation
                password = "".join(random.choice(password_chars) for _ in range(length))
            strength = assessPasswordStrength(password)
        
        if not password:  # To handle the case where word pool wasn't ready
            return

        passwordField.delete(0, tk.END)
        passwordField.insert(0, password)
        updatePasswordStrengthDisplay(strength)
        
        if copyToClipboard.get() == 1:
            pyperclip.copy(password)
            copyBtn.config(text="Copied!")

    def start_background_tasks(status_label):
        threading.Thread(target=lambda: async_load_model_and_generate_pool(status_label), daemon=True).start()

    # Global variables for model and word pool
    global generator
    generator = None
    global word_pool
    word_pool = []

    # GUI Setup
    window = tk.Tk()
    window.title("Password Generator")
    window.config(padx=20, pady=20, bg="#f0f0f0")

    menubar = tk.Menu(window)
    fileMenu = tk.Menu(menubar, tearoff=0)
    fileMenu.add_command(label="Exit", command=window.quit)
    menubar.add_cascade(label="File", menu=fileMenu)

    helpMenu = tk.Menu(menubar, tearoff=0)
    helpMenu.add_command(label="Help", command=onClickHelp)
    helpMenu.add_command(label="About", command=onClickAbout)
    menubar.add_cascade(label="Help", menu=helpMenu)

    window.config(menu=menubar)

    specialChars = tk.IntVar()
    copyToClipboard = tk.IntVar()
    passwordType = tk.StringVar(value="Traditional")

    titleLabel = tk.Label(window, text="Password Generator", bg="#f0f0f0", fg="#333333", font=("Arial", 20, "bold"))
    titleLabel.grid(row=0, column=0, columnspan=4, pady=(0,20))

    lengthLabel = tk.Label(window, text="Password length:", bg="#f0f0f0", fg="#333333", font=("Arial", 12))
    lengthLabel.grid(row=1, column=0, sticky="w")

    charInput = tk.Entry(window, font=("Arial", 12), width=10)
    charInput.grid(row=1, column=1, sticky="w")
    charInput.insert(0, "12")

    specialCharsCheck = tk.Checkbutton(window, text="Include Special Characters", variable=specialChars, bg="#f0f0f0", font=("Arial", 10))
    specialCharsCheck.grid(row=2, column=0, columnspan=2, sticky="w")

    passwordTypeLabel = tk.Label(window, text="Password Type:", bg="#f0f0f0", fg="#333333", font=("Arial", 12))
    passwordTypeLabel.grid(row=2, column=2, sticky="w")

    passwordTypeTraditional = tk.Radiobutton(window, text="Traditional", variable=passwordType, value="Traditional", bg="#f0f0f0", font=("Arial", 10))
    passwordTypeTraditional.grid(row=3, column=2, sticky="w")

    passwordTypeSentence = tk.Radiobutton(window, text="Sentence", variable=passwordType, value="Sentence", bg="#f0f0f0", font=("Arial", 10))
    passwordTypeSentence.grid(row=3, column=3, sticky="w")

    copyClipboardCheck = tk.Checkbutton(window, text="Copy to Clipboard Automatically", variable=copyToClipboard, bg="#f0f0f0", font=("Arial", 10))
    copyClipboardCheck.grid(row=4, column=0, columnspan=2, sticky="w")

    generateBtn = tk.Button(window, text="Generate Password", command=passwordGenerator, bg="#4CAF50", fg="white", font=("Arial", 12), width=20)
    generateBtn.grid(row=5, column=0, columnspan=2, pady=(20,0))

    copyBtn = tk.Button(window, text="Copy to Clipboard", command=lambda: pyperclip.copy(passwordField.get()), bg="#2196F3", fg="white", font=("Arial", 12), width=20)
    copyBtn.grid(row=5, column=2, columnspan=2, pady=(20,0))

    passwordField = tk.Entry(window, font=("Arial", 14), width=35, bd=2, relief="groove")
    passwordField.grid(row=6, column=0, columnspan=4, pady=(10,0))

    passwordStrengthLabel = tk.Label(window, text="", bg="#f0f0f0", fg="#333333", font=("Arial", 10))
    passwordStrengthLabel.grid(row=7, column=0, columnspan=4)

    modelStatusLabel = tk.Label(window, text="Loading model and generating word pool...", bg="#f0f0f0", fg="orange", font=("Arial", 10))
    modelStatusLabel.grid(row=8, column=0, columnspan=4)

    if __name__ == "__main__":
        start_background_tasks(modelStatusLabel)  # Passing the status label to the background task function
        window.mainloop()

# Start with the splash screen
splash_screen()

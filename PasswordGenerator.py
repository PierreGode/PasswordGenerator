import tkinter as tk
from tkinter import messagebox
import string
import random
import pyperclip
import threading


# Function to asynchronously load the model and generate the word pool
def async_load_model_and_generate_pool():
    load_model()
    generate_word_pool()

# Lazy loading of the generator to avoid slowing down the app startup
def load_model():
    global generator
    if generator is None:
        from transformers import pipeline
        generator = pipeline('text-generation', model='distilgpt2', truncation=True)
    return generator

# Initialize generator as None for lazy loading
generator = None

# Initialize a word pool
word_pool = []

# Generate a word pool from the model output, ensuring variety
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
    messagebox.showinfo("Password Generator Help", "1. Choose password length (minimum 10 characters).\n2. Select options for including special characters, sentence for password, and auto-copying to clipboard.\n3. Click 'Generate Password'.")

def onClickAbout():
    messagebox.showinfo("About Password Generator", "Created by Pierre Gode, 2022.\nUpdated with AI-based Word Pool, 2024.")

def generateSentenceBasedPassword(length, include_special_chars=False):
    if not word_pool:
        generate_word_pool()
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
    
    # Keep generating passwords until a strong or very strong one is generated
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
    
    passwordField.delete(0, tk.END)
    passwordField.insert(0, password)
    updatePasswordStrengthDisplay(strength)
    
    if copyToClipboard.get() == 1:
        pyperclip.copy(password)
        copyBtn.config(text="Copied!")

# Start the background task for model loading and word pool generation
def start_background_tasks():
    threading.Thread(target=async_load_model_and_generate_pool, daemon=True).start()

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

if __name__ == "__main__":
    start_background_tasks()  # Start loading model and generating word pool in the background
    window.mainloop()

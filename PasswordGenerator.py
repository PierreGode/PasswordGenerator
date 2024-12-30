import tkinter as tk
from tkinter import messagebox
import string
import random
import pyperclip
import threading
from transformers import pipeline

# Initialize global variables
generator = None
word_pool = set()

# Function to asynchronously load the model and generate the word pool
def async_load_model_and_generate_pool():
    load_model()
    generate_word_pool()

# Lazy loading of the generator to avoid slowing down the app startup
def load_model():
    global generator
    if generator is None:
        try:
            generator = pipeline('text-generation', model='distilgpt2', truncation=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load the model: {e}")
    return generator

# Generate a word pool from the model output, ensuring variety
def generate_word_pool(size=15):
    global word_pool
    if generator is None:
        load_model()
    prompt = "Generate a list of diverse words: "
    try:
        generated = generator(prompt, max_length=50, num_return_sequences=size, clean_up_tokenization_spaces=True)
        # Use set comprehension for uniqueness and efficiency
        new_words = {
            ''.join(filter(str.isalnum, word)) 
            for item in generated 
            for word in item['generated_text'].split()
            if ''.join(filter(str.isalnum, word))
        }
        word_pool.update(new_words)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate word pool: {e}")

def onClickHelp():
    messagebox.showinfo(
        "Password Generator Help",
        "1. Choose password length (minimum 10 characters).\n"
        "2. Select options for including special characters, sentence for password, and auto-copying to clipboard.\n"
        "3. Click 'Generate Password'."
    )

def onClickAbout():
    messagebox.showinfo(
        "About Password Generator",
        "Created by Pierre Gode, 2022.\nUpdated with AI-based Word Pool, 2024."
    )

def generateSentenceBasedPassword(length, include_special_chars=False):
    if not word_pool:
        generate_word_pool()
    if not word_pool:
        messagebox.showwarning("Word Pool Unavailable", "Word pool is not ready. Please try again shortly.")
        return ""
    password = ''.join(random.choices(tuple(word_pool), k=length))
    password = password[:length]  # Ensure the desired length
    if include_special_chars:
        special_chars = string.punctuation
        num_special = max(1, length // 5)
        password = list(password)
        for _ in range(num_special):
            pos = random.randint(0, len(password) - 1)
            password[pos] = random.choice(special_chars)
        password = ''.join(password)
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
    passwordStrengthLabel.config(text=f"Password Strength: {strength}", fg=colors.get(strength, "#333333"))

def passwordGenerator():
    copyBtn.config(text="Copy to Clipboard", state="disabled")
    include_special_chars = specialChars.get() == 1
    try:
        length = int(charInput.get())
        if length < 10:
            messagebox.showwarning("Invalid Input", "Password length must be at least 10.")
            return
    except ValueError:
        messagebox.showwarning("Invalid Input", "Please enter a valid number.")
        return
    
    # Generate password based on selected type
    if passwordType.get() == "Sentence":
        password = generateSentenceBasedPassword(length, include_special_chars)
    else:
        password_chars = string.ascii_letters + string.digits
        if include_special_chars:
            password_chars += string.punctuation
        password = ''.join(random.choices(password_chars, k=length))
    
    # Assess strength
    strength = assessPasswordStrength(password)
    
    # Update UI
    passwordField.delete(0, tk.END)
    passwordField.insert(0, password)
    updatePasswordStrengthDisplay(strength)
    
    if copyToClipboard.get() == 1 and password:
        pyperclip.copy(password)
        copyBtn.config(text="Copied!", state="normal")
    else:
        copyBtn.config(state="normal")

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

# Variables
specialChars = tk.IntVar()
copyToClipboard = tk.IntVar()
passwordType = tk.StringVar(value="Traditional")

# Widgets
titleLabel = tk.Label(
    window, text="Password Generator", bg="#f0f0f0", fg="#333333",
    font=("Arial", 20, "bold")
)
titleLabel.grid(row=0, column=0, columnspan=4, pady=(0, 20))

lengthLabel = tk.Label(
    window, text="Password length:", bg="#f0f0f0", fg="#333333",
    font=("Arial", 12)
)
lengthLabel.grid(row=1, column=0, sticky="w")

charInput = tk.Entry(window, font=("Arial", 12), width=10)
charInput.grid(row=1, column=1, sticky="w")
charInput.insert(0, "12")

specialCharsCheck = tk.Checkbutton(
    window, text="Include Special Characters", variable=specialChars,
    bg="#f0f0f0", font=("Arial", 10)
)
specialCharsCheck.grid(row=2, column=0, columnspan=2, sticky="w")

passwordTypeLabel = tk.Label(
    window, text="Password Type:", bg="#f0f0f0", fg="#333333",
    font=("Arial", 12)
)
passwordTypeLabel.grid(row=2, column=2, sticky="w")

passwordTypeTraditional = tk.Radiobutton(
    window, text="Traditional", variable=passwordType, value="Traditional",
    bg="#f0f0f0", font=("Arial", 10)
)
passwordTypeTraditional.grid(row=3, column=2, sticky="w")

passwordTypeSentence = tk.Radiobutton(
    window, text="Sentence", variable=passwordType, value="Sentence",
    bg="#f0f0f0", font=("Arial", 10)
)
passwordTypeSentence.grid(row=3, column=3, sticky="w")

copyClipboardCheck = tk.Checkbutton(
    window, text="Copy to Clipboard Automatically", variable=copyToClipboard,
    bg="#f0f0f0", font=("Arial", 10)
)
copyClipboardCheck.grid(row=4, column=0, columnspan=2, sticky="w")

generateBtn = tk.Button(
    window, text="Generate Password", command=passwordGenerator,
    bg="#4CAF50", fg="white", font=("Arial", 12), width=20
)
generateBtn.grid(row=5, column=0, columnspan=2, pady=(20, 0))

copyBtn = tk.Button(
    window, text="Copy to Clipboard", command=lambda: pyperclip.copy(passwordField.get()),
    bg="#2196F3", fg="white", font=("Arial", 12), width=20, state="disabled"
)
copyBtn.grid(row=5, column=2, columnspan=2, pady=(20, 0))

passwordField = tk.Entry(
    window, font=("Arial", 14), width=35, bd=2, relief="groove"
)
passwordField.grid(row=6, column=0, columnspan=4, pady=(10, 0))

passwordStrengthLabel = tk.Label(
    window, text="", bg="#f0f0f0", fg="#333333", font=("Arial", 10)
)
passwordStrengthLabel.grid(row=7, column=0, columnspan=4)

if __name__ == "__main__":
    start_background_tasks()  # Start loading model and generating word pool in the background
    window.mainloop()

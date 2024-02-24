import tkinter as tk
from tkinter import messagebox
import ctypes
import os
import string
import random
import pyperclip
from transformers import pipeline

# Check if the application is run as an administrator
def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

# Help Dialog
def onClickHelp():
    messagebox.showinfo("Password Generator Help", "1. Choose password length.\n2. Select options for including special characters, sentences for password, and auto-copying to clipboard.\n3. Click 'Generate Password'.")

# About Dialog
def onClickAbout():
    messagebox.showinfo("About Password Generator", "Created by Pierre Gode, 2022.\nUpdated Version 2024.")

# Clear Clipboard
def clearPyper():
    pyperclip.copy('')

# Generate Sentence-based Password
def generateSentenceBasedPassword(length):
    generator = pipeline('text-generation', model='gpt2')
    sentences = generator(" ", max_length=50, num_return_sequences=1)
    sentence = sentences[0]['generated_text']
    password = ''.join(e for e in sentence if e.isalnum())  # Remove spaces and punctuation
    return password[:length]

# Generate Password
def passwordGenerator():
    # Reset the Copy to Clipboard button's text when generating a new password
    copyBtn.config(text="Copy to Clipboard")
    
    if passwordType.get() == "Sentence":
        try:
            length = int(charInput.get())
            if length < 4 or length > 10:
                raise ValueError
            password = generateSentenceBasedPassword(length)  # Adjusted to pass length
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid number of sentences (4-10).")
            return
    else:
        if specialChars.get():
            password_chars = string.ascii_letters + string.digits + string.punctuation
        else:
            password_chars = string.ascii_letters + string.digits
        
        try:
            length = int(charInput.get())
            if length < 8 or length > 48:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid length (8-48).")
            return
        
        password = "".join(random.choice(password_chars) for _ in range(length))
    
    passwordField.delete(0, tk.END)
    passwordField.insert(0, password)
    
    # Assessing Password Strength
    strength = assessPasswordStrength(password)
    updatePasswordStrengthDisplay(strength)
    
    if copyToClipboard.get():
        pyperclip.copy(password)
        copyBtn.config(text="Copied!")

# Assessing Password Strength
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
    elif length >= 8 and (has_lower or has_upper) and (has_digit or has_special):
        return "Weak"
    else:
        return "Very Weak"

def updatePasswordStrengthDisplay(strength):
    passwordStrengthLabel.config(text=f"Password Strength: {strength}")
    # Optional: Adjust the color based on the strength
    colors = {
        "Very Weak": "#ff0000",
        "Weak": "#ff9900",
        "Strong": "#00ff00",
        "Very Strong": "#006400"
    }
    passwordStrengthLabel.config(fg=colors[strength])

# Initialize Window
window = tk.Tk()
window.title("Password Generator")
window.config(padx=20, pady=20, bg="#f0f0f0")

# Menu
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

# UI Elements
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

copyClipboardCheck = tk.Checkbutton(window, text="Copy to Clipboard", variable=copyToClipboard, bg="#f0f0f0", font=("Arial", 10), state=tk.NORMAL if is_admin() else tk.DISABLED)
copyClipboardCheck.grid(row=4, column=0, columnspan=2, sticky="w")

generateBtn = tk.Button(window, text="Generate Password", command=passwordGenerator, bg="#4CAF50", fg="white", font=("Arial", 12), width=20)
generateBtn.grid(row=5, column=0, columnspan=2, pady=(20,0))

copyBtn = tk.Button(window, text="Copy to Clipboard", command=lambda: [pyperclip.copy(passwordField.get()), copyBtn.config(text="Copied!")], bg="#2196F3", fg="white", font=("Arial", 12), width=20)
copyBtn.grid(row=5, column=2, columnspan=2, pady=(20,0))

passwordField = tk.Entry(window, font=("Arial", 14), width=35, bd=2, relief="groove")
passwordField.grid(row=6, column=0, columnspan=4, pady=(10,0))

passwordStrengthLabel = tk.Label(window, text="", bg="#f0f0f0", fg="#333333", font=("Arial", 10))
passwordStrengthLabel.grid(row=7, column=0, columnspan=4)

# Configure rows and columns for responsive design
for i in range(8):
    window.grid_rowconfigure(i, weight=1)
for i in range(4):
    window.grid_columnconfigure(i, weight=1)

window.mainloop()
import tkinter as tk
from tkinter import messagebox, ttk
import ctypes
import os
import string
import random
import pyperclip

# Check if the application is run as an administrator
def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

# Help Dialog
def onClickHelp():
    messagebox.showinfo("Password Generator Help", "1. Choose password length.\n2. Select options for including special characters and auto-copying to clipboard.\n3. Click 'Generate Password'.")

# About Dialog
def onClickAbout():
    messagebox.showinfo("About Password Generator", "Created by Pierre Gode, 2022.\nUpdated Version 2024.")

# Clear Clipboard
def clearPyper():
    pyperclip.copy('')

# Generate Password
def passwordGenerator():
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
    
    if copyToClipboard.get():
        pyperclip.copy(password)
        copyBtn.config(text="Copied!")

# Reset Copy Button Text
def resetCopyBtnText(event):
    copyBtn.config(text="Copy to Clipboard")

# Initialize Window
window = tk.Tk()
window.title("Pierre's Password Generator")
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

copyClipboardCheck = tk.Checkbutton(window, text="Copy to Clipboard", variable=copyToClipboard, bg="#f0f0f0", font=("Arial", 10), state=tk.NORMAL if is_admin() else tk.DISABLED)
copyClipboardCheck.grid(row=3, column=0, columnspan=2, sticky="w")

generateBtn = tk.Button(window, text="Generate Password", command=passwordGenerator, bg="#4CAF50", fg="white", font=("Arial", 12), width=20)
generateBtn.grid(row=4, column=0, columnspan=2, pady=(20,0))

copyBtn = tk.Button(window, text="Copy to Clipboard", command=lambda: [pyperclip.copy(passwordField.get()), copyBtn.config(text="Copied!")], bg="#2196F3", fg="white", font=("Arial", 12), width=20)
copyBtn.grid(row=4, column=2, columnspan=2, pady=(20,0))
copyBtn.bind("<Button-1>", resetCopyBtnText)

passwordField = tk.Entry(window, font=("Arial", 14), width=35, bd=2, relief="groove")
passwordField.grid(row=5, column=0, columnspan=4, pady=(10,0))

# Configure rows and columns for responsive design
for i in range(6):  # Configure all six rows to be responsive
    window.grid_rowconfigure(i, weight=1)

for i in range(4):  # Configure all four columns to be responsive
    window.grid_columnconfigure(i, weight=1)

window.mainloop()

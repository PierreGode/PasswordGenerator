import tkinter as tk
from tkinter import ttk, messagebox
import ctypes
import os
import string
import random
import pyperclip

def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

class PasswordGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pierre's Advanced Password Generator")
        self.config(padx=50, pady=50, bg="#235066")
        # Optionally set a local icon file here:
        # self.iconbitmap('path_to_your_icon_file.ico')
        
        self.admin_status = is_admin()
        self.create_menu()
        self.create_variables()
        self.create_widgets()
        self.layout_widgets()

    def create_menu(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.on_help)
        helpmenu.add_command(label="About...", command=self.on_about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        
        self.config(menu=menubar)

    def create_variables(self):
        self.use_special = tk.IntVar(value=1)
        self.copy_to_clip = tk.IntVar(value=1 if self.admin_status else 0)
        self.exclude_ambiguous = tk.IntVar(value=0)
        self.password_length = tk.IntVar(value=12)

    def create_widgets(self):
        # Title Label
        self.label_title = ttk.Label(self, text="Advanced Password Generator", 
                                     font=("Arial", 20, "bold"), background="#235066", foreground="#c5d7bd")
        # Slider for length
        self.length_slider = ttk.Scale(self, from_=6, to=32, orient='horizontal', variable=self.password_length,
                                       command=self.update_length_display)
        self.length_display = ttk.Label(self, text=f"Length: {self.password_length.get()}", background="#235066", foreground="#c5d7bd", font=("Arial", 12, "bold"))
        
        # Checkbuttons
        self.cb_special = ttk.Checkbutton(self, text="Include Special Characters", variable=self.use_special)
        self.cb_ambiguous = ttk.Checkbutton(self, text="Exclude Ambiguous Characters (iIl1O0)", variable=self.exclude_ambiguous)
        self.cb_clip = ttk.Checkbutton(self, text="Copy to Clipboard", variable=self.copy_to_clip,
                                        state=tk.NORMAL if self.admin_status else tk.DISABLED)
        
        # Entry for manual length input (with validation)
        vcmd = (self.register(self.validate_int), '%P')
        self.length_entry = ttk.Entry(self, textvariable=self.password_length, validate='key', validatecommand=vcmd, width=5)
        
        # Password display field
        self.password_field = ttk.Entry(self, font=("Arial", 15, "bold"), width=40)
        # Prevent direct editing
        self.password_field.bind('<Control-v>', lambda _: 'break')
        self.password_field.bind('<Control-c>', lambda _: 'break')
        self.password_field.bind('<BackSpace>', lambda _: 'break')
        
        # Password strength indicator
        self.strength_label = ttk.Label(self, text="Strength: N/A", background="#235066", foreground="#c5d7bd", font=("Arial", 12, "bold"))
        
        # Buttons
        self.generate_button = ttk.Button(self, text="Generate Password", command=self.generate_password)
        self.clear_button = ttk.Button(self, text="Clear Clipboard", command=self.clear_clipboard)

    def layout_widgets(self):
        # Grid layout with padding and proper row/column spans
        self.label_title.grid(row=0, column=0, columnspan=4, pady=(0,20))
        
        # Password length slider and entry
        self.length_display.grid(row=1, column=0, sticky='w')
        self.length_slider.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
        self.length_entry.grid(row=1, column=2, padx=10)
        
        # Checkbuttons for options
        self.cb_special.grid(row=2, column=0, pady=5, sticky='w')
        self.cb_ambiguous.grid(row=2, column=1, pady=5, sticky='w')
        self.cb_clip.grid(row=2, column=2, pady=5, sticky='w')
        
        # Generate button spanning multiple columns
        self.generate_button.grid(row=3, column=0, columnspan=3, pady=20, sticky='ew')
        self.clear_button.grid(row=3, column=3, padx=10, pady=20)
        
        # Password display and strength indicator
        self.password_field.grid(row=4, column=0, columnspan=3, pady=(10, 0))
        self.strength_label.grid(row=4, column=3, padx=10)

    def update_length_display(self, event=None):
        self.length_display.config(text=f"Length: {int(self.password_length.get())}")

    def validate_int(self, P):
        # Allow only digits or empty input
        return P.isdigit() or P == ""

    def generate_password(self):
        try:
            length = int(self.length_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer for password length.")
            return

        if length <= 0:
            messagebox.showerror("Invalid Length", "Password length must be greater than zero.")
            return

        # Build character set based on options
        if self.use_special.get():
            chars = string.ascii_letters + string.digits + string.punctuation
        else:
            chars = string.ascii_letters + string.digits
        
        if self.exclude_ambiguous.get():
            ambiguous = "iIl1O0"
            chars = ''.join(ch for ch in chars if ch not in ambiguous)
        
        password = "".join(random.choice(chars) for _ in range(length))
        self.password_field.delete(0, tk.END)
        self.password_field.insert(0, password)
        
        # Update password strength indicator
        self.update_strength_indicator(password)
        
        if self.copy_to_clip.get():
            pyperclip.copy(password)

    def update_strength_indicator(self, password):
        # Basic strength evaluation: longer and diverse characters yield higher score.
        score = 0
        length = len(password)
        score += length
        diversity = len(set(password))
        score += diversity
        if any(c in string.punctuation for c in password):
            score += 5
        if any(c in string.digits for c in password):
            score += 3
        
        if score < 20:
            strength = "Weak"
        elif score < 35:
            strength = "Moderate"
        else:
            strength = "Strong"
        self.strength_label.config(text=f"Strength: {strength}")

    def clear_clipboard(self):
        pyperclip.copy('')
        messagebox.showinfo("Clipboard Cleared", "Clipboard has been cleared.")

    def on_help(self):
        messagebox.showinfo("Password Generator Help", 
                            "Generate a password with desired options.\n"
                            "Use the slider or entry to set length.\n"
                            "Toggle options for special characters and excluding ambiguous ones.\n"
                            "Run as administrator to enable clipboard copy.")

    def on_about(self):
        messagebox.showinfo("About", "Advanced Password Generator\nCreated by Pierre Gode 2022")

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()

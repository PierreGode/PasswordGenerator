import tkinter as tk
from tkinter import messagebox
import tkinter.messagebox
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


def onClickhelp():
    tkinter.messagebox.askokcancel("Password Generator Help.", "Run program as administrator to enable Copy to Clipboard")


def onClickabout():
    tkinter.messagebox.askokcancel("Password Generator About.", "Created by Pierre Gode 2022")


def clear_pyper():
    pyperclip.copy('')


def password_generator():
    if Checkbutton1.get() == 1:
        password_chars = string.ascii_letters + string.digits + string.punctuation
    else:
        password_chars = string.ascii_letters + string.digits
    password_field.delete(0, tk.END)
    length = int(char_input.get())
    password = "".join([random.choice(password_chars) for _ in range(length)])
    password_field.insert(0, password)
    if Checkbutton2.get() == 1:
        pyperclip.copy(password)


window = tk.Tk()
window.title("Pierre's Password Generator")
window.config(padx=50, pady=50, bg="#235066")
# Please replace the following line with a local file for the icon
# window.iconbitmap('path_to_your_icon_file.ico')

menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=onClickhelp)
helpmenu.add_command(label="About...", command=onClickabout)
menubar.add_cascade(label="Help", menu=helpmenu)

window.config(menu=menubar)

Checkbutton1 = tk.IntVar()
Checkbutton2 = tk.IntVar()

label_title = tk.Label(window, text="Password Generator", bg="#235066", fg="#c5d7bd", font=("Arial", 20, "bold"))
label_title.grid(row=0, column=0, columnspan=3, pady=30)

label_before_input = tk.Label(window, text="Password length:", bg="#235066", fg="#c5d7bd", font=("Arial", 15, "bold"))
label_before_input.grid(row=1, column=0)

label_before_input_pass = tk.Checkbutton(window, text="Special Characters", variable=Checkbutton1, bg="#235066", fg="#c5d7bd", onvalue=1, offvalue=0, height=2, font=("Arial", 9, "bold"), width=20, pady=5)
label_before_input_pass.grid(row=1, column=3)

char_input = tk.Entry(window, bg="#235066", font=("Arial", 12), width=40)
char_input.grid(row=1, column=1)
char_input.insert(0, "12")
char_input.focus()

generate_password_button = tk.Button(window, text="Generate Password", bg="#fb743e", height=4, width=55, command=password_generator)
generate_password_button.grid(row=4, column=0, columnspan=3, padx=50, pady=50)

clear_all = tk.Button(window, text="Clear clipboard", bg="#fb743e", height=2, width=11, command=clear_pyper)
clear_all.grid(row=4, column=3)

password_field = tk.Entry(window, bg="#285c75", font=("Arial", 15, "bold"), width=40)
password_field.grid(row=5, column=0, columnspan=3)
password_field.bind('<Control-v>', lambda _: 'break')
password_field.bind('<Control-c>', lambda _: 'break')
password_field.bind('<BackSpace>', lambda _: 'break')

admin_status = is_admin()
coptoclip = tk.Checkbutton(window, text="Copy to Clipboard", variable=Checkbutton2, bg="#235066", fg="#c5d7bd", onvalue=1, offvalue=0, height=2, font=("Arial", 9, "bold"), width=20, pady=5, state=tk.NORMAL if admin_status else tk.DISABLED)
coptoclip.grid(row=1, column=2)

window.mainloop()
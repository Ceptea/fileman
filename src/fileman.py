#!/usr/bin/python3
import tkinter as tk
import os
import subprocess as sb
import tkinter.messagebox as tkmsg
import ttkbootstrap as ttk
from tkinter import simpledialog

terminal = "st"
text_editor = "leafpad"


def file_type(file):
    return os.path.splitext(file)[1]


class APP:
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("fileman")
        self.root.geometry("720x480")
        self.files = tk.Listbox()
        self.context = tk.Menu(tearoff=0)
        self.context.add_command(label="Open", command=self.open_file)
        self.context.add_command(label="New file", command=self.new_file)
        self.context.add_command(label="New folder", command=self.new_folder)
        self.context.add_command(label="Delete", command=self.delete_file)
        self.context.add_command(label="Refresh", command=self.refresh)

        self.files.bind("<Double-Button-1>", self.doubleclick)
        self.root.bind("<Button-3>", self.context_menu)
        self.root.bind("<Button-1>", self.hide_context_menu)

        self.new_file = ttk.Button(text="New file.", command=self.new_file)
        self.refresh_button = ttk.Button(text="Refresh.", command=self.refresh)
        self.files.pack(fill=tk.BOTH, expand=1)
        self.new_file.pack(side="left")
        self.refresh_button.pack(side="left")

        self.refresh()

    def refresh(self):
        cwd = os.getcwd()
        self.files.delete(0, tk.END)
        files = os.listdir(cwd)
        self.files.insert(tk.END, f"..")
        for file in files:
            if os.path.isdir(file):
                self.files.insert(tk.END, f"{file}/")
            else:
                self.files.insert(tk.END, file)

    def new_file(self):
        newfile = simpledialog.askstring(title="fileman", prompt="Create a file.")
        if newfile:
            with open(newfile, "w"):
                pass
            self.refresh()

    def new_folder(self):
        new_folder = simpledialog.askstring(title="fileman", prompt="Create a folder.")
        if new_folder:
            os.mkdir(new_folder)
            self.refresh()

    def delete_file(self):
        file = self.get_file()
        answer = tkmsg.askyesno("fileman", f"Are you sure you want to delete {file}")
        if answer:
            if os.path.isdir(file):
                os.rmdir(file)
            else:
                os.remove(file)

    def open_file(self, event=""):
        file = self.get_file()
        if file == "..":
            os.chdir("..")
        match file_type(file):
            case ".txt":
                sb.Popen(f"{text_editor} {file}", shell=1)
            case ".py":
                sb.Popen(f"{terminal} python3 {file}", shell=1)
            case ".pye":
                sb.Popen(f"{terminal} ./{file}", shell=1)
            case ".sh":
                sb.Popen(f"{terminal} ./{file}", shell=1)
            case _:
                sb.Popen(f"xdg-open {file}", shell=1)
        self.refresh()

    def get_file(self):
        file = self.files.curselection()
        file = self.files.get(file)
        file = str(file)
        return file

    def doubleclick(self, event):
        file = self.files.curselection()
        file = self.files.get(file)
        if os.path.isdir(file):
            os.chdir(file)
        else:
            self.open_file(file)
        if file == "..":
            os.chdir("..")
        self.refresh()

    def context_menu(self, event):
        self.context.post(event.x_root, event.y_root)

    def hide_context_menu(self, event):
        self.context.unpost()


root = ttk.Window(themename="vapor")

app = APP(root)
style = ttk.Style()

app.root.mainloop()

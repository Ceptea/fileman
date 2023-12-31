import tkinter as tk
import os
import subprocess as sb
import tkinter.messagebox as tkmsg
from tkinter import simpledialog
from config import *

try:
    import ttkbootstrap as ttk

    isthemeable = 1
except ImportError:
    import tkinter.ttk as ttk

    isthemeable = 0


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
        self.context.add_command(label="Edit", command=self.edit_file)
        self.context.add_command(label="Rename", command=self.rename_file)
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

    def edit_file(self):
        file = self.get_file()
        if os.path.isfile(file):
            self.run_file(file, f"{text_editor} {file}", 0)

    def rename_file(self):
        file = self.get_file()
        if not file:
            return -1
        new_name = simpledialog.askstring("fileman", f"Rename {file} to ?")

        os.rename(file, new_name)
        self.refresh()

    def new_folder(self):
        new_folder = simpledialog.askstring(title="fileman", prompt="Create a folder.")
        if new_folder:
            os.mkdir(new_folder)
            self.refresh()

    def delete_file(self):
        file = self.get_file()
        if file == "..":
            return -1
        if os.path.exists(file):
            answer = tkmsg.askyesno(
                "fileman", f"Are you sure you want to delete {file}"
            )
            if answer:
                if os.path.isdir(file):
                    os.rmdir(file)
                else:
                    os.remove(file)
        self.refresh()

    def run_file(self, file, cmd, confirm=1):
        file = self.get_file()
        if confirm:
            answer = tkmsg.askyesno(
                "fileman", f"Are you sure you want to execute {file}"
            )
            if answer:
                sb.Popen(cmd, shell=1)
        else:
            sb.Popen(cmd, shell=1)

    def open_file(self, event=""):
        file = self.get_file()
        if not file:
            return 0
        if file == "..":
            os.chdir("..")
        match file_type(file):
            case ".txt":
                self.run_file(file, f"{text_editor} {file}", 0)
            case ".py":
                self.run_file(file, f"{terminal} {python} ./{file}")
            case ".pye":
                self.run_file(file, f"{terminal} ./{file}")
            case ".sh":
                self.run_file(file, f"{terminal} ./{file}")
            case _:
                if os.access(file, os.X_OK):
                    self.run_file(file, f"{terminal} ./{file}")
                else:
                    sb.Popen(f"xdg-open {file}", shell=1)
        self.refresh()

    def get_file(self):
        try:
            file = self.files.curselection()
            file = self.files.get(file)
            file = str(file)
            return file
        except:
            return 0

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


if isthemeable:
    root = ttk.Window(themename=theme)
else:
    root = tk.Tk()
app = APP(root)
style = ttk.Style()

app.root.mainloop()

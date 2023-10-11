import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import git
import threading

def clone_repository(url, destination, progress_bar, cancel_button):
    try:
        if not url.endswith(".git"):
            url += ".git"
        repo = git.Repo.clone_from(url, destination)
        show_message("Clonagem Concluída", f"Repositório clonado em: {destination}")
    except git.GitCommandError as e:
        show_message("Erro", f"Erro ao clonar o repositório:\n{e}")
    progress_bar.stop()
    cancel_button.config(state=tk.DISABLED)

def show_message(title, message):
    error_window = tk.Toplevel(root)
    error_window.title(title)
    error_text = tk.Text(error_window, wrap=tk.WORD, width=50, height=10)
    error_text.insert(tk.END, message)
    error_text.pack()
    ok_button = tk.Button(error_window, text="OK", command=error_window.destroy)
    ok_button.pack()

def start_clone():
    url_file = entry_url.get()
    destination_folder = entry_destination.get()
    progress_bar.start()
    cancel_button.config(state=tk.NORMAL)
    threading.Thread(target=clone_repositories, args=(url_file, destination_folder)).start()

def cancel_clone():
    progress_bar.stop()
    cancel_button.config(state=tk.DISABLED)

def clone_repositories(url_file, destination_folder):
    with open(url_file, 'r') as file:
        for line in file:
            url = line.strip()
            if not url.endswith(".git"):
                url += ".git"
            repo_name = url.split("/")[-1].replace(".git", "")
            repo_destination = os.path.join(destination_folder, repo_name)
            try:
                repo = git.Repo.clone_from(url, repo_destination)
            except git.GitCommandError as e:
                print(f"Erro ao clonar o repositório {url}:\n{e}")
    
    show_message("Clonagem Concluída", f"Repositórios clonados em: {destination_folder}")
    progress_bar.stop()
    cancel_button.config(state=tk.DISABLED)

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Arquivos de Texto", "*.txt")])
    entry_url.delete(0, tk.END)
    entry_url.insert(0, file_path)

def select_destination():
    folder_path = filedialog.askdirectory()
    entry_destination.delete(0, tk.END)
    entry_destination.insert(0, folder_path)

root = tk.Tk()
root.title("Clonador de Repositórios do GitHub")

label_url = tk.Label(root, text="Arquivo de Links:")
label_url.grid(row=0, column=0, padx=10, pady=5, sticky="w")
label_destination = tk.Label(root, text="Pasta de Destino:")
label_destination.grid(row=1, column=0, padx=10, pady=5, sticky="w")

entry_url = tk.Entry(root, width=50)
entry_url.grid(row=0, column=1, padx=10, pady=5)
entry_destination = tk.Entry(root, width=50)
entry_destination.grid(row=1, column=1, padx=10, pady=5)

browse_button_url = tk.Button(root, text="Navegar", command=select_file)
browse_button_url.grid(row=0, column=2, padx=5, pady=5)
browse_button_destination = tk.Button(root, text="Navegar", command=select_destination)
browse_button_destination.grid(row=1, column=2, padx=5, pady=5)

start_button = tk.Button(root, text="Iniciar Clonagem", command=start_clone)
start_button.grid(row=2, column=0, columnspan=3, pady=10)

cancel_button = tk.Button(root, text="Cancelar", command=cancel_clone, state=tk.DISABLED)
cancel_button.grid(row=3, column=0, columnspan=3, pady=5)

progress_bar = ttk.Progressbar(root, mode="indeterminate", length=300)
progress_bar.grid(row=4, column=0, columnspan=3, pady=10)

root.mainloop()

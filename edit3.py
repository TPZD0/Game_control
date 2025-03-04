import json
import tkinter as tk
from tkinter import messagebox, simpledialog

# Gesture Editor Program
# 1 indicates finger up, 0 indicates finger down

CONFIG_FILE = "gesture_config.json"
FINGER_LABELS = ["Thumb", "Index", "Middle", "Ring", "Pinky"]

def load_config():
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "gesture_map": {
                "w": [0, 1, 1, 0, 0],
                "s": [0, 1, 1, 1, 0],
                "a": [0, 0, 0, 0, 1],
                "d": [1, 0, 0, 0, 0],
                "space": [0, 0, 0, 0, 0]
            }
        }

def save_config():
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)

def update_gesture():
    selected_key = key_listbox.get(tk.ACTIVE)
    if not selected_key:
        messagebox.showerror("Error", "No key selected.")
        return
    try:
        new_array = [int(entries[i].get()) for i in range(5)]
        if all(value in [0, 1] for value in new_array):
            config["gesture_map"][selected_key] = new_array
            save_config()
            messagebox.showinfo("Success", f"Gesture for key '{selected_key}' updated successfully!")
        else:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Enter 0 or 1 for each finger.")

def refresh_list():
    key_listbox.delete(0, tk.END)
    for key in config["gesture_map"].keys():
        key_listbox.insert(tk.END, key)

def on_select(event):
    try:
        selected_key = key_listbox.get(key_listbox.curselection())
        if selected_key in config["gesture_map"]:
            values = config["gesture_map"][selected_key]
            for i in range(5):
                entries[i].delete(0, tk.END)
                entries[i].insert(0, str(values[i]))
            current_key_label.config(text=f"Editing Key: {selected_key}")
    except:
        pass

def add_key():
    new_key = simpledialog.askstring("Input", "Enter new key:")
    if new_key and new_key not in config["gesture_map"]:
        config["gesture_map"][new_key] = [0, 0, 0, 0, 0]
        refresh_list()
        save_config()
        messagebox.showinfo("Success", f"Key '{new_key}' added successfully!")
    else:
        messagebox.showerror("Error", "Invalid or duplicate key.")

def delete_key():
    selected_key = key_listbox.get(tk.ACTIVE)
    if selected_key in config["gesture_map"]:
        del config["gesture_map"][selected_key]
        refresh_list()
        save_config()
        current_key_label.config(text="Editing Key: None")
        messagebox.showinfo("Success", f"Key '{selected_key}' deleted successfully!")
    else:
        messagebox.showerror("Error", "No key selected or key does not exist.")

config = load_config()

root = tk.Tk()
root.title("Gesture Editor")

frame = tk.Frame(root)
frame.pack(pady=20)

key_listbox = tk.Listbox(frame, width=40, height=15, font=("Helvetica", 14))
key_listbox.pack(side=tk.LEFT, padx=20)
key_listbox.bind("<<ListboxSelect>>", on_select)
refresh_list()

entry_frame = tk.Frame(frame)
entry_frame.pack(padx=20)

entries = []
for label in FINGER_LABELS:
    row = tk.Frame(entry_frame)
    row.pack(fill=tk.X, pady=5)
    tk.Label(row, text=label, width=20, anchor='w', font=("Helvetica", 14)).pack(side=tk.LEFT)
    entry = tk.Entry(row, width=5, font=("Helvetica", 14))
    entry.pack(side=tk.RIGHT)
    entries.append(entry)

current_key_label = tk.Label(root, text="Editing Key: None", font=("Helvetica", 14))
current_key_label.pack(pady=10)

update_button = tk.Button(root, text="Update Gesture", command=update_gesture, font=("Helvetica", 14))
update_button.pack(pady=10)

add_key_button = tk.Button(root, text="Add Key", command=add_key, font=("Helvetica", 14))
add_key_button.pack(pady=10)

delete_button = tk.Button(root, text="Delete Key", command=delete_key, font=("Helvetica", 14))
delete_button.pack(pady=10)

root.mainloop()

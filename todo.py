import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog, ttk
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My To-Do List")
        self.root.geometry("500x600") # Adjusted size for better layout
        self.root.resizable(False, False) # Make window not resizable

        self.todo_file = "todo_list.txt"
        # Stores tasks as dictionaries: {'text': 'Task Name', 'completed': False}
        self.tasks = []

        self.load_tasks()
        self.create_widgets()

    def create_widgets(self):
        # --- Header ---
        header_frame = ttk.Frame(self.root, padding="10")
        header_frame.pack(fill="x")
        ttk.Label(header_frame, text="To-Do List", font=("Helvetica", 18, "bold")).pack(pady=5)

        # --- Task Entry ---
        entry_frame = ttk.Frame(self.root, padding="10")
        entry_frame.pack(fill="x")

        self.task_entry = ttk.Entry(entry_frame, width=40, font=("Helvetica", 12))
        self.task_entry.pack(side=tk.LEFT, expand=True, fill="x", padx=(0, 10))
        # Bind Enter key to add_task
        self.task_entry.bind("<Return>", self.add_task_event)

        self.add_button = ttk.Button(entry_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT)

        # --- Task List Display ---
        list_frame = ttk.Frame(self.root, padding="10")
        list_frame.pack(fill="both", expand=True)

        self.task_listbox = tk.Listbox(
            list_frame,
            font=("Helvetica", 12),
            selectmode=tk.SINGLE, # Only allow single selection
            height=15,
            bd=0, # Border width
            highlightthickness=0, # No highlight around selection
            activestyle='none' # No active style on hover
        )
        self.task_listbox.pack(side=tk.LEFT, fill="both", expand=True)

        # Scrollbar for the listbox
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.task_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.task_listbox.config(yscrollcommand=scrollbar.set)

        # --- Action Buttons ---
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill="x", pady=(0, 10))

        self.complete_button = ttk.Button(button_frame, text="Mark Complete", command=self.mark_complete)
        self.complete_button.pack(side=tk.LEFT, expand=True, padx=5)

        self.delete_button = ttk.Button(button_frame, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, expand=True, padx=5)

        self.update_button = ttk.Button(button_frame, text="Edit Task", command=self.edit_task)
        self.update_button.pack(side=tk.LEFT, expand=True, padx=5)

        self.clear_completed_button = ttk.Button(button_frame, text="Clear Completed", command=self.clear_completed)
        self.clear_completed_button.pack(side=tk.LEFT, expand=True, padx=5)

        # Initial display refresh
        self.refresh_task_display()

    def load_tasks(self):
        """Loads tasks from the todo_list.txt file."""
        if os.path.exists(self.todo_file):
            try:
                with open(self.todo_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("[X] "):
                            self.tasks.append({'text': line[4:], 'completed': True})
                        elif line: # Only add non-empty lines
                            self.tasks.append({'text': line, 'completed': False})
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load tasks: {e}")
        else:
            # Create the file if it doesn't exist
            try:
                with open(self.todo_file, "w", encoding="utf-8") as f:
                    pass # Just create an empty file
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create todo file: {e}")


    def save_tasks(self):
        """Saves current tasks to the todo_list.txt file."""
        try:
            with open(self.todo_file, "w", encoding="utf-8") as f:
                for task in self.tasks:
                    if task['completed']:
                        f.write(f"[X] {task['text']}\n")
                    else:
                        f.write(f"{task['text']}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {e}")

    def refresh_task_display(self):
        """Clears and repopulates the listbox with current tasks and their styles."""
        self.task_listbox.delete(0, tk.END)
        for i, task in enumerate(self.tasks):
            self.task_listbox.insert(tk.END, task['text'])
            if task['completed']:
                # Apply overstrike and foreground directly to the item by its index
                self.task_listbox.itemconfig(i, {"fg": "gray", "overstrike": True})
            else:
                self.task_listbox.itemconfig(i, {"fg": "black", "overstrike": False})

    def add_task_event(self, event=None):
        """Callback for adding a task (e.g., from Enter key press)."""
        self.add_task()

    def add_task(self):
        """Adds a new task from the entry field to the list."""
        task_text = self.task_entry.get().strip()
        if task_text:
            self.tasks.append({'text': task_text, 'completed': False})
            self.task_entry.delete(0, tk.END)
            self.refresh_task_display()
            self.save_tasks()
        else:
            messagebox.showwarning("Input Error", "Task cannot be empty!")

    def mark_complete(self):
        """Toggles the completion status of the selected task."""
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            # Toggle the 'completed' status
            self.tasks[selected_task_index]['completed'] = not self.tasks[selected_task_index]['completed']
            self.refresh_task_display()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to mark complete.")

    def delete_task(self):
        """Deletes the selected task from the list."""
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            del self.tasks[selected_task_index]
            self.refresh_task_display()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def edit_task(self):
        """Edits the text of the selected task."""
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            current_text = self.tasks[selected_task_index]['text']

            # Open a dialog to get the new task text
            new_text = simpledialog.askstring("Edit Task", "Edit the selected task:", initialvalue=current_text)

            # Check if user clicked OK and entered non-empty text
            if new_text is not None and new_text.strip():
                self.tasks[selected_task_index]['text'] = new_text.strip()
                self.refresh_task_display()
                self.save_tasks()
            elif new_text is not None: # User clicked OK but entered empty text
                messagebox.showwarning("Input Error", "Task cannot be empty!")

        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to edit.")


    def clear_completed(self):
        """Removes all tasks marked as completed from the list."""
        if not self.tasks:
            messagebox.showinfo("Info", "No tasks to clear.")
            return

        response = messagebox.askyesno(
            "Clear Completed Tasks",
            "Are you sure you want to clear all completed tasks?"
        )
        if response:
            # Create a new list containing only tasks that are NOT completed
            self.tasks = [task for task in self.tasks if not task['completed']]
            self.refresh_task_display()
            self.save_tasks()
            messagebox.showinfo("Success", "Completed tasks cleared.")


if __name__ == "__main__":
    # Create the main Tkinter window
    root = tk.Tk()
    # Instantiate and run the To-Do application
    app = TodoApp(root)
    root.mainloop()
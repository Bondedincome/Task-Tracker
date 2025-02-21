import cmd
import json
from datetime import datetime

TASK_FILE = "file.json"

class TaskTrackerCLI(cmd.Cmd):
    prompt = "task-cli> "

    def do_add(self, arg):
        """Add a new task: add "task description" """
        if not arg.strip(): # checks for empty strings so as not to have junk data
            print("You need to provide a task!")
            return

        prev_data = get_file(TASK_FILE)
        task_id = max([task["id"] for task in prev_data], default=0) + 1  # Ensure unique IDs
        task = {
            "id": task_id,
            "description": arg,
            "status": "todo",
            "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        prev_data.append(task)
        write_file(TASK_FILE, prev_data)
        print(f"Task added successfully (ID: {task_id})")

    def do_list(self, arg):
        """List tasks: list [all|done|todo|in-progress]"""
        status_filter = arg.strip().lower() if arg else "all"
        get_list(status_filter)

    def do_update(self, arg):
        """Update a task: update <task_id> "new description" """
        try:
            task_id, new_desc = arg.split(" ", 1)
            task_id = int(task_id)
        except ValueError:
            print("Invalid format! Use: update <task_id> \"new description\"")
            return

        prev_data = get_file(TASK_FILE)
        for task in prev_data:
            if task["id"] == task_id:
                task["description"] = new_desc
                task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                write_file(TASK_FILE, prev_data)
                print(f"Task {task_id} updated successfully.")
                return

        print(f"Task with ID {task_id} not found.")

    def do_delete(self, arg):
        """Delete a task: delete <task_id>"""
        try:
            task_id = int(arg)
        except ValueError:
            print("Invalid task ID!")
            return

        prev_data = get_file(TASK_FILE)
        updated_data = [task for task in prev_data if task["id"] != task_id]

        write_file(TASK_FILE, updated_data)
        print(f"Task {task_id} deleted successfully.")

    def do_mark_done(self, arg):
        """Mark a task as done: mark-done <task_id>"""
        self.mark_status(arg, "done")

    def do_mark_in_progress(self, arg):
        """Mark a task as in progress: mark-in-progress <task_id>"""
        self.mark_status(arg, "in-progress")

    def mark_status(self, task_id, status):
        """Helper function to change task status"""
        try:
            task_id = int(task_id)
        except ValueError:
            print("Invalid task ID!")
            return

        prev_data = get_file(TASK_FILE)
        for task in prev_data:
            if task["id"] == task_id:
                task["status"] = status
                task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                write_file(TASK_FILE, prev_data)
                print(f"Task {task_id} marked as {status}.")
                return

        print(f"Task with ID {task_id} not found.")

    def do_exit(self, arg):
        """Exit the Task Tracker CLI"""
        print("Goodbye!")
        return True
    
    def do_clear(self, arg):
        """Clear the screen"""
        print("\033c", end="") 
        print("Cleared the screen!")


def get_file(filename):
    """Read tasks from JSON file"""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return empty list if file doesn't exist or is corrupted


def write_file(filename, data):
    """Write tasks to JSON file"""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def get_list(status_filter="all"):
    """Display tasks based on status"""
    tasks = get_file(TASK_FILE)
    if not tasks:
        print("No tasks found.")
        return

    filtered_tasks = [task for task in tasks if status_filter == "all" or task["status"] == status_filter]

    if not filtered_tasks:
        print(f"No tasks with status: {status_filter}")
        return

    print(f"\n{'ID':<5}{'Status':<15}{'Description'}")
    print("=" * 50)
    for task in filtered_tasks:
        print(f"{task['id']:<5}{task['status']:<15}{task['description']}")
    print("\n")


if __name__ == "__main__":
    TaskTrackerCLI().cmdloop()
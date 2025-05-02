import json
import os
from datetime import datetime

# File to store the notes
NOTES_FILE = "notes.json"

# ---------------------- File Handling ---------------------- #


# Load notes from the JSON file
def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    try:
        with open(NOTES_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        print("Failed to load notes. The file might be corrupted or unreadable.")
        return []


# Save notes to the JSON file
def save_notes(notes):
    try:
        with open(NOTES_FILE, "w") as file:
            json.dump(notes, file, indent=4)
    except IOError as e:
        print(f"Error saving notes: {e}.")


# ---------------------- Note Display ---------------------- #


def display_matches(notes):
    for i, note in enumerate(notes, 1):
        print(f"\nMatch {i}")
        print(f"Title     : {note.get('title')}")
        print(f"Content   : {note.get('content')}")
        print(f"Timestamp : {note.get('timestamp')}")


# ---------------------- CRUD Operations ---------------------- #


# Add a new note
def add_note():
    print("\n--- Add New Note ---")
    title = input("Title   : ").strip()
    content = input("Content : ").strip()

    if not title or not content:
        print("Title and content cannot be empty.")
        return

    timestamp = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    note = {"title": title, "content": content, "timestamp": timestamp}

    notes = load_notes()
    notes.append(note)
    save_notes(notes)
    print("Note added successfully!")


# View all notes
def view_notes():
    print("\n--- All Notes ---")
    notes = load_notes()
    display_matches(notes=notes)


# Edit an existing note by title
def edit_note():
    print("\n--- Edit Note ---")
    title = input("Which note do you want to edit (title)? ").strip()

    notes = load_notes()

    for note in notes:
        if note.get("title", "").lower() == title.lower():
            print("Leave a field empty if you don't want to change it.")

            new_title = input("New title (optional): ").strip()
            new_content = input("New content (optional): ").strip()

            if new_title:
                note["title"] = new_title
            if new_content:
                note["content"] = new_content

            note["timestamp"] = datetime.now().strftime("%d-%m-%Y %I:%M %p")
            save_notes(notes)
            print("Note updated successfully.")
            return

    print(f"No note found with the title '{title}'.")


# Delete a note by title
def delete_note():
    print("\n--- Delete Note ---")
    title_to_delete = input("Enter the title of the note to delete: ").strip()

    notes = load_notes()
    if not notes:
        print("No notes found.")
        return

    updated_notes = [note for note in notes if note.get("title", "").lower() != title_to_delete.lower()]

    if len(updated_notes) == len(notes):
        print(f"No note found with title '{title_to_delete}'.")
    else:
        save_notes(updated_notes)
        print(f"Note titled '{title_to_delete}' deleted.")


# Search notes by keyword
def search_notes():
    print("\n--- Search Notes ---")
    keyword = input("Enter keyword to search: ").strip().lower()

    if not keyword:
        print("Keyword cannot be empty.")
        return

    notes = load_notes()
    matching_notes = [note for note in notes if keyword in note["title"].lower() or keyword in note["content"].lower()]

    if not matching_notes:
        print("No matching notes found.")
        return

    display_matches(notes=matching_notes)


# Remove empty note dictionaries (e.g., if a bad entry was saved)
def clean_notes():
    notes = load_notes()
    cleaned_notes = [note for note in notes if note and isinstance(note, dict)]
    if len(cleaned_notes) != len(notes):
        save_notes(cleaned_notes)
        print("Empty or invalid notes removed.")
    else:
        print("No empty notes found.")


# ---------------------- Menu ---------------------- #
def show_menu():
    options = {"1": add_note, "2": view_notes, "3": edit_note, "4": delete_note, "5": search_notes, "6": exit_program}

    while True:
        print("\n===📓 Notes Manager ===")
        print("1. Add Note")
        print("2. View All Notes")
        print("3. Edit Note")
        print("4. Delete Note")
        print("5. Search Notes")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()
        action = options.get(choice)
        if action:
            try:
                action()
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


def exit_program():
    print("Exiting Notes Manager... Goodbye!")
    exit()


# ---------------------- Entry Point ---------------------- #
if __name__ == "__main__":
    clean_notes()
    show_menu()

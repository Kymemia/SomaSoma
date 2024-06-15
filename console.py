#!/usr/bin/python3

"""This is the console module for our website"""


import json
import os
from datetime import datetime, timedelta


class Note:
    """This is a class that encapsulates an entire note."""
    def __init__(self, title, content):
        """Initializes title + content of a particular note."""
        self.title = title
        self.content = content

class NotesCommand:
    """This class contains features for the SomaSoma console"""
    def __init__(self):
        """Initializes the notes contained + load_notes feature"""
        self.notes = []
        self.load_notes()
        self.recycle_bin = []

    def create_note(self, title, content):
        """This method allows a user to create a note"""
        note = Note(title, content)
        self.notes.append(note)
        print(f"Note '{title}' created.")

    def edit_note(self, index, new_title, content):
        """This method allows a user to edit a note
        by accessing the following parameters listed
        in the brackets
        self => contains all of a user's notes
        index => unique position of the particular note to edit
        new_title => this is the title of the new edited note
                      (can still be the same title though)
        content => new data that'll ideally be inserted in the note"""
        try:
            note = self.notes[index - 1]
            note.title = new_title
            note.content = new_content
            print(f"Note '{new_title}' updated.")
        except IndexError:
            print("Note not found")

    def view_note_content(self, index):
        """This method allows a user to view a specific note's content"""
        try:
            note = self.notes[index - 1]
            print(f"Title: {note.title}\nContent: {note.content}")
        except IndexError:
            print("Note not found.")

    def view_notes(self):
        """This method allows a user to view all their notes"""
        for x, note in enumerate(self.notes, start=1):
            print(f"{x}. {note.title}")

    def save_notes(self):
        """This method allows a user to save all their notes"""
        with open('notes.json', 'w') as f:
            json.dump([note.__dict__ for note in self.notes], f)

    def delete_note(self, index):
        """This method allows a user to delete a single note.
        Note will be sent to the recycle bin for x number of days"""
        try:
            note = self.notes.pop(index - 1)
            delete_time = datetime.now()
            self.recycle_bin.append((note, delete_time))
            print(f"Note '{note.title}' moved to recycle bin.")
        except IndexError:
            print("Note not found")

    def load_notes(self):
        """This method allows a user to load their notes"""
        if os.path.exists('note.json'):
            with open('notes.json', 'r') as f:
                notes_data = json.load(f)
                self.notes = [Note(**note) for note in notes_data]

    def search_notes(self, keyword):
        """This method allows a user
        to search their notes based on a keyword"""
        results = [note for note in self.notes if keyword.lower() in note.title.lower() or keyword.lower() in note.content.lower()]
        for note in results:
            print(f"Title: {note.title}\nContent: {note.content}\n")

    def delete_all_notes(self):
        """This method allows a user to delete all their notes
         ~ Notes will be moved to the recycle bin"""
        confirmation = input("Are you sure you want to delete all notes? Notes will be moved to recycle bin. (y/n): ").strip().lower()

        if confirmation == 'y':
            for note in self.notes:
                delete_time = datetime.now()
                self.recycle_bin.append((note, delete_time))
            self.notes = []
            print("All notes moved to the recycle bin.")
        else:
            print("Doomsday deletion aborted.")

    def restore_note_from_recycle_bin(self, index):
        """This method allows a user to restore
        a single note from the recycle bin"""
        try:
            note, delete_time = self.recycle_bin.pop(index - 1)
            self.notes.append(note)
            print(f"Note '{note.title}' restored from recycle bin.")
        except IndexError:
            print("Deleted not not found in recycle bin.")

    def empty_recycle_bin(self):
        """This method allows a user
        to delete all the contents from their recycle bin"""
        current_time = datetime.now()
        for note, delete_time in self.recycle_bin[:]:
            if (current_time - delete_time) > timedelta(days=7):
                self.recycle_bin.remove((note, delete_time))
                print(f"Note '{note.title}' permanently deleted after 7 days.")

        confirmation = input("Are you sure you want to delete all notes? Notes will be permanently deleted. (y/n): ").strip().lower()
        if confirmation == 'y':
            notes_deleted = len(self.recycle_bin)
            self.recycle_bin.clear()
            print(f"note{'s' if notes_deleted != 1 else ''} permanently deleted.")
        else:
            print("Recycle bin emptying aborted")

    def view_recycle_bin_notes(self):
        """This method allows a user
        to view the deleted notes in the recycle bin"""
        if not self.recycle_bin:
            print("Recycle bin is empty.")
        else:
            for j, (note, delete_time) in enumerate(self.recycle_bin, start=1):
                print(f"{j} {note.title} (deleted on {delete_time})")
                

if __name__ == "__main__":
    app = NotesCommand()

    while True:
        print("\nWelcome to SomaSoma Console")
        print("1. Create Note")
        print("2. Edit Note")
        print("3. View Note Content")
        print("4. View all Notes")
        print("5. Search Notes")
        print("6. Delete a Note")
        print("7. Delete all Notes")
        print("8. View recycle bin notes")
        print("9. Restore note from recycle bin")
        print("10. Empty recycle bin")
        print("11. Save notes to file")
        print("0. Exit")


        choice = input("Choose an option (0-10): ").strip()

        if choice == '1':
            title = input("Enter note title: ")
            content = input("Enter note's content: ")
            app.create_note(title, content)
        elif choice == '2':
            index = int(input("Enter note index: "))
            new_title = input("Enter new title: ")
            new_content = input("Enter new content: ")
            app.edit_note(index, new_title, new_content)
        elif choice == '3':
            index = int(input("Enter note index: "))
            app.view_note_content(index)
        elif choice == '4':
            app.view_notes()
        elif choice == '5':
            keyword = input("Enter keyword to search notes: ")
            app.search_notes(keyword)
        elif choice == '6':
            index = int(input("Enter index of note to delete: "))
            app.delete_note(index)
        elif choice == '7':
            app.delete_all_notes()
        elif choice == '8':
            app.view_recycle_bin_notes()
        elif choice == '9':
            index = int(input("Enter index of note to restore from recycle bin: "))
            app.restore_note_from_recycle_bin(index)
        elif choice == '10':
            app.empty_recycle_bin()
        elif choice == '11':
            app.save_notes()
        elif choice == '0':
            print("Exiting SomaSoma Console. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 0 and 10.")

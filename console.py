#!/usr/bin/env python3

import pyrebase
import json
import tempfile
import os
import urllib.request
from datetime import datetime, timedelta

# Firebase configuration
firebaseConfig = {
    'apiKey': "AIzaSyAZbrMm0lHELEM0uTkEyoSTUk7rTfuVqHs",
    'authDomain': "fir-ologi.firebaseapp.com",
    'projectId': "fir-ologi",
    'storageBucket': "fir-ologi.appspot.com",
    'messagingSenderId': "691465790967",
    'appId': "1:691465790967:web:e60ce9f9078d96d2a2faf2",
    'databaseURL': "https://fir-ologi-default-rtdb.firebaseio.com",
    'measurementId': "G-MGB84Q7K2F"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)

# Firebase Authentication
auth = firebase.auth()

# Firebase Storage
storage = firebase.storage()

class Note:
    """This is a class that encapsulates an entire note."""
    def __init__(self, title, content, last_edited=None):
        """Initializes title + content of a particular note."""
        self.title = title
        self.content = content
        self.last_edited = last_edited or datetime.now().isoformat()


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
        self.notes.sort(key=lambda x: x.last_edited, reverse=True)
        print(f"Note '{title}' created.")

    def edit_note(self, index):
        """This method allows a user to edit a note"""
        try:
            note = self.notes[index - 1]
            with tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix=".tmp") as temp_file:
                temp_file.write(note.content)
                temp_file.flush()
                temp_file_name = temp_file.name

            editor = os.environ.get('EDITOR', 'vim')
            os.system(f'{editor} {temp_file_name}')

            with open(temp_file_name, 'r') as temp_file:
                new_content = temp_file.read()

            os.remove(temp_file_name)

            note.content = new_content
            note.last_edited = datetime.now().isoformat()
            self.notes.sort(key=lambda x: x.last_edited, reverse=True)
            print(f"Note '{note.title}' updated.")
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
        if os.path.exists('notes.json'):
            with open('notes.json', 'r') as f:
                notes_data = json.load(f)
                self.notes = [Note(**note) for note in notes_data]
                self.notes.sort(key=lambda x: x.last_edited, reverse=True)

    def search_notes(self, keyword):
        """This method allows a user to search their notes based on a keyword"""
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
        """This method allows a user to restore a single note from the recycle bin"""
        try:
            note, delete_time = self.recycle_bin.pop(index - 1)
            self.notes.append(note)
            self.notes.sort(key=lambda x: x.last_edited, reverse=True)
            print(f"Note '{note.title}' restored from recycle bin.")
        except IndexError:
            print("Deleted note not found in recycle bin.")

    def empty_recycle_bin(self):
        """This method allows a user to delete all the contents from their recycle bin"""
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
        """This method allows a user to view the deleted notes in their recycle bin"""
        if not self.recycle_bin:
            print("Recycle bin is empty.")
        else:
            for j, (note, delete_time) in enumerate(self.recycle_bin, start=1):
                print(f"{j} {note.title} (deleted on {delete_time})")

    def upload_note_to_firebase(self, filename, cloudfilename):
        """This method allows a user to upload a note to Firebase storage"""
        try:
            storage.child(cloudfilename).put(filename)
            print(f"File '{filename}' uploaded as '{cloudfilename}'.")
        except Exception as e:
            print(f"Error uploading file: {e}")

    def download_note_from_firebase(self, cloudfilename, localfilename):
        """This method allows a user to download a note from Firebase storage"""
        try:
            storage.child(cloudfilename).download(localfilename)
            print(f"File '{cloudfilename}' downloaded as '{localfilename}'.")
        except Exception as e:
            print(f"Error downloading file: {e}")

    def read_note_from_firebase(self, cloudfilename):
        """This method allows a user to read a note from Firebase storage"""
        try:
            url = storage.child(cloudfilename).get_url(None)
            f = urllib.request.urlopen(url).read()
            print(f"Content of '{cloudfilename}':\n{f.decode()}")
        except Exception as e:
            print(f"Error reading file: {e}")

# Function to log in user
def login_user(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print("Successfully logged in!")
        return user
    except Exception as e:
        print(f"Error logging in: {e}")
        return None

# Signup a new user
def signup_user(email, password, confirmpass):
    if password == confirmpass:
        try:
            auth.create_user_with_email_and_password(email, password)
            print("SomaSoma Account Creation Successful!")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    else:
        print("Passwords do not match. Try again.")
        return False

# Initial signup/login process
def user_authentication():
    print("Welcome to SomaSoma Console")
    while True:
        print("1. Sign up")
        print("2. Log in")
        choice = input("Choose an option (1-2): ").strip()
        
        if choice == '1':
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            confirmpass = input("Please confirm your password: ")
            if signup_user(email, password, confirmpass):
                return
        elif choice == '2':
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            if login_user(email, password):
                return
        else:
            print("Invalid choice. Please enter 1 or 2.")

def main_menu(app):
    while True:
        print("\nSomaSoma Console Menu")
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
        print("12. Upload note to Firebase storage")
        print("13. Download note from Firebase storage")
        print("14. Read note from Firebase storage")
        print("0. Exit")

        choice = input("Choose an option (0-14): ").strip()

        if choice == '1':
            title = input("Enter note title: ")
            content = input("Enter note content: ")
            app.create_note(title, content)
        elif choice == '2':
            index = int(input("Enter note index to edit: "))
            app.edit_note(index)
        elif choice == '3':
            index = int(input("Enter note index to view: "))
            app.view_note_content(index)
        elif choice == '4':
            app.view_notes()
        elif choice == '5':
            keyword = input("Enter keyword to search: ")
            app.search_notes(keyword)
        elif choice == '6':
            index = int(input("Enter note index to delete: "))
            app.delete_note(index)
        elif choice == '7':
            app.delete_all_notes()
        elif choice == '8':
            app.view_recycle_bin_notes()
        elif choice == '9':
            index = int(input("Enter index of note in recycle bin to restore: "))
            app.restore_note_from_recycle_bin(index)
        elif choice == '10':
            app.empty_recycle_bin()
        elif choice == '11':
            app.save_notes()
        elif choice == '12':
            filename = input("Enter filename to upload: ")
            cloudfilename = input("Enter cloud filename: ")
            app.upload_note_to_firebase(filename, cloudfilename)
        elif choice == '13':
            cloudfilename = input("Enter cloud filename to download: ")
            localfilename = input("Enter local filename: ")
            app.download_note_from_firebase(cloudfilename, localfilename)
        elif choice == '14':
            cloudfilename = input("Enter cloud filename to read: ")
            app.read_note_from_firebase(cloudfilename)
        elif choice == '0':
            print("Exiting SomaSoma Console. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 0 and 14.")

if __name__ == "__main__":
    app = NotesCommand()
    user_authentication()
    main_menu(app)

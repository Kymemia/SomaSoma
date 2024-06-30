#!/usr/bin/python3
"""This is a test for the create note feature"""
import unittest
from unittest import mock
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from console import NotesCommand, Note

class TestNotesCommand(unittest.TestCase):
    """test for the Create Note feature"""
    def setUp(self):
        """this method sets up a fresh instance
        of the NotesCommand class for each test"""
        self.notes_command = NotesCommand()

    def test_create_note_creates_note(self):
        """this method tests whether create_note successfully adds
        a note to the notes column."""
        title = "** Test_Note **"
        content = "We have lift off."
        self.notes_command.create_note(title, content)

        # To check whether the note was added
        self.assertEqual(len(self.notes_command.notes), 1)
        self.assertEqual(self.notes_command.notes[0].title, title)
        self.assertEqual(self.notes_command.notes[0].content, content)

    def test_create_note_sorts_note(self):
        """this method tests whether notes are sorted
        by last_edited in descending order"""
        old_note = "Gen I"
        old_content = "something something first note"
        new_note = "Gen II"
        new_content = "something something second note"

        # To create 2 notes with different timestamps
        self.notes_command.create_note(old_note, old_content)
        self.notes_command.notes[0].last_edited = (datetime.now() - timedelta(days=1)).isoformat()
        self.notes_command.create_note(new_note, new_content)
        

        # To check the order of notes created
        self.assertEqual(self.notes_command.notes[0].title, new_note)
        self.assertEqual(self.notes_command.notes[1].title, old_note)


    def test_create_note_prints_confirm(self):
        """this method prints the correct confirmation message"""
        title = "Sample Note<CM>"
        content = "something something confirm message"

        with mock.patch('builtins.print') as mocked_print:
            self.notes_command.create_note(title, content)
            mocked_print.assert_called_with(f"Note '{title}' created.")


if __name__ == "__main__":
    unittest.main()

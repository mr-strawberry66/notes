"""Classes to handle note creation, deletion, and restoration."""
from datetime import datetime
from dataclasses import dataclass
import re
from time import time

from colorama import Fore

from editor import edit

import inquirer

# from pandas import DataFrame


@dataclass(order=True)
class Note:
    """Class defining a note."""

    id: int
    created_at: int
    category: str
    title: str
    body: str
    tags: list
    due_date: str


class NewNote:
    """Class used to cast a dictionary into a Note."""

    def __init__(self, note):
        """
        Initialise the class.

        args:
            note: (dict)
                One dictionary formatted
                note to be cast into a new
                Note object.

        returns:
            A new note object.
        """
        self.note = note

    def dict_to_note(self) -> Note:
        """Convert a note from a dict into a Note object."""
        return Note(
            id=self.note["id"],
            created_at=self.note["created_at"],
            category=self.note["category"],
            title=self.note["title"],
            body=self.note["body"],
            tags=self.note["tags"],
            due_date=self.note["due_date"],
        )


class CreateNote:
    """Wrapper around note creation."""

    def __init__(self, categories: list = None, data: list = None) -> None:
        """
        Initialise the class.

        categories: (list)
            The options for aggregating
            your notes by.

        data: (list)
            A list of dicts storing
            your notes.
        """
        self.categories = categories or ["Personal", "Work"]
        self.data = data

    def _find_max_id(self):
        """Return the highest id in list of notes."""
        ids = [note.id for note in self.data]
        return max(ids) if ids else 0

    def _set_id(self):
        """
        Read list of notes and create an ID of max ID + 1.

        returns: (int)
            A suitable ID to
            use with a new note.
        """
        return self._find_max_id() + 1

    def _set_title(self):
        """Set the title for a note based on user input."""
        while True:
            title = input("Give your note a title: ")
            if not title:
                print(
                    f"\n{Fore.YELLOW}Please input a title for your note.{Fore.RESET}\n"
                )
                pass
            else:
                return title

    def _set_category(self):
        """Set the category of a note from user selection."""
        categories = [
            inquirer.List(
                "category",
                message="Select note category",
                choices=self.categories,
            )
        ]
        user_resp = inquirer.prompt(categories)
        return user_resp["category"]

    def _set_body(self):
        """Set the body of a note based on user input."""
        while True:
            body = (
                edit(contents="# Lines starting with a '#' will be ignored. ")
                .decode("utf-8")
                .strip()
            )
            if not body:
                print(
                    f"\n{Fore.YELLOW}Please input content for your note.{Fore.RESET}\n"
                )
                pass
            else:
                return re.sub(r"^#.*\n?", "", body, flags=re.MULTILINE)

    def _clean_tags(self, tags: str) -> list:
        """Parse a string of tags into a list."""
        return [tag.strip().lower() for tag in tags.split(",")]

    def _set_tags(self):
        """Set tags for a note."""
        tags = input("Enter tags, seperated by a comma: ")
        return self._clean_tags(tags=tags) if tags else []

    def _set_due_date(self):
        """Set the due date of a note based on user input."""
        while True:
            date = input("Set a due date in yyyy-mm-dd format (optional): ")
            if not date:
                return None
            else:
                try:
                    timestamp = datetime.strptime(date, "%Y-%m-%d")
                    return timestamp.strftime("%Y-%m-%d")
                except ValueError:
                    print(
                        f"\n{Fore.YELLOW}Date must be yyyy-mm-dd format{Fore.RESET}\n"
                    )
                    pass

    def create_note(self) -> Note:
        """Create a new note."""
        note = Note(
            id=self._set_id(),
            created_at=int(time()),
            category=self._set_category(),
            title=self._set_title(),
            body=self._set_body(),
            tags=self._set_tags(),
            due_date=self._set_due_date(),
        )
        return note


class UpdateNote:
    """
    Wrapper around locating and updating notes.

    args:
        data: (list)
            A list of dicts storing
            your notes.
    """

    def __init__(self, categories: list = None, data: list = None) -> None:
        """Initialise the class."""
        self.data = data
        self.create_note = CreateNote(categories=categories, data=self.data)

    def find_index(self, _id: int) -> int:
        """Return a note by a specified ID."""
        index = [self.data.index(row) for row in self.data if row.id == _id]
        return index[0] if isinstance(index, list) else index

    def _find_note(self, _id: int) -> dict:
        index = self.find_index(_id=_id)
        return self.data[index]

    def _update_field(self, _id: int, field: str) -> str:
        """
        Update a field in a specified note.

        args:
            _id: (int)
                The Id of the note
                to update.

            field: (str)
                The field to edit.

        returns:
            The string updated by the
            user for the specified field.
        """
        note = self._find_note(_id=_id)
        content = getattr(note, field)
        updated_content = edit(contents=content).decode("utf-8")
        return re.sub(r"^#.*\n?", "", updated_content, flags=re.MULTILINE)

    def _clean_tags(self, tag_string: str) -> list:
        """Take a string representation of a tag and parse as a list."""
        return [
            tag.strip().lower().replace("\n", "")
            for tag in tag_string.split(",")
            if tag.strip().replace("\n", "")
        ]

    def _update_tags(self, _id) -> list:
        """Update tags for a note."""
        tag_string = ""
        tags = self._find_note(_id=_id).tags
        for tag in tags:
            tag_string += f"{tag},"
        updated_tags = edit(contents=tag_string).decode("utf-8")
        return self._clean_tags(tag_string=updated_tags)

    def update_all(self, _id) -> dict:
        """Update all fields for a note."""
        note = self._find_note(_id=_id)
        note.category = self.create_note._set_category()
        note.title = self._update_field(_id=_id, field="title")
        note.body = self._update_field(_id=_id, field="body")
        note.tags = self._update_tags(_id=_id)
        note.due_date = self.create_note._set_due_date()
        return note

    def update_category(self, _id) -> dict:
        """Update the category for a note."""
        note = self._find_note(_id=_id)
        note.category = self.create_note._set_category()
        return note

    def update_title(self, _id) -> dict:
        """Update the title for a note."""
        note = self._find_note(_id=_id)
        note.title = self._update_field(_id=_id, field="title")
        return note

    def update_body(self, _id) -> dict:
        """Update the body for a note."""
        note = self._find_note(_id=_id)
        note.body = self._update_field(_id=_id, field="body")
        return note

    def update_tags(self, _id) -> dict:
        """Update the tags for a note."""
        note = self._find_note(_id=_id)
        note.tags = (self._update_tags(_id=_id),)
        return note

    def update_date(self, _id) -> dict:
        """Update the due date for a note."""
        note = self._find_note(_id=_id)
        note.due_date = self.create_note._set_due_date()
        return note


class DeleteNote:
    """
    Wrapper around locating and deleting notes.

    args:
        data: (list)
            A list of dicts storing
            your notes.
    """

    def __init__(self, data: list = None) -> None:
        """Initialise the class."""
        self.data = data

    def _find_note(self, _id: int) -> dict:
        """Return a note by a specified ID."""
        return [self.data.index(row) for row in self.data if row.id == _id]

    def find_index(self, _id) -> int:
        """Return the index of a row to delete."""
        while True:
            usr_input = input(f"Are you sure you want to delete note? {_id} y/n: ")
            if usr_input == "y":
                index = self._find_note(_id=_id)
                return index[0] if isinstance(index, list) else index
            elif usr_input == "n":
                return "Cancelling..."


class DisplayNote:
    """Wrapper around displaying notes to the end user."""

    def __init__(self, data: list = None) -> None:
        """
        Initialise the class.

        args:
            data: (list)
                A list of dicts storing
                your notes.
        """
        self.data = data

    def _test_due_date(self, due_date: str) -> Fore:
        """Return a colour based on how close a due date is."""
        if due_date:
            now = datetime.now()
            set_date = datetime.strptime(due_date, "%Y-%m-%d")
            time_diff = (set_date - now).days
            if time_diff >= 10:
                return Fore.CYAN
            elif time_diff < 10 and time_diff >= 5:
                return Fore.GREEN
            elif time_diff < 5 and time_diff >= 0:
                return Fore.YELLOW
            else:
                return Fore.RED
        else:
            return Fore.CYAN

    def list_all(self) -> None:
        """Display a summary of all notes."""
        try:
            for note in self.data:
                _id = note.id
                title = note.title
                _due_date = note.due_date
                colour = self._test_due_date(due_date=_due_date)
                due_date = _due_date or "Not Set"
                print(
                    f"\nId: {_id}\n"
                    f"Title: {title}\n"
                    f"Due Date: {colour}{due_date}{Fore.RESET}"
                )
        except TypeError:
            return "No notes found"

    def _find_note(self, _id: int) -> dict:
        """Return a note by a specified ID."""
        return [row for row in self.data if row.id == _id][0]

    def show_note(self, _id: int) -> None:
        """Display the full content of a specified note."""
        try:
            note = self._find_note(_id=_id)
            title = note.title
            body = note.body
            _due_date = note.due_date
            tags = note.tags
            colour = self._test_due_date(due_date=_due_date)
            due_date = _due_date or "Not Set"
            print(
                f"\nId: {_id}\n"
                f"Title: {title}\n"
                f"{body}\n\n"
                f"Due Date: {colour}{due_date}{Fore.RESET}\n"
                f"Tags: {tags}"
            )
        except TypeError:
            return "Note not found"

    def _aggregate(self, aggregation: str) -> list:
        return [note for note in self.data if note.category == aggregation]

    def list_aggregation(self, aggregation: str) -> None:
        """
        Display notes grouped by a specified category.

        args:
            aggregation: (str)
                The category of note
                to display.
        """
        for note in self._aggregate(aggregation=aggregation):
            _id = note.id
            title = note.title
            _due_date = note.due_date
            colour = self._test_due_date(due_date=_due_date)
            if _due_date:
                due_date = _due_date
            else:
                due_date = "Not Set"
            print(
                f"\nId: {_id}\n"
                f"Title: {title}\n"
                f"Due Date: {colour}{due_date}{Fore.RESET}"
            )

    def _find_tag(self, tag: str) -> list:
        return [row for row in self.data if tag in row.tags]

    def list_by_tag(self, tag: str) -> None:
        """List notes grouped by a tag."""
        notes = self._find_tag(tag=tag)
        if notes:
            for note in notes:
                _id = note.id
                title = note.title
                _due_date = note.due_date
                colour = self._test_due_date(due_date=_due_date)
                due_date = _due_date or "Not Set"
                print(
                    f"\nId: {_id}\n"
                    f"Title: {title}\n"
                    f"Due Date: {colour}{due_date}{Fore.RESET}"
                )

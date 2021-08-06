"""Classes to handle note creation, deletion, and restoration."""
from colorama import Fore
from datetime import datetime
from time import time
from pandas import DataFrame
import editor
import inquirer


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
        if not categories:
            self.categories = ["Personal", "Work"]
        else:
            self.categories = categories
        self.data = data

    def _find_max_id(self):
        """Return the highest id in list of notes."""
        _ids = []
        if self.data:
            for row in self.data:
                _ids.append(row["id"])
            return max(_ids)
        else:
            return 0

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
            body = editor.edit(contents="# Write your note on the next line: ").decode(
                "utf-8"
            )
            if not body:
                print(
                    f"\n{Fore.YELLOW}Please input content for your note.{Fore.RESET}\n"
                )
                pass
            else:
                return body.replace("# Write your note on the next line: ", "")

    def _clean_tags(self, tags: str) -> list:
        cleaned_tags = []
        for tag in tags.split(","):
            cleaned_tags.append(tag.strip().lower())
        return cleaned_tags

    def _set_tags(self):
        """Set tags for a note."""
        tags = input("Enter tags, seperated by a comma: ")
        if tags:
            return self._clean_tags(tags=tags)
        return []

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

    def create_note(self) -> dict:
        """Create a new note."""
        note = {
            "id": self._set_id(),
            "created_at": int(time()),
            "category": self._set_category(),
            "title": self._set_title(),
            "body": self._set_body(),
            "tags": self._set_tags(),
            "due_date": self._set_due_date(),
        }
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
        for row in self.data:
            if row["id"] == _id:
                return self.data.index(row) + 1

    def _find_note(self, _id: int) -> dict:
        index = self.find_index(_id=_id) - 1
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
        content = self._find_note(_id=_id)[field]
        updated_content = editor.edit(contents=content).decode("utf-8")
        return updated_content

    def _clean_tags(self, tag_string: str) -> list:
        """Take a string representation of a tag and parse as a list."""
        cleaned_tags = []
        tags = tag_string.split(",")
        for tag in tags:
            cleaned_tags.append(tag.strip().lower().replace("\n", ""))
        return cleaned_tags

    def _update_tags(self, _id) -> list:
        """Update tags for a note."""
        tag_string = ""
        tags = self._find_note(_id=_id)["tags"]
        for tag in tags:
            tag_string += f"{tag},"
        updated_tags = editor.edit(contents=tag_string).decode("utf-8")
        return self._clean_tags(tag_string=updated_tags)

    def update_all(self, _id) -> dict:
        """Update all fields for a note."""
        note = self._find_note(_id=_id)
        updated_note = {
            "id": note["id"],
            "created_at": note["created_at"],
            "category": self.create_note._set_category(),
            "title": self._update_field(_id=_id, field="title"),
            "body": self._update_field(_id=_id, field="body"),
            "tags": self._update_tags(_id=_id),
            "due_date": self.create_note._set_due_date(),
        }
        return updated_note

    def update_category(self, _id) -> dict:
        """Update the category for a note."""
        note = self._find_note(_id=_id)
        updated_note = {
            "id": note["id"],
            "created_at": note["created_at"],
            "category": self.create_note._set_category(),
            "title": note["title"],
            "body": note["body"],
            "tags": note["tags"],
            "due_date": note["due_date"],
        }
        return updated_note

    def update_title(self, _id) -> dict:
        """Update the title for a note."""
        note = self._find_note(_id=_id)
        updated_note = {
            "id": note["id"],
            "created_at": note["created_at"],
            "category": note["category"],
            "title": self._update_field(_id=_id, field="title"),
            "body": note["body"],
            "tags": note["tags"],
            "due_date": note["due_date"],
        }
        return updated_note

    def update_body(self, _id) -> dict:
        """Update the body for a note."""
        note = self._find_note(_id=_id)
        updated_note = {
            "id": note["id"],
            "created_at": note["created_at"],
            "category": note["category"],
            "title": note["title"],
            "body": self._update_field(_id=_id, field="body"),
            "tags": note["tags"],
            "due_date": note["due_date"],
        }
        return updated_note

    def update_tags(self, _id) -> dict:
        """Update the tags for a note."""
        note = self._find_note(_id=_id)
        updated_note = {
            "id": note["id"],
            "created_at": note["created_at"],
            "category": note["category"],
            "title": note["title"],
            "body": note["body"],
            "tags": self._update_tags(_id=_id),
            "due_date": note["due_date"],
        }
        return updated_note

    def update_date(self, _id) -> dict:
        """Update the due date for a note."""
        note = self._find_note(_id=_id)
        updated_note = {
            "id": note["id"],
            "created_at": note["created_at"],
            "category": note["category"],
            "title": note["title"],
            "body": note["body"],
            "tags": note["tags"],
            "due_date": self.create_note._set_due_date(),
        }
        return updated_note


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
        for row in self.data:
            if row["id"] == _id:
                return self.data.index(row) + 1

    def find_index(self, _id) -> int:
        """Return the index of a row to delete."""
        while True:
            usr_input = input(f"Are you sure you want to delete note? {_id} y/n: ")
            if usr_input == "y":
                return self._find_note(_id=_id)
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
                _id = note["id"]
                title = note["title"]
                _due_date = note["due_date"]
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
        except TypeError:
            return "No notes found"

    def _find_note(self, _id: int) -> dict:
        """Return a note by a specified ID."""
        for row in self.data:
            if row["id"] == _id:
                return row

    def show_note(self, _id: int) -> None:
        """Display the full content of a specified note."""
        try:
            note = self._find_note(_id=_id)
            title = note["title"]
            body = note["body"]
            _due_date = note["due_date"]
            tags = note["tags"]
            colour = self._test_due_date(due_date=_due_date)
            if _due_date:
                due_date = _due_date
            else:
                due_date = "Not Set"
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
        data = DataFrame(self.data)
        data = data[data["category"] == aggregation]
        return data.to_dict("records")

    def list_aggregation(self, aggregation: str) -> None:
        """
        Display notes grouped by a specified category.

        args:
            aggregation: (str)
                The category of note
                to display.
        """
        for note in self._aggregate(aggregation=aggregation):
            _id = note["id"]
            title = note["title"]
            _due_date = note["due_date"]
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
        matched_rows = []
        if self.data:
            for row in self.data:
                for _tag in row["tags"]:
                    if _tag == tag:
                        matched_rows.append(row)
            return matched_rows

    def list_by_tag(self, tag: str) -> None:
        for note in self._find_tag(tag=tag):
            _id = note["id"]
            title = note["title"]
            _due_date = note["due_date"]
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

"""Classes to handle note creation, deletion, and restoration."""
from colorama import Fore
from datetime import datetime
import inquirer


class CreateNote:
    """Wrapper around note creation"""

    def __init__(self, categories: list = None, data: list = None) -> None:
        """Initialise the class."""
        if not categories:
            self.categories = ["Personal", "Work"]
        else:
            self.categories = categories
        self.data = data

    def _find_max_id(self):
        """Return the highest id in list of notes."""
        _ids = []
        for row in self.data:
            _ids.append(row["id"])
        return max(_ids)

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
            body = input("Write your note: ")
            if not body:
                print(
                    f"\n{Fore.YELLOW}Please input content for your note.{Fore.RESET}\n"
                )
                pass
            else:
                return body

    def _set_due_date(self):
        """."""
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

    def create_note(self):
        note = {
            "id": self._set_id(),
            "category": self._set_category(),
            "title": self._set_title(),
            "body": self._set_body(),
            "due_date": self._set_due_date(),
        }
        return note

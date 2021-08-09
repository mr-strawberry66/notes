"""Wrapper around all top-level functions for notes handling."""
from sk_notes.local_handler import LocalHandler
from sk_notes.note_handler import CreateNote, DeleteNote, DisplayNote, UpdateNote


class Notes:
    """Wrapper around storing and displaying notes."""

    def __init__(self, categories: list) -> None:
        """
        Initialise the class.

        args:
            categories: (list)
                A list of user defined
                categories.
        """
        self.categories = categories
        self.local = LocalHandler()
        self.data = self.local.read_notes()
        self.create_note = CreateNote(categories=categories, data=self.data)
        self.delete_note = DeleteNote(data=self.data)
        self.display_note = DisplayNote(data=self.data)
        self.update_note = UpdateNote(categories=categories, data=self.data)

    def notes(self) -> str:
        """Display all notes."""
        return self.display_note.list_all()

    def personal(self) -> str:
        """Display a summary of notes categorised as personal."""
        return self.display_note.list_aggregation(aggregation="Personal")

    def work(self) -> str:
        """Display a summary of notes categorised as work."""
        return self.display_note.list_aggregation(aggregation="Work")

    def group(self, aggregation: str) -> str:
        """Display a summary of notes by a specified aggregation."""
        return self.display_note.list_aggregation(aggregation=aggregation)

    def tag(self, tag: str) -> str:
        """
        Display a summary of notes aggregated by a tag.

        args:
            tag: (str)
                The tag to search
                notes for.
        """
        return self.display_note.list_by_tag(tag=tag.lower().strip())

    def note(self, _id: int) -> str:
        """
        Display the content of a note called by note Id.

        args:
            _id: (int)
                The ID of the note you want
                to display the full content
                of. This can be obtained by
                running notes.show_all().
        """
        return self.display_note.show_note(_id=_id)

    def new(self) -> None:
        """Write a new note."""
        note = self.create_note.create_note()
        self.data.append(note)

    def save(self) -> str:
        """Store notes locally and optionally in Cloud Storage."""
        return self.local.write_notes(data=self.data)

    def delete(self, _id: int) -> str:
        """Delete a note by specified Id."""
        index = self.delete_note.find_index(_id=_id)
        if index:
            if isinstance(index, int):
                self.data.pop(index - 1)
                return f"Note {_id} has been deleted"
            else:
                print(index)
        else:
            return "Note not found"

    def update(self, _id: int) -> str:
        """Update a note specified by Id."""
        index = self.update_note.find_index(_id=_id)
        if index:
            if isinstance(index, int):
                self.data.append(self.update_note.update_all(_id=_id))
                self.data.pop(index - 1)
                return f"Note {_id} has been updated"
            else:
                print(index)
        else:
            return "Note not found"

    def update_category(self, _id: int) -> str:
        """Update a note specified by Id."""
        index = self.update_note.find_index(_id=_id)
        if index:
            if isinstance(index, int):
                self.data.append(self.update_note.update_category(_id=_id))
                self.data.pop(index - 1)
                return f"Note {_id} has been updated"
            else:
                print(index)
        else:
            return "Note not found"

    def update_title(self, _id: int) -> str:
        """Update a note specified by Id."""
        index = self.update_note.find_index(_id=_id)
        if index:
            if isinstance(index, int):
                self.data.append(self.update_note.update_title(_id=_id))
                self.data.pop(index - 1)
                return f"Note {_id} has been updated"
            else:
                print(index)
        else:
            return "Note not found"

    def update_body(self, _id: int) -> str:
        """Update a note specified by Id."""
        index = self.update_note.find_index(_id=_id)
        if index:
            if isinstance(index, int):
                self.data.append(self.update_note.update_body(_id=_id))
                self.data.pop(index - 1)
                return f"Note {_id} has been updated"
            else:
                print(index)
        else:
            return "Note not found"

    def update_tags(self, _id: int) -> str:
        """Update a note specified by Id."""
        index = self.update_note.find_index(_id=_id)
        if index:
            if isinstance(index, int):
                self.data.append(self.update_note.update_tags(_id=_id))
                self.data.pop(index - 1)
                return f"Note {_id} has been updated"
            else:
                print(index)
        else:
            return "Note not found"

    def update_date(self, _id: int) -> str:
        """Update a note specified by Id."""
        index = self.update_note.find_index(_id=_id)
        if index:
            if isinstance(index, int):
                self.data.append(self.update_note.update_date(_id=_id))
                self.data.pop(index - 1)
                return f"Note {_id} has been updated"
            else:
                print(index)
        else:
            return "Note not found"

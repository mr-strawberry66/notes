"""Wrapper around all top-level functions for notes handling."""
from sk_notes.local_handler import LocalHandler
from sk_notes.note_handler import CreateNote, DeleteNote, DisplayNote, UpdateNote


class Notes:
    """Wrapper around storing and displaying notes."""

    def __init__(self) -> None:
        """Initialise the class."""
        self.local = LocalHandler()
        self.data = self.local.read_notes()
        self.create = CreateNote(data=self.data)
        self.delete = DeleteNote(data=self.data)
        self.display = DisplayNote(data=self.data)
        self.update = UpdateNote(data=self.data)

    def notes(self) -> str:
        """Display all notes."""
        return self.display.list_all()

    def personal(self) -> str:
        """Display a summary of notes categorised as personal."""
        return self.display.list_aggregation(aggregation="Personal")

    def work(self) -> str:
        """Display a summary of notes categorised as work."""
        return self.display.list_aggregation(aggregation="Work")

    def tag(self, tag: str) -> str:
        """
        Display a summary of notes aggregated by a tag.

        args:
            tag: (str)
                The tag to search
                notes for.
        """
        return self.display.list_by_tag(tag=tag.lower().strip())

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
        return self.display.show_note(_id=_id)

    def new(self) -> None:
        """Write a new note."""
        note = self.create.create_note()
        self.data.append(note)

    def save(self) -> str:
        """Store notes locally and optionally in Cloud Storage."""
        return self.local.write_notes(data=self.data)

    def delete(self, _id: int) -> str:
        """Delete a note by specified Id."""
        note_pos = self.delete.find_index(_id=_id)
        if note_pos:
            if isinstance(note_pos, int):
                self.data.pop(note_pos - 1)
                return f"Note {_id} has been deleted"
            else:
                print(note_pos)
        else:
            return "Note not found"

    def update(self, _id: int) -> str:
        """Update a note specified by Id."""
        return self.update.update_note(_id=_id)

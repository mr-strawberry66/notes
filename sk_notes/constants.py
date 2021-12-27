"""Module to hold project-wide constants."""
from datetime import datetime
from time import time

EXAMPLE_NOTE = [
    {
        "id": 1,
        "category": "Example",
        "title": "This is an example note.",
        "body": (
            "This is an example of a note. "
            "The category field is used to filter "
            "and group by notes. Examples of this "
            "could be 'Work', or 'Personal', which "
            "would allow you to seperate your notes"
            "from work, and from your personal life. "
            "This field IS case sensitive. \nThe "
            "title field is used to give a brief summary "
            "of the note, allowing you to understand the "
            "contents of the note from a glance. A title "
            "must be provided. \nThe description is the"
            "of your note. \nThe complete_by field is "
            "used to set a date to complete the task in "
            "note by, if applicable. Notes will be sorted "
            "by how long you have left to do the task, "
            "shortest amount of time, to longest."
        ),
        "created_at": int(time()),
        "due_date": datetime.now().strftime("%Y-%m-%d"),
        "tags": ["example", "test"],
    }
]

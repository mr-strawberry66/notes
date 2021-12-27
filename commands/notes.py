"""Commands for notes cli."""
import click
from sk_notes import Notes

NOTES = Notes()


@click.command()
@click.option(
    "-i",
    "--id",
    "_id",
    type=int,
    help="The ID of a specific note to display.",
    default=lambda: None,
)
def ls(_id: int):
    """Display all notes."""
    if _id:
        NOTES.note(_id)
    else:
        NOTES.notes()


@click.group()
def find():
    """List notes that match a specified tag or aggregation."""


@find.command()
@click.option(
    "-t",
    "--tag",
    type=str,
    help="A tag to search for.",
)
def tag(tag: str):
    """Find notes by a tag."""
    if tag:
        NOTES.tag(tag=tag)


@find.command()
@click.option("-a", "--aggregation", type=str, help="The aggregation to search for.")
def group(aggregation: str):
    """Find notes by an aggregation."""
    if aggregation:
        NOTES.aggregate(aggregation=aggregation)


@click.command()
def new():
    """Create a new note."""
    NOTES.new()
    NOTES.save()


@click.command()
@click.option(
    "-i",
    "--id",
    "_id",
    type=int,
    help="The ID of the note to delete.",
)
def delete(_id: int):
    """Delete an existing note."""
    NOTES.delete(_id)
    NOTES.save()


@click.group()
def update():
    """Update existing notes."""


@update.command()
@click.option(
    "-i",
    "--id",
    "_id",
    type=int,
    help="The ID of the note to update.",
)
def note(_id: int):
    """Update the entirety of a note."""
    NOTES.update(_id)
    NOTES.save()


@update.command()
@click.option(
    "-i",
    "--id",
    "_id",
    type=int,
    help="The ID of the note to update.",
)
def category(_id: int):
    """Update the category of a note."""
    NOTES.update_category(_id)
    NOTES.save()


@update.command()
@click.option(
    "-i",
    "--id",
    "_id",
    type=int,
    help="The ID of the note to update.",
)
def title(_id: int):
    """Update the title of a note."""
    NOTES.update_title(_id)
    NOTES.save()


@update.command()
@click.option(
    "-i",
    "--id",
    "_id",
    type=int,
    help="The ID of the note to update.",
)
def body(_id: int):
    """Update the content of a note."""
    NOTES.update_body(_id)
    NOTES.save()


@update.command()
@click.option(
    "-i",
    "--id",
    "_id",
    type=int,
    help="The ID of the note to update.",
)
def tags(_id: int):
    """Update the tags associated with the note."""
    NOTES.update_tags(_id)
    NOTES.save()


@update.command()
@click.option(
    "-i",
    "--id",
    "_id",
    type=int,
    help="The ID of the note to update.",
)
def date(_id: int):
    """Update the due date on the note."""
    NOTES.update_date(_id)
    NOTES.save()

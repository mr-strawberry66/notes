"""A placeholder file to execute code used to test."""
from sk_notes import BigQueryOperations, LocalHandler, CreateNote
from pyfiglet import Figlet
from colorama import Fore


def main():
    """Execute code for testing."""
    f = Figlet(font="slant")
    print(f.renderText("Notes"))
    # bq_ops = BigQueryOperations(
    #     table="test_notes",
    # )

    # print(bq_ops.read_notes())

    local_ops = LocalHandler()
    read_notes = local_ops.read_notes()

    note = CreateNote(data=read_notes)

    read_notes.append(note.create_note())

    write = local_ops.write_notes(data=read_notes)
    print(write)


if __name__ == "__main__":
    main()

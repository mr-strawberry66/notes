"""Wrapper around the REPL."""
from sk_notes.note_handler import UpdateNote
from sk_notes import Notes
from pyfiglet import Figlet
import IPython


def main():
    """Initialise and execute the REPL."""
    figlet = Figlet(font="slant")
    notes = Notes()
    test = UpdateNote(data="Froop")

    header = figlet.renderText("Notes")
    scope_vars = {"notes": notes, "test": test}

    print(header)
    IPython.start_ipython(argv=[], user_ns=scope_vars)


if __name__ == "__main__":
    main()

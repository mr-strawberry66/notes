"""Wrapper around the REPL."""
from sk_notes import Notes
from pyfiglet import Figlet
import IPython


def main():
    """Initialise and execute the REPL."""
    figlet = Figlet(font="slant")
    notes = Notes()

    header = figlet.renderText("Notes")
    scope_vars = {"notes": notes}

    print(header)
    IPython.start_ipython(argv=[], user_ns=scope_vars)


if __name__ == "__main__":
    main()

"""Classes to handle interactions with local storage."""
import json
import os
import re
from time import time

import numpy

from sk_notes.constants import EXAMPLE_NOTE


class LocalHandler:
    """Wrapper around local storage operations."""

    def __init__(self, directory: str = None) -> None:
        """Initialise the class."""
        if not directory:
            self.directory = ".notes_storage"
        else:
            self.directory = directory
        self.file_prefix = "local_stored_notes"

    def _set_local_storage(self) -> str:
        """Create local storage directory if not exists."""
        storage_exists = self._test_for_local_directory()
        if storage_exists:
            return self.directory
        else:
            self._create_local_directory()
            return self.directory

    def _test_for_local_directory(self) -> bool:
        """Return true if local directory exists."""
        exists = os.path.isdir(self.directory)
        return exists

    def _create_local_directory(self) -> bool:
        """
        Create a directory to store notes locally.

        Return True if directory was created or
        False if the directory exists.
        """
        try:
            os.mkdir(self.directory)
            return True
        except FileExistsError:
            return False
        except Exception as err:
            raise Exception(err)

    def _set_outfile_path(self) -> str:
        """Return a file path to write notes to."""
        directory = self._set_local_storage()
        now = int(time())
        file_path = f"{directory}/{self.file_prefix}-{now}.json"
        return file_path

    def _clean_note_file_names(self, notes: list) -> list:
        """
        Extract the date from historical filenames.

        args:
            notes: (list)
                A list of file names
                to extract the date from.

        returns: (list)
            A list of datetimes
            extracted from file names.
        """
        cleaned_notes = []
        for note in notes:
            cleaned_note = re.search(".*([0-9]{10}).json", note).group(1)
            cleaned_notes.append(int(cleaned_note))
        return cleaned_notes

    def _find_nearest_date(self, dates: list, date: int) -> list:
        """
        Take a list of timestamps and find closest to specified timestamp.

        args:
            dates: (list)
                A list of timestamps
                to test for the most
                recent date.

            date: (int)
                A timestamp used as
                a reference to find
                the closest date to.
        """
        dates = numpy.asarray(dates)
        index = (numpy.abs(dates - date)).argmin()
        return dates[index]

    def write_notes(self, data: list) -> str:
        """
        Write notes to a file locally.

        args:
            data: (list)
                A list of dictionaries
                containing notes to
                store locally.

        returns: (str)
            A message confirming the write
            location of the notes.

        """
        file_path = self._set_outfile_path()
        with open(file_path, mode="w") as file:
            json.dump(data, file)
        return f"Notes written to {file_path}"

    def _find_most_recent_file_timestamp(self) -> int:
        """
        Get the most recent timestamp from a list of file names.

        returns: (int)
            The most recent timestamp.
        """
        try:
            stored_notes = os.listdir(self.directory)
            current_time = int(time())
            dates = self._clean_note_file_names(stored_notes)
            date = self._find_nearest_date(dates=dates, date=current_time)
            return date
        except FileNotFoundError:
            return False
        except ValueError:
            return False
        except Exception as err:
            raise Exception(err)

    def read_notes(self) -> list:
        """
        Read notes from most recent local file.

        returns: (list)
            A list of dictionaries containing
            notes if historical notes are found,
            or the example note.
        """
        file_time = self._find_most_recent_file_timestamp()
        if file_time:
            file = f"{self.directory}/{self.file_prefix}-{file_time}.json"
            with open(file, "r") as notes_file:
                notes = json.load(notes_file)
            return notes
        else:
            return EXAMPLE_NOTE

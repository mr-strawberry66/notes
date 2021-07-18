"""Classes to handle interractions with BigQuery."""
import os
from google.cloud import bigquery

class BigQueryOperations:
    """Wrapper around all BigQuery operations."""

    def __init__(
        self,
        gcp_project_id: str=None,
        dataset: str=None,
        table: str=None,
        environment: str=None,
    ):
        """Initialise the class."""
        if not gcp_project_id:
            try:
                self.gcp_project_id = os.environ["GCP_PROJECT_ID"]
            except KeyError:
                raise ValueError(
                    "Please provide a GCP Project Id."
                )
        else:
            self.gcp_project_id=gcp_project_id

        if not dataset:
            try:
                self.dataset_suffix = os.environ["DATASET"]
            except KeyError:
                raise ValueError(
                    "Please provide a dataset to write your notes to."
                )
        else:
            self.dataset_suffix = self.dataset

        if not table:
            try:
                self.table = os.environ["TABLE"]
            except KeyError:
                self.table = "notes"
        else:
            self.table = table

        if not environment:
            try:
                self.environment = os.environ["ENVIRONMENT"]
            except KeyError:
                self.environment = "dev"
        else:
            self.environment=environment

        self.client = bigquery.Client(project=self.gcp_project_id)
        self.dataset = f"{self.environment}_{self.dataset_suffix}"

    def test_for_notes_table(self):
        """Check to see if a table exists in the current BigQuery environment."""
        pass

    def create_notes_table(self):
        """Create a table in BigQuery to store notes in."""
        pass

    def read_notes(self):
        """Read existing notes from BigQuery. """
        return self.client

    def write_notes(self):
        """Write new and updated notes to BigQuery."""
        return self.client

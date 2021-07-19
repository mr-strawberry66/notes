"""Classes to handle interractions with BigQuery."""
from google.api_core import exceptions as google_exceptions
from google.cloud import bigquery
from pandas import DataFrame
import pandas_gbq
from .constants import EXAMPLE_NOTE
from .settings import BigQueryCredentials


class BigQueryOperations:
    """Wrapper around all BigQuery operations."""

    def __init__(
        self,
        gcp_project_id: str = None,
        dataset: str = None,
        table: str = None,
        environment: str = None,
    ) -> None:
        """Initialise the class."""
        bq_credentials = BigQueryCredentials(
            gcp_project_id=gcp_project_id,
            dataset=dataset,
            table=table,
            environment=environment,
        )
        self.gcp_project_id = bq_credentials.set_gcp_project_id()
        self.dataset_suffix = bq_credentials.set_dataset_suffix()
        self.table = bq_credentials.set_table()
        self.environment = bq_credentials.set_environment()
        self.client = bigquery.Client(project=self.gcp_project_id)
        self.dataset = f"{self.environment}_{self.dataset_suffix}"
        self.get_notes_query = f"""
            SELECT
                *
            FROM
                `{self.gcp_project_id}.{self.dataset}.{self.table}`
        """

    def create_notes_table(self) -> None:
        """Create a table in BigQuery to store notes in."""
        dataframe = DataFrame(EXAMPLE_NOTE)
        try:
            dataframe.to_gbq(
                destination_table=f"{self.dataset}.{self.table}",
                project_id=self.gcp_project_id,
                chunksize=None,
                if_exists="fail",
            )
            return EXAMPLE_NOTE
        except pandas_gbq.gbq.TableCreationError as pd_err:
            raise Exception(pd_err)
        except Exception as err:
            raise Exception(err)

    def read_notes(self) -> list:
        """
        Read existing notes from BigQuery.

        returns: (list)
            A list of dictionaries
            storing previously written
            notes.

        excepts (google.api_core.exceptions.NotFound):
            If the table doesn't exist,
            create a new table and
            return the default note
            stored in constants.py.

        excepts (Exception):
            Raise a generic exception
            if something else goes
            wrong with the query.
        """
        try:
            bqclient_result = (
                self.client.query(
                    self.get_notes_query,
                )
                .result()
                .to_dataframe()
                .to_dict("records")
            )
            return bqclient_result
        except google_exceptions.NotFound:
            print("The table or dataset could not be found. Creating now")
            return self.create_notes_table()
        except Exception as err:
            raise Exception(err)

    def write_notes(self) -> str:
        """Write new and updated notes to BigQuery."""
        return self.client

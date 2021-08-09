"""Classes to house project wide generic operations."""
import os
import yaml


class BigQueryCredentials:
    """Wrapper around BigQuery credentials."""

    def __init__(
        self,
        gcp_project_id: str = None,
        dataset: str = None,
        table: str = None,
        environment: str = None,
    ) -> None:
        """Initialise the class."""
        self.gcp_project_id = gcp_project_id
        self.dataset = dataset
        self.table = table
        self.environment = environment

    def set_gcp_project_id(self) -> str:
        """
        Return a GCP Project Id.

        returns: (str)
            A string representing the
            Id for the GCP Project to
            write notes to.

        excepts: (KeyError)
            Raises a ValueError if
            no Id is provided, either
            through the environment
            or explicitly.
        """
        if not self.gcp_project_id:
            try:
                return os.environ["GCP_PROJECT_ID"]
            except KeyError:
                raise ValueError("Please provide a GCP Project Id.")
        else:
            return self.gcp_project_id

    def set_dataset_suffix(self) -> str:
        """
        Return a BigQuery Dataset Id suffix.

        This will later be combined with an
        environment to form a full dataset
        Id.

        returns: (str)
            A string representing the
            suffix for a Dataset to
            write notes into.

        excepts: (KeyError)
            Raises a ValueError if
            no suffix is provided,
            either through the
            environment or explicitly.
        """
        if not self.dataset:
            try:
                return os.environ["DATASET"]
            except KeyError:
                raise ValueError("Please provide a dataset to write your notes to.")
        else:
            return self.dataset

    def set_table(self) -> str:
        """
        Return a BigQuery Table Id.

        returns: (str)
            A string representing a
            BigQuery table Id to
            write notes to.

        excepts: (KeyError)
            Returns "notes" as a
            default if no table Id
            is provided either in the
            environment or explicitly.
        """
        if not self.table:
            try:
                return os.environ["TABLE"]
            except KeyError:
                return "notes"
        else:
            return self.table

    def set_environment(self) -> str:
        """
        Return a runtime environment.

        This is used to specify whether
        the code should be run in a
        development environment, or in
        production.

        returns: (str)
            A string representing a
            runtime environment execute
            the code in.

        excepts: (KeyError)
            Returns "dev" as a
            default if no runtime
            environment is provided.
        """
        if not self.environment:
            try:
                return os.environ["ENVIRONMENT"]
            except KeyError:
                return "dev"
        else:
            return self.environment


class Config:
    """Class used to load settings.yml file."""

    def __init__(self, settings_file: str) -> None:
        """Initialise the class.

        args:
            settings_file: (str)
                The path to the yaml
                settings file used to
        """
        if settings_file:
            self.settings_file = settings_file
        else:
            self.settings_file = "settings.yml"

    def settings(self) -> None:
        """Load settings.yml into memory."""
        with open(self.settings_file, "r") as file:
            try:
                return yaml.safe_load(file)
            except yaml.YAMLError as err:
                return err
            except FileNotFoundError:
                return None


class SetUp:
    """Class used to extract user defined settings."""

    def __init__(self) -> None:
        """Initialise the class."""
        self.config = Config(settings_file="settings.yml")
        self.settings = self.config.settings()

    def aggregations(self) -> list:
        """Return user defined aggregations."""
        return self.settings.get("aggregations", None)

    def gcp_credentials(self) -> str:
        """Expose GCP credentials path to the environment."""
        gcp_creds = self.settings.get("gcp_credentials_path", None)
        if gcp_creds:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_creds
            return gcp_creds

    def gcp_project_id(self) -> str:
        """Expose GCP project id to the environment."""
        gcp_project_id = self.settings.get("gcp_project_id", None)
        if gcp_project_id:
            os.environ["GCP_PROJECT_ID"] = gcp_project_id
            return gcp_project_id

    def bucket(self) -> str:
        """Get GCP bucket from settings."""
        return self.settings.get("gcs_bucket", None)

"""Classes to house project wide generic operations."""
import os
import yaml


class Config:
    """Class used to load settings.yml file."""

    def __init__(self, settings_file: str) -> None:
        """Initialise the class.

        args:
            settings_file: (str)
                The path to the yaml
                settings file used to
        """
        self.settings_file = settings_file or "settings.yml"

    def settings(self) -> None:
        """Load settings.yml into memory."""
        with open(self.settings_file, "r") as file:
            try:

                return yaml.safe_load(file)
            except yaml.YAMLError as err:
                raise yaml.YAMLError(err)
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

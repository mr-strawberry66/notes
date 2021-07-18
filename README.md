# Notes
This repository is to house code used to run my note-taking application.

## Environment
Included in this repo is a file called `env-template`. This file is a template you can use in order to create an environment file of your own.

| Name | Meaning |
|---|---|
| GCP_PROJECT_ID | The ID of your Google Cloud Platform (GCP) project. This is required as the notes are written to a GCP instance. |
| DATASET | The ID of a dataset within BigQuery. This dataset is where your notes will be written. This is used as a suffix to the full dataset name. |
| ENVIRONMENT | A prefix added to the provided DATASET environment variable. This is used to determine whether the code will write to a production or development environment. Recommended values are `dev` for development, and `prod` for production. Defaults to `dev` if no value is provided. |
| TABLE | The name of the BigQuery table you would like to write your notes to. Defaults to `notes` if no value is provided. |

"""A placeholder file to execute code used to test."""
from sk_notes import BigQueryOperations


def main():
    """Execute code for testing."""
    bq_ops = BigQueryOperations(
        table="test_notes",
    )

    print(bq_ops.read_notes())


if __name__ == "__main__":
    main()

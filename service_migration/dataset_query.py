from google.cloud import bigquery


def dataset_input(filename):
    bqclient = bigquery.Client()

    # Download query results.
    query_string = "SELECT * FROM `macro-centaur-330222.service_migration_dataset." + filename + "`"

    dataframe = (
        bqclient.query(query_string)
            .result()
            .to_dataframe(
            create_bqstorage_client=True,
        )
    )
    return dataframe

import sys
import awswrangler as wr
from kestra import Kestra


INGEST_S3_KEY_PATH = "s3://kestra-iceberg-demo/inbox/"

if len(sys.argv) > 1:
    INGEST_S3_KEY_PATH = sys.argv[1]
else:
    print(f"No custom path provided. Using the default path: {INGEST_S3_KEY_PATH}.")

# Iceberg table
BUCKET_NAME = "kestra-iceberg-demo"
DATABASE = "kestra-iceberg-demo-db"
TABLE = "raw_fruits"

# Iceberg table's location
S3_PATH = f"s3://{BUCKET_NAME}/{TABLE}"
S3_PATH_TMP = f"{S3_PATH}_tmp"


MERGE_QUERY = """
MERGE INTO fruits f USING (
    SELECT *
    FROM (
        SELECT
            *,
            ROW_NUMBER() OVER (PARTITION BY fruit ORDER BY id DESC) AS rn
        FROM raw_fruits
    ) t
    WHERE rn = 1
) r
    ON f.fruit = r.fruit
    WHEN MATCHED
        THEN UPDATE
            SET id = r.id, berry = r.berry, update_timestamp = current_timestamp
    WHEN NOT MATCHED
        THEN INSERT (id, fruit, berry, update_timestamp)
              VALUES(r.id, r.fruit, r.berry, current_timestamp);
"""

if not INGEST_S3_KEY_PATH.startswith("s3://"):
    INGEST_S3_KEY_PATH = f"s3://{BUCKET_NAME}/{INGEST_S3_KEY_PATH}"

df = wr.s3.read_csv(INGEST_S3_KEY_PATH)
nr_rows = df.id.nunique()
print(f"Ingesting {nr_rows} rows")
Kestra.counter("nr_rows", nr_rows, {"table": TABLE})

df = df[~df["fruit"].isin(["Blueberry", "Banana"])]
df = df.drop_duplicates(subset=["fruit"], ignore_index=True, keep="first")

wr.catalog.delete_table_if_exists(database=DATABASE, table=TABLE)

wr.athena.to_iceberg(
    df=df,
    database=DATABASE,
    table=TABLE,
    table_location=S3_PATH,
    temp_path=S3_PATH_TMP,
    partition_cols=["berry"],
    keep_files=False,
)

wr.athena.start_query_execution(
    sql=MERGE_QUERY,
    database=DATABASE,
    wait=True,
)
print(f"New data successfully ingested into {S3_PATH}")
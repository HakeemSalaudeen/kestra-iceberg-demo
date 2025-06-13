import awswrangler as wr
import pandas as pd

bucket_name = "kestra-iceberg-demo"
glue_database = "kestra-iceberg-demo-db"
glue_table = "raw_fruits"
path = f"s3://{bucket_name}/{glue_table}/"
temp_path = f"s3://{bucket_name}/{glue_table}_tmp/"

wr.catalog.delete_table_if_exists(database=glue_database, table=glue_table)

#read csv
df = pd.read_csv("https://huggingface.co/datasets/kestra/datasets/raw/main/csv/fruit.csv")
df = df[~df["fruit"].isin(["Blueberry", "Banana"])]
df = df.drop_duplicates(subset=["fruit"], ignore_index=True, keep="first")

wr.athena.to_iceberg(
    df=df,
    database=glue_database,
    table=glue_table,
    table_location=path,
    temp_path=temp_path,
    partition_cols=["berry"],
)
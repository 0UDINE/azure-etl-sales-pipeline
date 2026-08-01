import pandas as pd
from azure.storage.blob import BlobServiceClient
import os
from io import StringIO
from dotenv import load_dotenv

load_dotenv()

CONN_STRING = os.environ["AZURE_STORAGE_CONNECTION_STRING"]


def read_processed_data() -> pd.DataFrame:
    client = BlobServiceClient.from_connection_string(CONN_STRING)

    blob = client.get_blob_client(
        container="processed",
        blob="sales_processed.csv"
    )

    content = blob.download_blob().readall().decode("utf-8")

    return pd.read_csv(StringIO(content))


def summarize(df: pd.DataFrame) -> None:
    print(f"\nTotal records : {len(df)}")
    print(f"Columns       : {list(df.columns)}")

    print("\nRevenue by region:")

    # ADF does column copy/rename - Python adds business logic on top
    df["revenue"] = (
        df["quantity"]
        * df["unit_price"]
        * (1 - df["discount_pct"] / 100)
    )

    print(
        df.groupby("region")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .round(2)
    )


if __name__ == "__main__":
    df = read_processed_data()
    summarize(df)
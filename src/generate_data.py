import pandas as pd
import numpy as np
from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv

load_dotenv()

CONN_STRING = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
CONTAINER = "raw"
BLOB_NAME = "sales_raw.csv"


def generate_sales_data(rows: int = 500) -> pd.DataFrame:
    np.random.seed(42)

    regions = ["EMEA", "APAC", "AMER", "LATAM"]
    products = ["Widget-A", "Widget-B", "Widget-C", "Widget-D"]

    return pd.DataFrame({
        "transaction_id": [f"TXN-{i:05d}" for i in range(rows)],
        "sale_date": pd.date_range(
            "2024-01-01",
            periods=rows,
            freq="h"
        ).strftime("%Y-%m-%d"),
        "region": np.random.choice(regions, rows),
        "product": np.random.choice(products, rows),
        "quantity": np.random.randint(1, 50, rows),
        "unit_price": np.round(np.random.uniform(10.0, 500.0, rows), 2),
        "discount_pct": np.random.choice([0, 5, 10, 15, 20], rows),
    })


def upload_to_blob(df: pd.DataFrame) -> None:
    client = BlobServiceClient.from_connection_string(CONN_STRING)
    blob_client = client.get_blob_client(
        container=CONTAINER,
        blob=BLOB_NAME
    )

    blob_client.upload_blob(
        df.to_csv(index=False),
        overwrite=True
    )

    print(f"Uploaded {len(df)} rows to {CONTAINER}/{BLOB_NAME}")


if __name__ == "__main__":
    df = generate_sales_data()
    upload_to_blob(df)
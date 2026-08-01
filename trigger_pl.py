from azure.identity import ClientSecretCredential
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import CreateRunResponse
import os
import time
from dotenv import load_dotenv

load_dotenv()

SUBSCRIPTION_ID = os.environ["AZURE_SUBSCRIPTION_ID"]
RESOURCE_GROUP = "rg-etl-demo"
FACTORY_NAME = "adf-etl-demo-oussama"
PIPELINE_NAME = "pl_etl_sales"

# Use Service Principal - create one in Azure AD -> App registrations
credential = ClientSecretCredential(
    tenant_id=os.environ["AZURE_TENANT_ID"],
    client_id=os.environ["AZURE_CLIENT_ID"],
    client_secret=os.environ["AZURE_CLIENT_SECRET"],
)


def trigger_and_wait() -> None:
    adf_client = DataFactoryManagementClient(
        credential,
        SUBSCRIPTION_ID,
    )

    run: CreateRunResponse = adf_client.pipelines.create_run(
        RESOURCE_GROUP,
        FACTORY_NAME,
        PIPELINE_NAME,
    )

    run_id = run.run_id
    print(f"Pipeline triggered. Run ID: {run_id}")

    # Poll status
    while True:
        run_status = adf_client.pipeline_runs.get(
            RESOURCE_GROUP,
            FACTORY_NAME,
            run_id,
        )

        status = run_status.status
        print(f"Status: {status}")

        if status in ("Succeeded", "Failed", "Cancelled"):
            break

        time.sleep(5)

    if status == "Succeeded":
        print("ETL pipeline completed successfully.")
    else:
        raise RuntimeError(f"Pipeline ended with status: {status}")


if __name__ == "__main__":
    trigger_and_wait()
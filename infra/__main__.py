import pulumi
from pulumi_azure_native import resources, storage, web

# Resource Group
resource_group = resources.ResourceGroup("comgas-service", location="Brazil South", resource_group_name="comgas-service")

# Storage Account
account = storage.StorageAccount(
    "storage",
    resource_group_name=resource_group.name,
    sku={"name": storage.SkuName.STANDARD_LRS},
    kind=storage.Kind.STORAGE_V2,
    location="Brazil South",
)

account_keys = storage.list_storage_account_keys_output(
    resource_group_name=resource_group.name,
    account_name=account.name
)

account_key = account_keys.keys.apply(lambda keys: keys[0].value)

blob_container = storage.BlobContainer(
    "blob_container-comgas",
    resource_group_name=resource_group.name,
    account_name=account.name,
    container_name="blob-container-comgas",
    public_access="None",
)

zip_code_path = pulumi.asset.FileArchive("./handler")

blob = storage.Blob(
    "blob-code-comgas",
    resource_group_name=resource_group.name,
    account_name=account.name,
    container_name=blob_container.name,
    blob_name="blob-code-comgas.zip",
    type="Block",
    source=zip_code_path,
)

# App Service Plan
plan = web.AppServicePlan(
    "app_service_plan",
    name="app-service-plan",
    resource_group_name=resource_group.name,
    kind="FunctionApp",
    sku={"tier": "Dynamic", "name": "Y1"},
    reserved=True,
)

zip_url = pulumi.Output.concat(
    "https://", account.name, ".blob.core.windows.net/", blob_container.name, "/", blob.name
)

# Exporta os recursos que outras stacks vão usar
pulumi.export("resource_group_name", resource_group.name)
pulumi.export("storage_account_name", account.name)
pulumi.export("app_service_plan_id", plan.id)
pulumi.export("account_key", account_key)
pulumi.export("zip_url", zip_url)
import pulumi
from pulumi_azure_native import web

# Referência aos outputs da stack `infra`
infra_stack = pulumi.StackReference("Rodrigosiq03/comgas-service/infra")  # Substitua "user" pelo seu usuário Pulumi

resource_group_name = infra_stack.get_output("resource_group_name")
app_service_plan_id = infra_stack.get_output("app_service_plan_id")
storage_account_name = infra_stack.get_output("storage_account_name")
account_key = infra_stack.get_output("account_key")
zip_url = infra_stack.get_output("zip_url")

# Função e Configuração da API (aproveite o código que já criou)
function_app = web.WebApp(
  "function-app-comgas",
  resource_group_name=resource_group_name,
  name="functions-app-comgas",
  server_farm_id=app_service_plan_id,
  reserved=True, # TORNAR O SISTEMA OPERACIONAL LINUX
  location="Brazil South",
  kind="FunctionApp",
  site_config=web.SiteConfigArgs(
    app_settings=[
      web.NameValuePairArgs(name="FUNCTIONS_WORKER_RUNTIME", value="python"),
      web.NameValuePairArgs(name="FUNCTIONS_EXTENSION_VERSION", value="~4"),
      web.NameValuePairArgs(name="AzureWebJobsStorage", value=f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"),
    ],
    linux_fx_version="Python|3.10",
    cors=web.CorsSettingsArgs(allowed_origins=["*"]),
  ),
  https_only=True,
  public_network_access="Enabled",
)

pulumi.export("host_name", function_app.default_host_name)
pulumi.export("function_app_name", function_app.name)

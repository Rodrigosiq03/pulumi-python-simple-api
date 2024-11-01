import pulumi
from pulumi_azure_native import apimanagement
from pulumi import Output

# Referência aos outputs da stack `webapp`
web_app_stack = pulumi.StackReference("Rodrigosiq03/comgas-service/webapp")
infra_stack = pulumi.StackReference("Rodrigosiq03/comgas-service/infra")

resource_group_name = infra_stack.get_output("resource_group_name")
host_name = web_app_stack.get_output("host_name")

apim = apimanagement.ApiManagementService(
  resource_name="apiManagementService",
  resource_group_name=resource_group_name,
  location="Brazil South",
  publisher_name="Intelicity",
  publisher_email="rodrigo.siqueira@intelicity.com.br",
  sku=apimanagement.ApiManagementServiceSkuPropertiesArgs(
    capacity=0,
    name="Consumption",
  ),
)

api = apimanagement.Api(
  resource_name="comgas-api",
  resource_group_name=resource_group_name,
  api_id="comgas-api",
  service_name=apim.name,
  display_name="Comgas API",
  path="/api",
  protocols=["https"],
  subscription_required=False
)

health_check = apimanagement.ApiOperation(
  "healthCheckOperation",
  api_id=api.id.apply(lambda id: id.split("/")[-1]),
  resource_group_name=resource_group_name,
  service_name=apim.name,
  operation_id="healthCheck",
  display_name="Health Check",
  method="GET",
  url_template="/health",
  responses=[
    apimanagement.ResponseContractArgs(
      status_code=200,
      description="Health check successful.",
      representations=[{"contentType": "application/json"}],
    )
  ],
)

policy = apimanagement.ApiOperationPolicy(
  "policy",
  api_id=api.id.apply(lambda id: id.split("/")[-1]),
  resource_group_name=resource_group_name,
  service_name=apim.name,
  operation_id=health_check.id.apply(lambda id: id.split("/")[-1]),
  value=f"""
    <policies>
      <inbound>
        <base />
        <set-backend-service backend-id="{host_name}" />
      </inbound>
      <backend>
        <base />
        <backend-service base-url="https://{host_name}" />
      </backend>
      <outbound>
        <base />
      </outbound>
      <on-error>
        <base />
      </on-error>
    </policies>
  """,
)

pulumi.export("function_app_url", Output.concat("https://", host_name, "/api/health"))

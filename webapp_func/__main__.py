import pulumi
from pulumi_azure_native import web

infra_stack = pulumi.StackReference("Rodrigosiq03/comgas-service/infra")
web_app_stack = pulumi.StackReference("Rodrigosiq03/comgas-service/webapp")

resource_group_name = infra_stack.get_output("resource_group_name")
zip_url = infra_stack.get_output("zip_url")
function_app_name = web_app_stack.get_output("function_app_name")
  

health_check_function = web.WebAppFunction(
  "health-check-function",
  resource_group_name=resource_group_name,
  name=function_app_name,
  function_name="health",
  script_root_path_href=zip_url,
  script_href="function_app.py",
  kind="HttpTrigger",
  config={
    "bindings": [
      {
        "authLevel": "anonymous",
        "type": "httpTrigger",
        "direction": "in",
        "name": "req",
        "methods": ["GET"],
        "route": "health",
      },
      {
        "type": "http",
        "direction": "out",
        "name": "$return",
      },
    ],
    "scriptFile": "function_app.py",
  },
)
import pulumi

stack = pulumi.get_stack()
if stack == "infra":
  from infra.__main__ import * 
elif stack == "api":
  from api.__main__ import * 
elif stack == "webapp":
  from webapp.__main__ import *
elif stack == "webapp_func":
  from webapp_func.__main__ import *
else:
  raise Exception(f"Stack '{stack}' não encontrada.")

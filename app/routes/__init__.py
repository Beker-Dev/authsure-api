import os
import importlib
from fastapi import APIRouter

router = APIRouter()

current_directory = os.path.dirname(__file__)

package_name = os.path.basename(current_directory)

for filename in os.listdir(current_directory):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]
        module = importlib.import_module(f"app.routes.{module_name}")

        if hasattr(module, "router"):
            router.include_router(module.router)

import importlib.util
import pip._internal

packages = ["pygame", "requests", "websockets"]
for package in packages:
    spec = importlib.util.find_spec(package)
    if spec is None:
        pip._internal.main(["install", package])
        print(f"installed {package}")

    else:
        print(f"{package} already installed")

import main
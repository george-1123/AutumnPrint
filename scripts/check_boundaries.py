"""Check imports and declared package dependency directions."""

import ast
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
allowed = {
    "autumn_api": {"autumn_control", "autumn_contracts"},
    "autumn_worker": {"autumn_control", "autumn_contracts"},
    "autumn_edge": {"autumn_contracts"},
    "autumn_control": {"autumn_contracts"},
    "autumn_contracts": set(),
}
issues = []
for manifest in [*ROOT.glob("apps/*/pyproject.toml"), *ROOT.glob("packages/*/pyproject.toml")]:
    config = tomllib.loads(manifest.read_text())
    source = manifest.parent / "src"
    owner = next(source.iterdir()).name
    permitted = allowed[owner] | {owner}
    for dependency in config["project"].get("dependencies", []):
        package = dependency.split("[")[0].split(">=")[0].replace("-", "_")
        if package.startswith("autumn_") and package not in permitted:
            issues.append(f"{manifest}: prohibited dependency {package}")
    for path in source.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            imports = (
                [node.module]
                if isinstance(node, ast.ImportFrom)
                else ([alias.name for alias in node.names] if isinstance(node, ast.Import) else [])
            )
            for module in imports:
                package = (module or "").split(".")[0]
                if package.startswith("autumn_") and package not in permitted:
                    issues.append(f"{path}:{node.lineno}: prohibited import {package}")
if issues:
    raise SystemExit("\n".join(issues))
print("Python dependency boundaries passed")

import json
from pathlib import Path

from autumn_api.main import create_app
from autumn_contracts import Command, CompleteCommand, EdgeRegistration
from autumn_control.settings import Settings

root = Path(__file__).resolve().parents[1]
settings = Settings("personal", "schema", "sqlite:///:memory:", "d" * 32, "e" * 32)
schema = create_app(settings).openapi()
target = root / "packages/sdk-ts"
(target / "openapi.json").write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")
(target / "protocol.json").write_text(
    json.dumps(
        {
            model.__name__: model.model_json_schema()
            for model in (Command, CompleteCommand, EdgeRegistration)
        },
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)

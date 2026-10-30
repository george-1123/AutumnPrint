import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, StrictInt


class Component(BaseModel):
    model_config = ConfigDict(extra="forbid")
    model: str
    per_kit: StrictInt = Field(gt=0)


class OrderFixture(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    kits: StrictInt = Field(gt=0)
    models: dict[str, str | None]
    components: list[Component] = Field(min_length=1)
    missing_information: list[str]


def show_order(path: Path):
    order = OrderFixture.model_validate_json(path.read_text(encoding="utf-8"))
    lines = []
    for item in order.components:
        if item.model not in order.models:
            raise ValueError(f"unknown model: {item.model}")
        model_path = order.models[item.model]
        if model_path:
            target = (path.parent / model_path).resolve()
            if not target.is_relative_to(path.parent.resolve()):
                raise ValueError("model path escapes fixture directory")
            if not target.is_file():
                raise ValueError(f"missing model file: {item.model}")
        lines.append(
            {
                "model": item.model,
                "required_quantity": order.kits * item.per_kit,
                "model_available": bool(model_path),
            }
        )
    return json.dumps(
        {
            "id": order.id,
            "kits": order.kits,
            "lines": lines,
            "missing_information": order.missing_information,
        },
        ensure_ascii=False,
        indent=2,
    )

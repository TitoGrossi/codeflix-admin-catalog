from __seedwork.domain.value_objects import UniqueEntityId
from abc import ABC
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, TypeVar


Property = TypeVar("Property")


@dataclass(slots=True, frozen=True, order=False, kw_only=True)
class Entity(ABC):
    unique_entity_id: UniqueEntityId = field(
        default_factory=lambda: UniqueEntityId())

    def __eq__(self, __o: "Entity") -> bool:
        return self.unique_entity_id == __o.unique_entity_id

    @property
    def id(self) -> str:
        return self.unique_entity_id.id

    def to_dict(self) -> Dict[str, Any]:
        entity_dict = asdict(self)
        entity_dict.pop("unique_entity_id")
        entity_dict["id"] = self.id
        return entity_dict

    def _set(self, property_name: str, value: Property):
        object.__setattr__(self, property_name, value)
        return self

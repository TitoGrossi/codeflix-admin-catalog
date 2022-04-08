from abc import ABC
from dataclasses import dataclass, field, fields
import uuid

from __seedwork.exceptions import InvalidUUIDException


@dataclass(frozen=True)
class ValueObject(ABC):
    def __str__(self) -> str:
        fields_name = [getattr(self, f.name) for f in fields(self)]
        return f"<{self.__class__.__name__}: {'[' if len(fields_name) != 1 else ''}{', '.join(fields_name)}{']' if len(fields_name) != 1 else ''}>"


@dataclass(frozen=True)
class UniqueEntityId(ValueObject):
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self):
        id_value = str(self.id) if isinstance(
            self.id, uuid.UUID) else self.id
        object.__setattr__(self, "id", id_value)
        self.__validate()

    def __validate(self):
        try:
            uuid.UUID(self.id)
        except ValueError as err:
            raise InvalidUUIDException() from err

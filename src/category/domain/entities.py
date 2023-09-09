from dataclasses import dataclass, field
from datetime import datetime
from functools import partialmethod
from typing import Optional

from __seedwork.domain.validators import ValidatorRules
from __seedwork.entities import Entity


# Desafio 1 (atribuição de propriedades):
# Criar operações:
# update | activate | deactivate


@dataclass(slots=True, frozen=True, order=False, kw_only=True)
class Category(Entity):
    name: str
    description: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = field(
        default_factory=lambda: datetime.now())

    def update(self, name: str, description: str):
        self.validate(name, description, self.is_active)
        self._set("name", name)
        self._set("description", description)

    def __set_active(self, active: bool) -> None:
        self.validate(self.name, self.description, active)
        self._set("is_active", active)

    activate = partialmethod(__set_active, active=True)
    deactivate = partialmethod(__set_active, active=False)

    @classmethod
    def validate(cls, name: str, description: Optional[str], is_active: bool):
        ValidatorRules.values(name, "name").required().string().max_length(255)
        ValidatorRules.values(description, "description").string()
        ValidatorRules.values(is_active, "is_active").required().boolean()

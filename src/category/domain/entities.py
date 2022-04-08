from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from __seedwork.entities import Entity


@dataclass(frozen=True, kw_only=True)
class Category(Entity):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    # pylint: disable=unnecessary-lambda
    created_at: Optional[datetime] = field(
        default_factory=lambda: datetime.now())

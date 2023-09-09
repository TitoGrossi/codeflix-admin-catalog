from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Generic, List, TypeVar

from rest_framework.serializers import Serializer

from __seedwork.exceptions import ValidationException


@dataclass(frozen=True, slots=True)
class ValidatorRules:
    value: Any
    prop: str

    @staticmethod
    def values(value: Any, prop: str) -> "ValidatorRules":
        return ValidatorRules(value=value, prop=prop)

    def required(self) -> "ValidatorRules":
        if self.value is None or self.value == "":
            raise ValidationException(f"The {self.prop} field is required")
        return self

    def string(self) -> "ValidatorRules":
        if self.value is not None and not isinstance(self.value, str):
            raise ValidationException(
                f"The {self.prop} field must be a string")

        return self

    def max_length(self, max_length: int) -> "ValidatorRules":
        if self.value is not None and len(self.value) > max_length:
            raise ValidationException(
                f"The {self.prop} field must not surpass the length of {max_length}"
            )

        return self

    def boolean(self) -> "ValidatorRules":
        if self.value is not None and not isinstance(self.value, bool):
            raise ValidationException(
                f"The {self.prop} field must be a boolean")

        return self


ErrorFields = Dict[str, List[str]]

PropsValidated = TypeVar("PropsValidated", None, str)


@dataclass(slots=True, kw_only=True)
class ValidatorFieldsInterface(ABC, Generic[PropsValidated]):
    errors: ErrorFields = {}
    validated_data: PropsValidated | None = None

    @abstractmethod
    def validate(self, data: Any) -> bool:
        raise NotImplementedError()


class DRFValidator(ValidatorFieldsInterface[PropsValidated]):
    def validate(self, data: Serializer[Dict[str, PropsValidated]]) -> bool:
        serializer = data
        is_valid = serializer.is_valid()
        if not is_valid:
            self.errors = {
                key: [str(_error) for _error in _errors] for key, _errors in serializer.errors.items()
            }
            return False

        self.validated_data = serializer.validated_data
        return True

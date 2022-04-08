from abc import ABC
from dataclasses import FrozenInstanceError, dataclass, fields, is_dataclass
import unittest
from unittest.mock import patch
import uuid

from __seedwork.domain.value_objects import UniqueEntityId, ValueObject
from __seedwork.exceptions import InvalidUUIDException


# Class to immitate defined behaviour to test ABC
@dataclass(frozen=True)
class StubOneProp(ValueObject):
    prop: str


# Class to immitate defined behaviour to test ABC
@dataclass(frozen=True)
class StubTwoProp(ValueObject):
    prop1: str
    prop2: str


class TestValueObject(unittest.TestCase):
    def test_is_dataclass(self):
        self.assertTrue(is_dataclass(UniqueEntityId))

    def test_is_abc(self):
        self.assertIsInstance(ValueObject(), ABC)

    def test_init_prop(self):
        vo = StubOneProp(prop="value")
        self.assertEqual(vo.prop, "value")

        vo = StubTwoProp(prop1="value1", prop2="value2")
        self.assertEqual(vo.prop1, "value1")
        self.assertEqual(vo.prop2, "value2")

    def test_convert_to_str(self):
        vo = StubOneProp(prop="value1")
        self.assertEqual(
            f"<{vo.__class__.__name__}: {vo.prop}>", str(vo))

        vo = StubTwoProp(prop1="value1", prop2="value2")
        fields_name = [getattr(vo, f.name) for f in fields(vo)]
        self.assertEqual(
            f"<{vo.__class__.__name__}: [{', '.join(fields_name)}]>", str(vo))

    def test_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            vo = StubOneProp(prop="value")
            vo.prop = "prop"


class TestUniqueEntityIdUnit(unittest.TestCase):
    def test_is_dataclass(self):
        self.assertTrue(is_dataclass(UniqueEntityId))

    def test_validate_error_for_non_valid_uuid(self):
        with patch.object(
            UniqueEntityId,
            "_UniqueEntityId__validate",
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate,
        ) as mock_validate:
            with self.assertRaises(InvalidUUIDException) as assert_error:
                UniqueEntityId("lasdfjklskj")
            mock_validate.assert_called_once()
            self.assertEqual(
                assert_error.exception.args[0], "ID must be valid UUID")

    def test_accepts_valid_uuid_passed_in_constructor(self):
        with patch.object(
            UniqueEntityId,
            "_UniqueEntityId__validate",
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate,
        ) as mock_validate:
            value_object = UniqueEntityId(
                "afbec0bc-49d4-4085-82d4-9a6aabd568c9")
            mock_validate.assert_called_once()
            self.assertEqual(
                value_object.id, "afbec0bc-49d4-4085-82d4-9a6aabd568c9")

    def test_uuid_converted_to_str(self):
        uuid_value = uuid.uuid4()
        value_object = UniqueEntityId(uuid_value)
        self.assertEqual(value_object.id, str(uuid_value))

    def test_generate_id_if_no_arg_for_id_is_passed(self):
        value_object = UniqueEntityId()
        # Assert the uuid is generated and is a valid one (next line would raise error otherwise)
        uuid.UUID(value_object.id)

    def test_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            value_object = UniqueEntityId()
            value_object.id = "ldkfjasl"

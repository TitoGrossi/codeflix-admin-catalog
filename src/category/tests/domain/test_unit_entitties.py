# pylint: disable=unexpected-keyword-arg
from abc import ABC
from dataclasses import is_dataclass, dataclass
import unittest
import uuid
from __seedwork.domain.value_objects import UniqueEntityId

from __seedwork.entities import Entity


# Class to immitate defined behaviour to test ABC
@dataclass(frozen=True, kw_only=True)
class StubEntity(Entity):
    prop1: str
    prop2: str


class TestEntityUnit(unittest.TestCase):
    def test_is_dataclass(self):
        self.assertTrue(is_dataclass(Entity))

    def test_is_abc(self):
        self.assertIsInstance(Entity(), ABC)

    def test_set_unique_entity_id_and_props(self):
        entity = StubEntity(prop1="prop1", prop2="prop2")

        self.assertEqual(entity.prop1, "prop1")
        self.assertEqual(entity.prop2, "prop2")
        self.assertIsInstance(entity.unique_entity_id, UniqueEntityId)
        self.assertEqual(entity.unique_entity_id.id, entity.id)

    def test_accepts_a_valid_uuid_as_id(self):
        id_ = str(uuid.uuid4())
        entity = StubEntity(unique_entity_id=UniqueEntityId(
            id=id_), prop1="prop1", prop2="prop2")

        self.assertEqual(entity.id, id_)

    def test_to_dict_method(self):
        entity = StubEntity(prop1="prop1", prop2="prop2")

        self.assertDictEqual(entity.to_dict(), {
            "id": entity.id,
            "prop1": "prop1",
            "prop2": "prop2",
        })

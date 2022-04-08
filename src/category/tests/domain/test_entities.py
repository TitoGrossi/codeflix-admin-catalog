# pylint: disable=unexpected-keyword-arg
from dataclasses import FrozenInstanceError, is_dataclass
from datetime import datetime
import unittest

from category.domain.entities import Category


class TestCategoryUnit(unittest.TestCase):
    def test_constructor_category(self):
        new_category = Category(
            name="Teste",
            description="Uma descricao",
            is_active=True,
            created_at=datetime.now())
        self.assertEqual(new_category.name, "Teste")
        self.assertEqual(new_category.description, "Uma descricao")
        self.assertEqual(new_category.is_active, True)
        self.assertIsInstance(new_category.created_at, datetime)

    def test_constructor_uses_default_values(self):
        new_category = Category(name="Teste")
        self.assertEqual(new_category.description, None)
        self.assertEqual(new_category.is_active, True)
        self.assertIsInstance(new_category.created_at, datetime)

    def test_constructor_uses_default_value_create_at(self):
        category1 = Category(name="Teste")
        category2 = Category(name="Teste")
        self.assertNotEqual(category1.created_at, category2.created_at)

    def test_is_dataclass(self):
        self.assertTrue(is_dataclass(Category))

    def test_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            entity = Category(name="Teste")
            entity.name = "ldkfjasl"

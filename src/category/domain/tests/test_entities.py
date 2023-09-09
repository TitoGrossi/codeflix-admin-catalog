# pylint: disable=unexpected-keyword-arg
from dataclasses import is_dataclass
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

    def test_update_category(self):
        category = Category(name="Teste")
        category.update(name="Novo nome", description="Descricao")
        self.assertEqual(category.name, "Novo nome")
        self.assertEqual(category.description, "Descricao")

    def test_activate_category(self):
        category = Category(name="Teste", is_active=False)
        category.activate()
        self.assertEqual(category.is_active, True)

    def test_deactivate_category(self):
        category = Category(name="Teste")
        category.deactivate()
        self.assertEqual(category.is_active, False)

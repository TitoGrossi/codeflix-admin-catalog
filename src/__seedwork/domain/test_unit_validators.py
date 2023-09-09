from typing import List
import unittest

from __seedwork.domain.validators import ValidatorRules
from __seedwork.exceptions import ValidationException


class TestValidatorRules(unittest.TestCase):
    dummy_value = "some value"
    def test_values_method(self):
        validator = ValidatorRules.values(self.dummy_value, "prop")
        self.assertIsInstance(validator, ValidatorRules)
        self.assertEqual(validator.value, self.dummy_value)
        self.assertEqual(validator.prop, "prop")

    def test_required_rule(self):
        invalid_data: List[ValidatorRules] = [
            ValidatorRules.values(None, "prop"),
            ValidatorRules.values("", "prop"),
        ]
        for invalid_instance in invalid_data:
            with self.assertRaises(ValidationException) as assert_error:
                invalid_instance.required()
            self.assertEqual(
                assert_error.exception.args[0],
                f"The {invalid_instance.prop} field is required"
            )

        valid_data = [
            ValidatorRules.values("test", "prop"),
            ValidatorRules.values(5, "prop"),
            ValidatorRules.values(0, "prop"),
            ValidatorRules.values(False, "prop"),
        ]
        for valid_instance in valid_data:
            self.assertIsInstance(valid_instance.required(), ValidatorRules)

    def test_string_rule(self):
        invalid_data: List[ValidatorRules] = [
            ValidatorRules.values(5, "prop"),
            ValidatorRules.values(True, "prop"),
        ]
        for invalid_instance in invalid_data:
            with self.assertRaises(ValidationException) as assert_error:
                invalid_instance.string()
            self.assertEqual(
                assert_error.exception.args[0],
                f"The {invalid_instance.prop} field must be a string"
            )

        valid_data = [
            ValidatorRules.values("test", "prop"),
            ValidatorRules.values("", "prop"),
            ValidatorRules.values("0", "prop"),
            ValidatorRules.values(None, "prop"),
        ]
        for valid_instance in valid_data:
            self.assertIsInstance(valid_instance.string(), ValidatorRules)

    def test_max_length_rule(self):
        invalid_data: List[ValidatorRules] = [
            ValidatorRules.values("t"*5, "prop"),
        ]
        for invalid_instance in invalid_data:
            with self.assertRaises(ValidationException) as assert_error:
                invalid_instance.max_length(4)
            self.assertEqual(
                assert_error.exception.args[0],
                f"The {invalid_instance.prop} field must not surpass the length of 4"
            )

        valid_data = [
            ValidatorRules.values("t"*5, "prop"),
        ]
        for valid_instance in valid_data:
            self.assertIsInstance(valid_instance.max_length(5), ValidatorRules)

    def test_boolean_rule(self):
        invalid_data: List[ValidatorRules] = [
            ValidatorRules.values("teste", "prop"),
            ValidatorRules.values(2, "prop"),
            ValidatorRules.values(0, "prop"),
            ValidatorRules.values(1, "prop"),
        ]
        for invalid_instance in invalid_data:
            with self.assertRaises(ValidationException) as assert_error:
                invalid_instance.boolean()
            self.assertEqual(
                assert_error.exception.args[0],
                f"The {invalid_instance.prop} field must be a boolean"
            )

        valid_data = [
            ValidatorRules.values(True, "prop"),
            ValidatorRules.values(False, "prop"),
            ValidatorRules.values(None, "prop"),
        ]
        for valid_instance in valid_data:
            self.assertIsInstance(valid_instance.boolean(), ValidatorRules)

    def test_throw_a_validation_exception_when_combine_two_or_more_rules(self):
        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(None, "prop").required().string().max_length(5)
        self.assertEqual(assert_error.exception.args[0], "The prop field is required")

        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(False, "prop").required().string().max_length(5)
        self.assertEqual(assert_error.exception.args[0], "The prop field must be a string")

        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values("t"*5, "prop").required().string().max_length(4)
        self.assertEqual(
            assert_error.exception.args[0],
            "The prop field must not surpass the length of 4"
        )

        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(None, "prop").required().boolean()
        self.assertEqual(
            assert_error.exception.args[0],
            "The prop field is required"
        )

        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values("t", "prop").required().boolean()
        self.assertEqual(
            assert_error.exception.args[0],
            "The prop field must be a boolean"
        )

    def test_valid_cases_for_combination_between_rules(self):
        """
        Test that assures no error is thrown for valid combinations
        """
        ValidatorRules("test", "props").required().string()
        ValidatorRules("t"*5, "props").required().string().max_length(5)
        ValidatorRules(True, "props").required().boolean()

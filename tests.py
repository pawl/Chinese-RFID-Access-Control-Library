import unittest

from rfid import comma_format_to_ten_digit, ten_digit_to_comma_format


class TestTenDigitToCommaFormat(unittest.TestCase):

    def test_happy_path(self):
        result = ten_digit_to_comma_format(11111111)
        expected_result = 16935527
        self.assertEqual(result, expected_result)


class TestCommaFormatToTenDigit(unittest.TestCase):

    def test_happy_path(self):
        result = comma_format_to_ten_digit(16935527)
        expected_result = 11111111
        self.assertEqual(result, expected_result)

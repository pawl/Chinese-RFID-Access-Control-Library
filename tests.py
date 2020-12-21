import unittest

from mock import patch

from rfid import (RFIDClient, comma_format_to_ten_digit,
                  ten_digit_to_comma_format)


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


class TestRFIDClient(unittest.TestCase):
    def test_invalid_ip(self):
        with self.assertRaises(TypeError):
            RFIDClient("blah")

    @patch("rfid.RFIDClient.connect")
    @patch("rfid.RFIDClient.check_valid_ipv4_address")
    def test_controller_serial(self, mock_connect, mock_check_valid_ipv4_address):
        controller_ip = "192.168.1.20"
        controller_serial = 123106461
        rfid_client = RFIDClient(controller_ip, controller_serial)
        expected_controller_serial = "9d745607"
        self.assertEqual(rfid_client.controller_serial, expected_controller_serial)

    def test_crc_16_ibm(self):
        test_controller_serial = "9d745607"
        test_data = (
            "2010"
            + RFIDClient.source_port
            + "2800000000000000"
            + test_controller_serial
            + "00000200ffffffff"
        )
        result = RFIDClient.crc_16_ibm(test_data)
        expected_result = "201066f228000000000000009d74560700000200ffffffff"
        self.assertEqual(result, expected_result)

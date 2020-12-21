import unittest

from mock import patch

from rfid import (RFIDClient, comma_format_to_ten_digit,
                  ten_digit_to_comma_format)


TEST_CONTROLLER_IP = "192.168.1.20"
TEST_CONTROLLER_SERIAL = 123106461
TEST_BADGE = 16935527


class TestTenDigitToCommaFormat(unittest.TestCase):
    def test_happy_path(self):
        result = ten_digit_to_comma_format(11111111)
        self.assertEqual(result, TEST_BADGE)


class TestCommaFormatToTenDigit(unittest.TestCase):
    def test_happy_path(self):
        result = comma_format_to_ten_digit(TEST_BADGE)
        expected_result = 11111111
        self.assertEqual(result, expected_result)


class mock_socket(object):
    def __init__(self, expected_response_starts):
        # the expected beginning of the packet response
        self.expected_response_starts = expected_response_starts

    def recv(self, size):
        expected_response_start = self.expected_response_starts.pop()
        # repeat expected response start until matching expected recv size
        return expected_response_start * (size // 2)

    def send(self, msg):
        return len(msg)

    def close(self):
        return True


class TestRFIDClient(unittest.TestCase):
    def test_invalid_ip(self):
        with self.assertRaises(TypeError):
            RFIDClient("blah")

    @patch("rfid.RFIDClient.connect")
    @patch("rfid.RFIDClient.check_valid_ipv4_address")
    def test_controller_serial(self, mock_connect, mock_check_valid_ipv4_address):
        rfid_client = RFIDClient(TEST_CONTROLLER_IP, TEST_CONTROLLER_SERIAL)
        expected_controller_serial_hex = "9d745607"
        self.assertEqual(rfid_client.controller_serial, expected_controller_serial_hex)

    def test_crc_16_ibm(self):
        test_controller_serial_hex = "9d745607"
        test_data = (
            "2010"
            + RFIDClient.source_port
            + "2800000000000000"
            + test_controller_serial_hex
            + "00000200ffffffff"
        )
        result = RFIDClient.crc_16_ibm(test_data)
        expected_result = "201066f228000000000000009d74560700000200ffffffff"
        self.assertEqual(result, expected_result)

    @patch("rfid.RFIDClient.connect", return_value=mock_socket([b'\x23\x21', b'\x20\x11']))
    @patch("rfid.RFIDClient.check_valid_ipv4_address")
    def test_add_user(self, mock_connect, mock_check_valid_ipv4_address):
        rfid_client = RFIDClient(TEST_CONTROLLER_IP, TEST_CONTROLLER_SERIAL)
        test_doors = [1, 2]
        rfid_client.add_user(TEST_BADGE, test_doors)

    @patch("rfid.RFIDClient.connect", return_value=mock_socket([b'\x23\x21']))
    @patch("rfid.RFIDClient.check_valid_ipv4_address")
    def test_remove_user(self, mock_connect, mock_check_valid_ipv4_address):
        rfid_client = RFIDClient(TEST_CONTROLLER_IP, TEST_CONTROLLER_SERIAL)
        rfid_client.remove_user(TEST_BADGE)

    @patch("rfid.RFIDClient.connect", return_value=mock_socket([b'\x20\x41']))
    @patch("rfid.RFIDClient.check_valid_ipv4_address")
    def test_open_door(self, mock_connect, mock_check_valid_ipv4_address):
        rfid_client = RFIDClient(TEST_CONTROLLER_IP, TEST_CONTROLLER_SERIAL)
        rfid_client.open_door(1)

import unittest

from mock import patch

from rfid import RFIDClient, comma_format_to_ten_digit, ten_digit_to_comma_format

TEST_CONTROLLER_IP = "192.168.1.20"
TEST_CONTROLLER_SERIAL = 123106461
TEST_BADGE = 3126402

open_door_resp = (
    b" A\xb9\x8c\x05\x00\x00\x00\x9dtV\x07\x00\x00\x00\x00\x01\x05\x02\x00\x01"
    b"\x00\x00\x00"
)

add_badge_resp_1 = (
    b" \x11\xd0\xfc(\x00\x00\x00\x9dtV\x07\x00\x00\x00\x00\x01\x05\x02\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\xadN\x00\x00\x00\x00\x00\x00\x00\x90L\x00B"
    b"\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00"
    b"\x04\x00\x00\x00\x00A\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x16\x10\x00\x00@\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x16\x10\x00\x00?\x00\x00\x00\x01\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\x16\x10\x00\x00>\x00\x00\x00\x01\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\x10\x00\x00=\x00\x00\x00\x01"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\x10\x00\x00<\x00\x00"
    b"\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\x10\x00\x00;"
    b"\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x00\x00"
    b"\x00:\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12"
    b"\x83\x00\x009\x00\x00\x00\x02\x01\xa8\xc0\x00\x00\x00\x00\x1a\x1d\xf1"
    b"\xba\x16\x10\x00\x008\x00\x00\x00X\xd6,\x00\x00\x00\x00\x00\x1a\x1dp\xac"
    b"\x10\x90\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0\xff\xff\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00h\x00\x00\x00"
    b"\xff\x8f\xff_\x13\x86\xff\xfb\xff?\xff\x0f\xff\x1d\x00.\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\x00"
)

add_badge_resp_2 = b"#!\xee\xb1)\x00\x00\x00\x9dtV\x07\x00\x00\x00\x00\x01\x05\x02\x00"

remove_user_resp = b'#!\xa9\x86"\x00\x00\x00\x9dtV\x07\x00\x00\x00\x00\x01\x05\x02\x00'


class TestTenDigitToCommaFormat(unittest.TestCase):
    def test_happy_path(self):
        result = ten_digit_to_comma_format(2058018)
        self.assertEqual(result, TEST_BADGE)


class TestCommaFormatToTenDigit(unittest.TestCase):
    def test_happy_path(self):
        result = comma_format_to_ten_digit(TEST_BADGE)
        expected_result = 2058018
        self.assertEqual(result, expected_result)


class mock_socket(object):
    def __init__(self, responses):
        self.responses = responses

    def recv(self, size):
        return self.responses.pop()

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
        expected_result = (
            b" \x10f\xf2(\x00\x00\x00\x00\x00\x00\x00\x9dtV\x07\x00\x00\x02"
            b"\x00\xff\xff\xff\xff"
        )
        self.assertEqual(result, expected_result)

    @patch(
        "rfid.RFIDClient.connect",
        return_value=mock_socket([add_badge_resp_2, add_badge_resp_1]),
    )
    @patch("rfid.RFIDClient.check_valid_ipv4_address")
    def test_add_user(self, mock_connect, mock_check_valid_ipv4_address):
        rfid_client = RFIDClient(TEST_CONTROLLER_IP, TEST_CONTROLLER_SERIAL)
        test_doors = [1, 2]
        rfid_client.add_user(TEST_BADGE, test_doors)

    @patch("rfid.RFIDClient.connect", return_value=mock_socket([remove_user_resp]))
    @patch("rfid.RFIDClient.check_valid_ipv4_address")
    def test_remove_user(self, mock_connect, mock_check_valid_ipv4_address):
        rfid_client = RFIDClient(TEST_CONTROLLER_IP, TEST_CONTROLLER_SERIAL)
        rfid_client.remove_user(TEST_BADGE)

    @patch("rfid.RFIDClient.connect", return_value=mock_socket([open_door_resp]))
    @patch("rfid.RFIDClient.check_valid_ipv4_address")
    def test_open_door(self, mock_connect, mock_check_valid_ipv4_address):
        rfid_client = RFIDClient(TEST_CONTROLLER_IP, TEST_CONTROLLER_SERIAL)
        rfid_client.open_door(1)

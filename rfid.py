import binascii
import socket
import struct
import sys


def ten_digit_to_comma_format(badge):
    """Returns the comma-format RFID number (without the comma) from the
    10-digit RFID number.

    Explanation:
    *On an EM4100/4001 spec RFID card, there will generally be two sets of
    numbers like this: 0015362878 234,27454
    *The part of the number before the comma represents the first hex byte of
    the "10 digit" number, and the second part is the last 2 hex bytes of the
    "10 digit" card number.
    *15362878 = EA6B3E
    *Splitting EA and 6B3E and converting them to decimal numbers will give
    you 234 and 27454 (the number with the comma on the card).
    *The comma is excluded in the return value because the controller does not
    need the comma.

    :param badge: 10-digit RFID card number, must be integer
    """
    # only the last 8 digits are the ID
    # the 8 digits correspond to only 6 hex values, so the max is FFFFFF
    if badge > 16777215:
        raise Exception("Error: Invalid RFID Number")
    formatted_id = str("{0:x}".format(badge)).zfill(6)  # converts to hex

    # splits the hex at first two and last 4, converts to dec,
    # then combines into string
    id_section_1 = str(int(formatted_id[:2], 16)).zfill(3)
    id_section_2 = str(int(formatted_id[-4:], 16)).zfill(5)
    return int(id_section_1 + id_section_2)


def comma_format_to_ten_digit(badge):
    """Returns the 10-digit number from the comma-format RFID number (without
    the comma)

    Explanation:
    *On an EM4100/4001 spec RFID card, there will generally be two sets of
    numbers like this: 0015362878 234,27454
    *This function turns the number with the comma (but excluding the comma)
    into the 10-digit number which is generally next to it.
    *The part of the number before the comma represents the first hex byte of
    the "10 digit" number, and the second part is the last 2 hex bytes of the
    "10 digit" card number.
    **234 = EA
    **27454 = 6B3E
    **Combining EA and 6B3E and converting it to a decimal number will give you
    15362878 (the first 10-digit number on the card).

    :param badge: comma-format RFID card number, must be integer with the comma
    removed
    """
    # the 8 digits correspond to a set of two and four hex values,
    # so the max is the decimal version of FF and FFFF concatenated
    if badge > 25565535:
        raise Exception("Error: Invalid RFID Number")
    badge = str(badge).zfill(8)

    # splits dec at last 5 digits and everything except last 5,
    # converts each section to hex, then combines
    id_section_1 = "{0:x}".format(int(badge[:-5])).zfill(2)
    id_section_2 = "{0:x}".format(int(badge[-5:])).zfill(4)
    formatted_id = id_section_1 + id_section_2

    # convert combined hex string to int
    return int(formatted_id, 16)


class RFIDClient(object):
    # part of the byte string replaced by the CRC, not required to be valid
    source_port = "0000"

    # these bytes form the packet that starts a transaction with the RFID controller
    start_transaction = (
        b"\r\r\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    )

    def __init__(self, ip, serial):
        """
        :param ip: IP address of the controller.
        :param serial: Serial number written on the controller, also
            "Device NO" on the web interface's configuration page.
        """
        self.check_valid_ipv4_address(ip)

        if not isinstance(serial, int):
            raise TypeError("Serial must be set to an integer")

        # pack controller serial as little endian integer
        self.controller_serial = self.little_endian_hex(serial)
        self.s = self.connect(ip)

    @staticmethod
    def little_endian_hex(val):
        """Convert integer to little-endian hex string."""
        endian = struct.pack("<I", val)
        return binascii.hexlify(endian).decode("utf8")

    @staticmethod
    def check_valid_ipv4_address(ip):
        try:
            socket.inet_aton(ip)
        except socket.error:
            raise TypeError("IP Address is not valid")

    @staticmethod
    def connect(ip, timeout=5, port=60000):
        """
        :param ip: IP address of the controller
        :param timeout: settimeout value for the sockets connection
        :param port: the destination port of the socket, should always be 60000
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
            s.connect((ip, port))
            s.settimeout(timeout)
        except Exception as e:
            print(e)
            sys.exit(1)
        return s

    @staticmethod
    def crc_16_ibm(data):
        """Returns hex byte string with CRC values added to positions 4 through 8.
        This CRC value is required by the controller or it will not process the
        request.

        :param data: original hex string which needs the CRC values added to it
        """
        hex_data = bytearray.fromhex(data)
        byte_list = list(hex_data)
        num1 = 0
        for i in range(0, len(byte_list)):
            num2 = byte_list[i]
            if i == 2 or i == 3:
                num2 = 0
            num1 ^= num2
            for j in range(0, 8):
                if num1 & 1 > 0:
                    num1 = (num1 >> 1) ^ 40961
                else:
                    num1 >>= 1
        code = num1 & 65535  # integer returned from CRC function

        # change hex string to list to support assignment
        data_list = list(data)

        # switch order to little endian and return unsigned short, then
        # replace characters in list with the CRC values
        endian = struct.pack("<H", code)
        data_list[4:8] = binascii.hexlify(endian).decode("utf8")

        return bytearray.fromhex("".join(data_list))

    def add_user(self, badge, doors):
        if not isinstance(badge, int):
            raise TypeError("RFID number must be set to an integer")

        if not isinstance(doors, list):
            raise Exception("doors must be set to a list")

        # create a list of "01"'s (enabled) and "00"'s (disabled)
        # then later join to create "01000000" (which is only door 1 enabled)
        doors_enabled = ""
        for door in [1, 2, 3, 4]:
            if door in doors:
                doors_enabled += "01"
            else:
                doors_enabled += "00"

        # pack badge number as little endian integer
        badge = self.little_endian_hex(badge)

        add_packet1 = self.crc_16_ibm(
            "2010"
            + self.source_port
            + "2800000000000000"
            + self.controller_serial
            + "00000200ffffffff"
        )

        self.s.send(self.start_transaction)
        self.s.send(add_packet1)

        binary_response_1 = self.s.recv(1024)
        if binary_response_1[:2] != b" \x11":
            msg = "Unexpected Result Received: {}".format(binary_response_1)
            raise Exception(msg)

        add_packet2 = self.crc_16_ibm(
            "2320"
            + self.source_port
            + "2900000000000000"
            + self.controller_serial
            + "00000200"
            + badge
            + "00000000a04e4605"
            + "87"
            + "1c9f3b"
            + doors_enabled
            + "00000000"
        )

        self.s.send(self.start_transaction)
        self.s.send(add_packet2)

        binary_response_2 = self.s.recv(1024)
        if binary_response_2[:2] != b"#!":
            msg = "Unexpected Result Received: {}".format(binary_response_2)
            raise Exception(msg)

    def remove_user(self, badge):
        if not isinstance(badge, int):
            raise TypeError("RFID number must be set to an integer")

        # pack badge number as little endian integer
        badge = self.little_endian_hex(badge)

        remove_packet = self.crc_16_ibm(
            "2320"
            + self.source_port
            + "2200000000000000"
            + self.controller_serial
            + "00000200"
            + badge
            + "00000000204e460521149f3b0000000000000000"
        )

        self.s.send(self.start_transaction)
        self.s.send(remove_packet)

        binary_response = self.s.recv(1024)
        if binary_response[:2] != b"#!":
            msg = "Unexpected Result Received: {}".format(binary_response)
            raise Exception(msg)

    def open_door(self, door_number):
        if not isinstance(door_number, int):
            raise TypeError("RFID number must be set to an integer")
        if not (1 <= door_number <= 4):
            raise Exception("door_number must be 1 to 4")

        door_number = str(door_number - 1).zfill(2)

        open_door_packet = self.crc_16_ibm(
            "2040"
            + self.source_port
            + "0500000000000000"
            + self.controller_serial
            + "0000020001000000ffffffffffffffff"
            + door_number
            + "000000"
        )

        self.s.send(self.start_transaction)
        self.s.send(open_door_packet)

        binary_response = self.s.recv(1024)
        if binary_response[:2] != b" A":
            msg = "Unexpected Result Received: {}".format(binary_response)
            raise Exception(msg)

    def __del__(self):
        """Closes the socket connection."""
        if hasattr(self, "s"):
            self.s.close()

from rfid import RFIDClient, ten_digit_to_comma_format

ip_address = "192.168.1.20"
controller_serial = 123106461
client = RFIDClient(ip_address, controller_serial)

# badge number needs to be in "comma format"
badge = ten_digit_to_comma_format(11111111)

client.remove_user(badge)

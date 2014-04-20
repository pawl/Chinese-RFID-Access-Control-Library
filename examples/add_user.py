from rfid import ten_digit_to_comma_format, RFIDClient

ip_address = '192.168.1.20'
controller_serial = 123106461
client = RFIDClient(ip_address, controller_serial)

badge = ten_digit_to_comma_format(11111111) # badge number needs to be in "comma format"

client.addUser(badge)
from rfid import RFIDClient

ip_address = '192.168.1.20'
controller_serial = 123106461
client = RFIDClient(ip_address, controller_serial)

client.open_door(1)

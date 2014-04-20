Chinese RFID Access Control Library
========================

This library allows python to control one of the most common RFID Access Control Systems sold in China. Now you can integrate an access control system with your software to do things like remove an user when they have failed to pay their bill. 

The goal of this project is to provide a cheap, out-of-the-box solution for RFID Access Control to Hackerspaces, Makerspaces, or other businesses which rely on RFID access control.

Main Features
-----

- Programmatically add and remove users to/from the access control system
- Convert the 10-digit format RFID numbers to comma format or vice versa

Hardware Requirement
-----
This library currently only works with a single type of controller which goes by a wide variety of model numbers. The controller can be found on Ebay, Aliexpress, and Amazon for around $50 (depending on the number of doors). You can know which one to buy by looking for one that looks like this:

![alt tag](https://raw.githubusercontent.com/pawl/Chinese-RFID-Access-Control-Library/master/access_controller.png)

One of the awesome things this controller has is a web interface. You can also add users, remove users, view logs, and change settings manually through that interface. Pictures of the interface are available here: http://imgur.com/a/Mw04Y

RFID Card Number Explanation
-----
![alt tag](https://raw.githubusercontent.com/pawl/Chinese-RFID-Access-Control-Library/master/rfid_card_number_explanation.png)

There are two numbers on the card. The access controller only uses the right number which I'm calling comma-format.

My usage example below shows an example of a function which converts the number on the left (which I'm calling 10-digit format) to the number on the right (comma format).

Usage
-----

Add user (using 10-digit format RFID number):

	from rfid import ten_digit_to_comma_format, RFIDClient

	ip_address = '192.168.1.20' # IP address of the controller
	controller_serial = 123106461 # serial number written on the controller
	client = RFIDClient(ip_address, controller_serial)

	badge = ten_digit_to_comma_format(11111111) # badge number needs to be converted to "comma format"

	client.add_user(badge)

Remove user (using 10-digit format RFID number):

	from rfid import ten_digit_to_comma_format, RFIDClient

	ip_address = '192.168.1.20' # IP address of the controller
	controller_serial = 123106461 # serial number written on the controller
	client = RFIDClient(ip_address, controller_serial)

	badge = ten_digit_to_comma_format(11111111) # badge number needs to be converted to "comma format"

	client.remove_user(badge)
	

Special Thanks
-----
- Thanks to Brooks Scharff for figuring out the cool stuff that this access controller could do and keeping me interested in the project.
- Thanks to Dallas Makerspace for letting me implement and test it at their facility. 
- Thanks to Mike Metzger for his work on starting to reverse engineer Dallas Makerspace's first access control system and documenting it to show me how to do it. https://dallasmakerspace.org/wiki/ReverseEngineeringRFIDReader
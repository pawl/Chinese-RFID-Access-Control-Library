Chinese RFID Access Control Library
========================

This library allows python to control one of the most common RFID Access Control Systems sold in China. Now you can integrate an access
control system with your software to do things like remove an user when they haven't paid their bill.

The goal of this project is to provide the ability to automate an inexpensive, out-of-the-box RFID Access Control solution. This is
especially made for businesses that rely on access control + monthly billing (hackerspaces, makerspaces, and gyms).

Main Features
-----

- Programmatically add and remove users to/from the access control system
- Programmatically trigger the relay to open the door
- Convert the 10-digit format RFID numbers to comma format or vice versa

Hardware Requirement
-----
This library currently only works with a single type of controller which goes by a wide variety of model numbers. The controller can
be found by searching for "TCP access control" on Ebay, Aliexpress, and Amazon. It costs around $30-85 (depending on the number of
doors). You can know which one to buy by looking for one that looks like this:

![alt tag](https://raw.githubusercontent.com/pawl/Chinese-RFID-Access-Control-Library/master/access_controller.png)

One of the awesome things this controller has is a web interface. You can also add users, remove users, view logs, and change settings
manually through that interface. Pictures of the interface are available here: http://imgur.com/a/Mw04Y

RFID Card Number Explanation
-----
![alt tag](https://raw.githubusercontent.com/pawl/Chinese-RFID-Access-Control-Library/master/rfid_card_number_explanation.png)

There are usually two sets of numbers on the 125kHz EM4100 RFID cards. Key fobs usually only have a single 10-digit number.

The number on the right, "comma format":
* The access controller's web interface only shows this number.
* According to the Weigand 26 spec, this is the badge number in this format: ```<8 bit facility code as an integer>, <16 bit ID number as an integer>```

The number on the left, "10-digit format":
* According to the Weigand 26 spec, this is the last 24 bits of data from the card as an integer. The last 24 bits include both the 8 bit facility code and the 16 bit ID number.
* Since there are 24 bits, only 10-digit IDs within a range of 0 to 16,777,215 are possible.

My usage example below shows an example of a function which converts the 10-digit format to the comma format, and vice versa.

Usage
-----
Install:

	pip install Chinese-RFID-Access-Control-Library

Add user (using 10-digit format RFID number):

	from rfid import ten_digit_to_comma_format, RFIDClient

	ip_address = '192.168.1.20' # IP address of the controller
	controller_serial = 123106461 # serial number written on the controller
	client = RFIDClient(ip_address, controller_serial)

	badge = ten_digit_to_comma_format(11111111) # badge number needs to be converted to "comma format"

	client.add_user(badge, [1, 2]) # add privileges for door 1 & 2

Remove user (using 10-digit format RFID number):

	from rfid import ten_digit_to_comma_format, RFIDClient

	ip_address = '192.168.1.20' # IP address of the controller
	controller_serial = 123106461 # serial number written on the controller
	client = RFIDClient(ip_address, controller_serial)

	badge = ten_digit_to_comma_format(11111111) # badge number needs to be converted to "comma format"

	client.remove_user(badge)

Open door #1:

	from rfid import RFIDClient

	ip_address = '192.168.1.20'
	controller_serial = 123106461
	client = RFIDClient(ip_address, controller_serial)

	client.open_door(1)

Running Tests
-----

	python setup.py test

TODO
-----
- Adding a name to an user without the web interface doesn't seem to be possible. Figure out a way to do this? (It might not be possible to do it without doing something hacky with the web interface.)
- The controller also stores the user's 2-factor pin for when the keypad is enabled. Need to add an optional parameter to add_user for a pin.
- Add a get_users method to RFIDClient that outputs a list of all the users currently in the controller.
- Add a get_logs method to RFIDClient which outputs the card swipe logs.

Special Thanks
-----
- Thanks to Brooks Scharff for figuring out the cool stuff that this access controller could do and keeping me interested in the project.
- Thanks to Dallas Makerspace for letting me implement and test it at their facility.
- Thanks to Mike Metzger for his work on starting to reverse engineer Dallas Makerspace's first access control system and documenting it to show me how to do it. https://dallasmakerspace.org/wiki/ReverseEngineeringRFIDReader

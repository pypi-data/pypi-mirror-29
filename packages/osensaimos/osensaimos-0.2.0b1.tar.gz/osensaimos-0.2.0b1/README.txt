===============
OsensaIMOS
===============

Python module for interfacing with the OSENSA IMOS.

Refer to https://github.com/osensa/osensaimos for source code and examples.

*History*
---------
*Release 0.2.0b1:*

- Add saveToFlash option for start stream method
- Add method for saving calibration to file
- Add method for loading calibration from file

*Release 0.1.9b1:*

- Revert back to Python 3 support
- Integrate start_stream() logic into osensaimos library

*Release 0.1.8b1:*

- Adjust code to support Python 2 instead of 3
- Add start_stream() method to hello_world.py example

*Release 0.1.7b1:*

- Fix 'no atrribute' bug when using update_crc()
- Fix bugs with set_baudrate() logic

*Release 0.1.6b1:*

- Add method to get device firmware version
- Adjust dump_calibration() output format

*Release 0.1.5b1:*

- Fix minor bugs

*Release 0.1.4b1:*

- Add new custom modbus actions

*Release 0.1.3b1:*

- Add stream mode bug fixes and parse logic

*Release 0.1.2b1:*

- Restructure package and add example file
 
*Release 0.1.1b1:*

- Initial release

*Release 0.1.0b1:*

- Test release
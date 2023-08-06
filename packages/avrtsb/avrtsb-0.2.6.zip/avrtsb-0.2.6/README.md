About AVRTSB
============

AVRTSB is Python implementation of TinySafeBoot - A tiny and safe
Bootloader for AVR-ATtinys and ATmegas [1]. AVRTSB version 0.2
now supports make custom firmwares. If you want compile the
firmware yourself, please download from [1].

The console script run with the command pytsb. For more
information run: pytsb --help 

The benefit of AVRTSB is automatic reset of MCU with DTR or RTS line.
The second line is set to HIGH value (+12V) for power RS232<->TTL
convertor directly from serial port.  All parameters are given only
from command line without user interraction. This makes AVRTSB perfect
for integration with IDE for automatic upload new firmware after
compilation. 

TinySafeBoot is great bootloader bacause of:
  1) Small size - only 512 byte
  2) Software emulated serial interface a thus configurable for use
     with all MCU pins.
  3) Secure access by password

More information can be found [1]. 


[1] Original website of TinySafeBoot 
    http://jtxp.org/tech/tinysafeboot_en.htm


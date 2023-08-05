=======
Carioca
=======

Carioca is a variation of Samba or, in the present case, of SAM-BA.
SAM-BA is a full-blown in-system programmer developed and distributed
by Atmel to support bootstrapping their various SAM microcontrollers.
SAM-BA is proprietary, meaning that (most) of the source code is
unavailable to SAM-BA users.  Thus, if something breaks there, only
Atmel can fix the problem.

In contrast, Carioca is a minimal and open-source tool with similar
goals as SAM-BA.  It is minimal in the sense that it does not have any
of the complex code required to initialize hardware components such as
DRAM or to program flash memory.  Instead Carioca provides just enough
support to enable booting a primary bootloader and from there an
operating system such as Linux.  All flash programming etc. can then
be done from within the target's operating system.

Carioca has two modes: script mode and terminal-emulation mode.  It
starts out in script-mode where it executes zero or more scripts
stored in files.  There is also an interactive script mode where a
user can type commands interactively in a terminal.  Once the scripts
are done, Carioca usually switches into terminal-emulation mode.  In
this mode, Carioca simply passes the serial traffic from the target's
serial interface to the terminal Carioca was started in.  This enables
a user to observe the boot process of the target's operating system,
to log in and to execute commands as needed.

With these two modes, Carioca enables bootstraping a SAM
microcontroller through a single serial interface (such as the Debug
serial port), rather than the two ports typically required with SAM-BA
(Debug serial port and USB serial interface).

Carioca is written entirely in Python 3 and the scripting language has
been influenced by another, now defunct Python project called Sam_I_Am
(the two projects share no actual code, though, and their scripts are
not compatible).

Quick start
-----------

1. Install with::

	pip install --user carioca

   (or use "pip3" if that's the version providing Python 3).

2. Connect a target board with a SAM microcontroller to your computer
   using either its Debug serial port or the USB serial port.  On
   Linux, the former would typically show up as device **/dev/ttyUSB0**,
   the latter as **/dev/ttyACM0**.

3. If the target's serial port shows up as **/dev/ttyUSB0** on your
   computer and the target's serial port speed is **115,200 baud**, then
   start Carioca like this::

	~/.local/bin/carioca

   You can use option -p to specify a non-default serial port (such as
   "**-p /dev/ttyACM0**") and the -b option to specify a non-default
   baudrate (such as "**-b 57600**").

4. Power up the target board.  Assuming your target has not been setup
   for automatic booting yet, you should see a "**RomBOOT**" prompt.  If so,
   continue.

5. Quit Carioca's terminal emulator by typing "**Ctrl-] quit**", followed
   by the **Enter** key.

6. Start Carioca's interactive script mode with::

	~/.local/bin/carioca -

   This will give you a "**carioca$**" prompt. You can type "**help**" to get
   a list of available commands.  When executing the first command
   requiring interaction with the target, Carioca report's the target's
   SAM-BA Monitor version.  For example::

	carioca$ writeb 0x200000 42

   will write the value 42 to memory location 0x200000 and respond with::

	Connected to SAM-BA Monitor v1.1 Jul 31 2015 15:09:09

   Typically, you'll want to send the primary bootstrap loader to
   the microcontroller's SRAM and then start execution.  This could be
   achieved with::

	carioca$ sendimg 0x200000 "at91bootstrap.bin"
	carioca$ go 0x200000

   As soon as the "**go**" command is executed, Carioca will switch to
   terminal-emulation mode so you can observe the boot process and
   interact with the target as needed.

7. When you get tired if playing with the target system, type
   "**Ctrl-] quit**", followed by the **Enter** key to quit Carioca.
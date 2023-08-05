#!/usr/bin/env python
#
# The MIT License (MIT)
#
# Copyright (c) 2016, 2018 eGauge Systems LLC
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
from __future__ import print_function

import argparse
import atexit
import os
import re
import select
import sys

from serial import Serial

from . import SAM_BA
from . import TTY
from . import commands
from .version import __version__

PROMPT = 'carioca$ '
samba = None
parser = None
args = None

# Python3 calls input what Python 2 calls raw_input...
try:
    input = raw_input
except NameError:
    pass

def execute_script(serial, script, scope):
    """Returns True if script ended with a 'go' command."""
    def get_samba():
        global samba
        if samba is None:
            samba = SAM_BA.Monitor(serial)
            try:
                version = samba.version()
            except SAM_BA.Error:
                print('%s: SAM-BA communication failed --- '
                      'is target at ROMboot prompt?' %
                      (parser.prog), file=sys.stderr)
                sys.exit(1)
            print('Connected to SAM-BA Monitor: %s' % version)
        return samba

    script_dir = os.getcwd()
    if hasattr(script, 'name'):
        filename = script.name
        if os.path.exists(filename):
            script_dir = os.path.dirname(filename)
    scope['SCRIPTDIR'] = script_dir

    line_number = 0
    cmd = ''
    if script.isatty():
        os.write(script.fileno(), PROMPT.encode('utf-8'))
    for line in script:
        line_number += 1
        cmd += line.strip(' \t\r\n')
        if len(cmd) < 1:
            continue
        if cmd[0] == '#':	# comment
            cmd = ''
            continue
        if cmd[len(cmd) - 1] == '\\':
            cmd = cmd[0:len(cmd) - 1]
        else:
            try:
                commands.execute(scope, get_samba, cmd, args.print_commands)
            except commands.Error:
                print('%s:%u: Error: %s' % \
                      (script.name, line_number, sys.exc_info()[1]),
                      file=sys.stderr)
                return False
            except commands.Command_Done as e:
                if e.args[0] == 'quit':
                    return False
                elif e.args[0] == 'go':
                    return True
                else:
                    print('%s: unknown Command_Done %s' % (parser.prog, e))
                    return False
            cmd = ''
        if script.isatty():
            os.write(script.fileno(), PROMPT.encode('utf-8'))

def open_script(filename):
    if filename == '-':
        script = sys.stdin
    elif os.path.isfile(filename):
        script = open(filename, 'r')
    else:
        script = open(filename + '.carioca', 'r')
    return script

def terminal_command(serial, scope):
    """Execute an interactively typed command.  Returns True if terminal
    mode should be resumed, False if it should be exited."""
    while True:
        cmd = input('carioca> ').strip().split()
        if len(cmd) == 0:
            return True

        if cmd[0] == 'quit':
            sys.exit(0)
        elif cmd[0] == 'send':
            serial.write(b'\x1d')
            return True
        elif cmd[0] == 'exec' or cmd[0] == 'x':
            if len(cmd) != 2:
                print('Command `%s\' requires exactly one argument' % cmd[0],
                      file=sys.stderr)
                continue
            try:
                script = open_script(cmd[1])
            except:
                print('Failed to open script `%s\': %s' %
                      (cmd[1], sys.exc_info()[1]), file=sys.stderr)
                script = None
            if script is not None:
                print('')
                if execute_script(serial, script, scope):
                    # script ended with "go" command; go back to terminal mode
                    return True
        else:
            print('Available commands:\n'
                  '\t   quit: Exit carioca\n'
                  '\t exec F: Execute commands in file F or in F.carioca\n'
                  '\t    x F: Shorthand for `exec\'.\n'
                  '\t   send: Send Ctrl-] character\n'
                  '\t<Enter>: Return to terminal-emulation mode')

def terminal_mode(serial, scope):
    print(79*'-' + '\n' +
          'Entering terminal-emulation mode (exit with: Ctrl-] quit):\n' +
          79*'-')

    ctty_mode = TTY.Mode(0)
    atexit.register(ctty_mode.restore)
    ctty_mode.set_raw()
    stdin_fd = sys.stdin.fileno()
    serial_fd = serial.fileno()
    while True:
        # select.select() is the most portable version and we're only dealing
        # with two file descriptors, so scalability is not a concern:
        res = select.select([serial_fd, stdin_fd], [], [])
        if stdin_fd in res[0]:
            data = os.read(stdin_fd, 128)
            if len(data) == 1 and bytearray(data)[0] == 0x1d:
                # User typed Ctrl-]
                ctty_mode.restore()
                print('')
                if not terminal_command(serial, scope):
                    return
                ctty_mode.set_raw()
            else:
                serial.write(data)
        if serial_fd in res[0]:
            ret = os.read(serial_fd, 128)
            os.write(1, ret)

def main():
    global parser, args

    script_help = commands.help_text()
    parser = argparse.ArgumentParser(
        description='Carioca is an open-source variant of Atmel\'s SAM-BA '
        'utility.\n'
        'It provides scriptable support for interacting with an Atmel\n'
        'microcontroller\'s SAM-BA Monitor through a serial interface\n'
        '(serial-over-USB or direct serial port, such as the Debug serial\n'
        'port found on most Atmel microcontrollers).\n\n'
        'Once a "go" command is issued, Carioca enters terminal-emulation\n'
        'mode.  This enables interacting with the target system as needed.\n'
        'To exit terminal-emulation mode, use Ctrl-] followed by "quit".\n\n'
        'Commands can be stored in a script file or can be typed\n'
        'interactively when using a single dash (`-\') as the script name.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='The syntax for scripts is as follows:\n\n' + script_help)
    parser.add_argument('script_or_assignment',
                        help='Filename of script to execute or a variable '
                        'assignment of the form NAME=VALUE.',
                        nargs='*')
    parser.add_argument('-p', '--serial-port',
                        help='Name of the serial port to open.',
                        nargs='?', default='/dev/ttyUSB0')
    parser.add_argument('-b', '--baud-rate',
                        help='Baudrate to use with serial-port.',
                        nargs='?', type=int, default=115200)
    parser.add_argument('-s', '--set', help='Set variable NAME to value VAL.',
                        nargs=2, action='append', metavar=('NAME', 'VAL'))
    parser.add_argument('-T', '--no-terminal-mode',
                        help='Don\'t enter terminal mode after a "go" '
                        'command.', action='store_true', default=False)
    parser.add_argument('-V', '--version',
                        help='Display the version number of carioca.',
                        action='store_true', default=False)
    parser.add_argument('-X', '--disable-xmodem',
                        help='Do not use XMODEM protocol to send/receive data. '
                        'This option is necessary when connecting to the '
                        'target via its USB device port.  '
                        'Do not use this option when connecting to the '
                        'target via its UART/DBGU port.', action='store_true',
                        default=False)
    parser.add_argument('-x', '--print-commands',
                        help='Print commands and their arguments as they are '
                        'executed.', action='store_true', default=False)
    args = parser.parse_args()

    if args.version:
        print('carioca v' + __version__)
        sys.exit(0)

    try:
        serial = Serial(port=args.serial_port, baudrate=args.baud_rate,
                        exclusive=True)
    except:
        print('%s: unable to open serial port %s: %s' %
              (parser.prog, args.serial_port, sys.exc_info()[1]))
        sys.exit(1)
    scope = {}	# variable scope

    SAM_BA.USE_XMODEM = not args.disable_xmodem

    num_scripts = 0
    for assignment_or_script in args.script_or_assignment:
        m = re.match(r'([a-z_][a-z_0-9]*)=(.*)', assignment_or_script,
                     re.IGNORECASE)
        if m:
            name = m.group(1)
            value = m.group(2)
            scope[name] = value
        else:
            num_scripts += 1
            script = open_script(assignment_or_script)
            if execute_script(serial, script, scope):
                if not args.no_terminal_mode:
                    terminal_mode(serial, scope)
                break

    if num_scripts == 0:
        terminal_mode(serial, scope)

if __name__ == '__main__':
    main()

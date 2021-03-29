#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2021, M6SIG

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Teletype stream utility:
# A Teletype cipher research helping tool.
#

import sys
import textwrap
import argparse
from pathlib import Path

'''ASCII/TTY coding conversion data.'''

# Constants for asc2tty array
INVC   = 255    # invalid character mapping

# / represents "Null"
# 3 represents "\r"
# 4 represents "New Line"
# 5 represents Figure Shift
# 8 represents Letter Shift
# 9 represents "Space"
tty2bpname = [
    '/', 'T', '3', 'O', '9', 'H', 'N', 'M',
    '4', 'L', 'R', 'G', 'I', 'P', 'C', 'V',
    'E', 'Z', 'D', 'B', 'S', 'Y', 'F', 'X',
    'A', 'W', 'J', '5', 'U', 'Q', 'K', '8']


# For converting Bletchley Park teleprinter representation
# back to 5-bits TTY code.
#
# 5 LSBs are significant.
# 0xff indicates invalid character mapping.
bpname2tty = [
 INVC, INVC, INVC, INVC, INVC, INVC, INVC, INVC, INVC, INVC,
 INVC, INVC, INVC, INVC, INVC, INVC, INVC, INVC, INVC, INVC,
 INVC, INVC, INVC, INVC, INVC, INVC, INVC, INVC, INVC, INVC,
 INVC, INVC, INVC, INVC, INVC, INVC, INVC, INVC, INVC, INVC,
#                                             /
 INVC, INVC, INVC, INVC, INVC, INVC, INVC,    0, INVC, INVC,
#   2     3     4     5     6     7     8     9     :     ;
 INVC,    2,    8,   27, INVC, INVC,   31,    4, INVC, INVC,
#   <     =     >     ?     @     A     B     C     D     E
 INVC, INVC, INVC, INVC, INVC,   24,   19,   14,   18,   16,
#   F     G     H     I     J     K     L     M     N     O
   22,   11,    5,   12,   26,   30,    9,    7,    6,    3,
#   P     Q     R     S     T     U     V     W     X     Y
   13,   29,   10,   20,    1,   28,   15,   25,   23,   21,
#   Z
   17]


def tty2blyprintout(s):
    
    result = []
    for char in s:
        char = tty2bpname[ord(char)]
        result.append(char)

    return ''.join(result)


def blyprintout2tty(s):

    result = []
    for char in s:
        # Drop MSB and convert
        if char < len(bpname2tty):
            char = bpname2tty[char]

            # Convert if valid
            if char != INVC:
                # Emit the converted char
                result.append(chr(char))

    return ''.join(result)


class gather_args(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not 'arg_sequence' in namespace:
            setattr(namespace, 'arg_sequence', [])
        prev = namespace.arg_sequence
        prev.append((self.dest, values))
        setattr(namespace, 'arg_sequence', prev)


def validate_args(infile):
    if not infile.is_file():
        sys.exit('"{}" is not a file.'.format(infile))


# Main entry point when called as an executable script.
if __name__ == '__main__':

    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(
        prog='python3 ttystreamutil.py',
        epilog=textwrap.dedent('''\
        Example:
          python3 ttystreamutil.py --printout <input file> <output file>
          python3 ttystreamutil.py --maketape <input file> <output file>
          '''),
        add_help=True,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    # maincommandoption = parser.add_mutually_exclusive_group()
    parser.add_argument('--printout', action=gather_args, nargs=2,
                        metavar=('<input file>', '<output file>'),
                        help='''Read input file in Baudot code and output the Bletchley Park teleprinter format equivalent to the screen and output file.''')

    parser.add_argument('--maketape', action=gather_args, nargs=2,
                        metavar=('<input file>', '<output file>'),
                        help='''Read input file in Bletchley Park teleprinter format equivalent and output file in Baudot code.''')


    # Parse the command-line arguments. Need to create empty arg_sequence
    # in case no command-line arguments were included.
    args = parser.parse_args()
    if not 'arg_sequence' in args:
        setattr(args, 'arg_sequence', [])
    cmd = ''
    opt = ''


    if len(args.arg_sequence) == 1:
        cmd = args.arg_sequence[0][0]
        opt = args.arg_sequence[0][1]
    else:
        sys.stderr.write("Wrong options!\npython3 ttystreamutil.py --help or -h for usage info.\n")
        exit(1)


    if cmd == 'printout':
        baudot_file = Path(opt[0])
        output_file = opt[1]
        validate_args(baudot_file)

        input_bcode = []
        print("Reading TTY tape file", baudot_file, "...")
        with baudot_file.open('rb') as f_in:
            while f_in.peek():
                input_bcode.append(f_in.read(1))

        bp_print_out = tty2blyprintout(input_bcode)

        with open(output_file, 'w') as f_out:
            f_out.write(bp_print_out)
        print("Tape in bletchley park format written to:", output_file)
        print("The tape read:", bp_print_out)


    elif cmd == 'maketape':
        input_file = Path(opt[0])
        output_file = opt[1]
        validate_args(input_file)
        input_code = []
        print("Reading", input_file,"...")
        with input_file.open('rb') as f_input:
            while f_input.peek():
                input_code.append(ord(f_input.read(1)))

        input_baudot = blyprintout2tty(input_code)

        print("Punching...")

        with open(output_file, 'w') as f_out:
            f_out.write(input_baudot)
        print("TTY tape written to:", output_file)

    else:
        sys.stderr.write("Wrong options!\npython3 ttystreamutil.py --help or -h for usage info.\n")
        exit(1)

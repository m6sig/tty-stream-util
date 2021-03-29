# tty-stream-util
A teletype cipher research helping tool.

Convert tty stream to a format that the teleprinter cipher researcher at Bletchley Park used during the WW2 and back to tty stream.

# Usage
```
python3 ttystreamutil.py [-h] [--printout <input file> <output file>]
                                [--maketape <input file> <output file>]

optional arguments:
  -h, --help            show this help message and exit
  --printout <input file> <output file>
                        Read input file in Baudot code and output the
                        Bletchley Park teleprinter format equivalent to the
                        screen and output file.
  --maketape <input file> <output file>
                        Read input file in Bletchley Park teleprinter format
                        equivalent and output file in Baudot code.

Example:
  python3 ttystreamutil.py --printout <input file> <output file>
  python3 ttystreamutil.py --maketape <input file> <output file>
```

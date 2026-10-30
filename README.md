# Messy Spreadsheet Cleaner

A Python script that turns a messy customer spreadsheet (CSV or Excel) into a clean, consistent file and prints a short report of what it fixed.

## What it fixes
- Extra spaces and inconsistent capital letters in names
- Emails converted to lowercase
- Phone numbers standardised (for example +254 722 111 222 becomes 0722111222)
- Dates in several formats, including real Excel dates, converted to YYYY-MM-DD
- Money values like "Sh 1,200" converted to 1200.00
- Blank rows and duplicate customers removed

## Supported files
- Input: .csv, .xlsx
- Output: .csv, .xlsx (you can also convert, for example CSV in and Excel out)

## Usage
    python clean.py messy.csv tidy.csv
    python clean.py messy.xlsx tidy.xlsx
    python clean.py messy.csv tidy.xlsx

Excel files need one library:

    pip install openpyxl

CSV files need no extra libraries.

## Example
See messy.csv and messy.xlsx (before) and tidy.csv and tidy.xlsx (after) in this repo.

## Notes
- Dates such as 05/10/2026 are read as day first (5 October 2026).
- Phone formatting follows the Kenyan style (starting with 0).
- Column names are matched without case, so "Name" and "name" both work.

Built with Python 3 on an Android phone.

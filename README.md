# Messy CSV Cleaner

A Python script that turns a messy customer spreadsheet (CSV) into a clean, consistent file and prints a short report of what it fixed. It needs no extra libraries.

## What it fixes
- Extra spaces and inconsistent capital letters in names
- Emails converted to lowercase
- Phone numbers standardised (for example +254 722 111 222 becomes 0722111222)
- Dates in several formats converted to YYYY-MM-DD
- Money values like "Sh 1,200" converted to 1200.00
- Blank rows and duplicate customers removed

## Usage
    python clean.py messy.csv tidy.csv

## Example
See messy.csv (before) and tidy.csv (after) in this repo.

## Notes
- Dates such as 05/10/2026 are read as day first (5 October 2026).
- Phone formatting follows the Kenyan style (starting with 0).

Built with Python 3 on an Android phone.

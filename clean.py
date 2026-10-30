import csv
import re
import sys
from datetime import datetime, date

DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d %b %Y", "%b %d, %Y"]
FIELDS = ["name", "email", "phone", "signup_date", "amount"]
NEED_OPENPYXL = "Excel files need openpyxl. Install it with: pip install openpyxl"


def to_text(v):
    if v is None:
        return ""
    if isinstance(v, (datetime, date)):
        return v.strftime("%Y-%m-%d")
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


def clean_name(v):
    return " ".join(v.split()).title()


def clean_email(v):
    return v.strip().lower()


def clean_phone(v):
    digits = re.sub(r"\D", "", v)
    if digits.startswith("254"):
        digits = "0" + digits[3:]
    elif len(digits) == 9:
        digits = "0" + digits
    return digits


def clean_date(v):
    v = v.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(v, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return ""


def clean_amount(v):
    v = re.sub(r"[^\d.]", "", v)
    return f"{float(v):.2f}" if v else ""


def read_rows(path):
    if path.lower().endswith((".xlsx", ".xlsm")):
        try:
            from openpyxl import load_workbook
        except ImportError:
            sys.exit(NEED_OPENPYXL)
        sheet = load_workbook(path, data_only=True).active
        data = list(sheet.iter_rows(values_only=True))
        if not data:
            return []
        header = [to_text(h).strip().lower() for h in data[0]]
        return [{h: to_text(v) for h, v in zip(header, row)} for row in data[1:]]
    with open(path, newline="", encoding="utf-8-sig") as f:
        return [
            {k.strip().lower(): (v or "") for k, v in r.items() if k}
            for r in csv.DictReader(f)
        ]


def write_rows(path, rows):
    if path.lower().endswith(".xlsx"):
        try:
            from openpyxl import Workbook
        except ImportError:
            sys.exit(NEED_OPENPYXL)
        wb = Workbook()
        ws = wb.active
        ws.title = "Cleaned"
        ws.append(FIELDS)
        for r in rows:
            when = datetime.strptime(r["signup_date"], "%Y-%m-%d").date() if r["signup_date"] else None
            amount = float(r["amount"]) if r["amount"] else None
            ws.append([r["name"], r["email"], r["phone"], when, amount])
        for row in ws.iter_rows(min_row=2):
            row[3].number_format = "yyyy-mm-dd"
            row[4].number_format = "0.00"
        for col, width in zip("ABCDE", [24, 32, 16, 14, 12]):
            ws.column_dimensions[col].width = width
        wb.save(path)
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main(src, dst):
    rows = read_rows(src)
    report = {"rows read": len(rows), "blank rows removed": 0,
              "duplicates removed": 0, "dates not recognised": 0}
    cleaned, seen = [], set()

    for r in rows:
        if not any(v.strip() for v in r.values()):
            report["blank rows removed"] += 1
            continue
        row = {
            "name": clean_name(r.get("name", "")),
            "email": clean_email(r.get("email", "")),
            "phone": clean_phone(r.get("phone", "")),
            "signup_date": clean_date(r.get("signup_date", "")),
            "amount": clean_amount(r.get("amount", "")),
        }
        if r.get("signup_date", "").strip() and not row["signup_date"]:
            report["dates not recognised"] += 1
        key = row["email"] or row["phone"]
        if key and key in seen:
            report["duplicates removed"] += 1
            continue
        seen.add(key)
        cleaned.append(row)

    write_rows(dst, cleaned)
    report["rows saved"] = len(cleaned)
    print("Cleaning report")
    for k, v in report.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean.py input.(csv|xlsx) output.(csv|xlsx)")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])

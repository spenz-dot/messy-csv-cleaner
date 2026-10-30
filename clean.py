import csv
import re
import sys
from datetime import datetime

DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d %b %Y", "%b %d, %Y"]
FIELDS = ["name", "email", "phone", "signup_date", "amount"]


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


def main(src, dst):
    with open(src, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    report = {"rows read": len(rows), "blank rows removed": 0,
              "duplicates removed": 0, "dates not recognised": 0}
    cleaned, seen = [], set()

    for r in rows:
        if not any((v or "").strip() for v in r.values()):
            report["blank rows removed"] += 1
            continue
        row = {
            "name": clean_name(r["name"]),
            "email": clean_email(r["email"]),
            "phone": clean_phone(r["phone"]),
            "signup_date": clean_date(r["signup_date"]),
            "amount": clean_amount(r["amount"]),
        }
        if r["signup_date"].strip() and not row["signup_date"]:
            report["dates not recognised"] += 1
        key = row["email"] or row["phone"]
        if key and key in seen:
            report["duplicates removed"] += 1
            continue
        seen.add(key)
        cleaned.append(row)

    with open(dst, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(cleaned)

    report["rows saved"] = len(cleaned)
    print("Cleaning report")
    for k, v in report.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean.py input.csv output.csv")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])

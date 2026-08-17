#!/usr/bin/env python3
"""Convert one or more CSV files to .xlsx, writing output to ~/Downloads."""
import csv
import sys
from pathlib import Path

from openpyxl import Workbook

DOWNLOADS = Path.home() / "Downloads"

# Tried in order; utf-8-sig also matches plain utf-8. cp1252 covers the vast
# majority of Excel-exported CSVs from Western European locales (e.g. "ä").
ENCODINGS = ["utf-8-sig", "cp1252"]


def open_text(csv_path: Path):
    for encoding in ENCODINGS:
        try:
            f = csv_path.open(newline="", encoding=encoding)
            f.read()
            f.seek(0)
            return f
        except UnicodeDecodeError:
            f.close()
    # Last resort: latin-1 never raises, since every byte is a valid code point.
    return csv_path.open(newline="", encoding="latin-1")


def convert(csv_path: Path) -> Path:
    wb = Workbook()
    ws = wb.active
    with open_text(csv_path) as f:
        sniffer = csv.Sniffer()
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = sniffer.sniff(sample, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel
        for row in csv.reader(f, dialect):
            ws.append(row)

    out_path = DOWNLOADS / (csv_path.stem + ".xlsx")
    wb.save(out_path)
    return out_path


def main(argv: list[str]) -> int:
    if not argv:
        print("Usage: csv_to_xlsx.py file1.csv [file2.csv ...]", file=sys.stderr)
        return 1

    DOWNLOADS.mkdir(exist_ok=True)
    for arg in argv:
        csv_path = Path(arg)
        if csv_path.suffix.lower() != ".csv":
            print(f"Skipping non-CSV file: {csv_path}", file=sys.stderr)
            continue
        if not csv_path.exists():
            print(f"File not found: {csv_path}", file=sys.stderr)
            continue
        out_path = convert(csv_path)
        print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

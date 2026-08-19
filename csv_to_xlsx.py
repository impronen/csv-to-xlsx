#!/usr/bin/env python3
"""Convert one or more CSV files to .xlsx, writing output next to each source
file (falling back to ~/Downloads if that folder isn't writable)."""
import csv
import sys
import time
from pathlib import Path

from openpyxl import Workbook

DOWNLOADS = Path.home() / "Downloads"

# Tried in order; utf-8-sig also matches plain utf-8. cp1252 covers the vast
# majority of Excel-exported CSVs from Western European locales (e.g. "ä").
ENCODINGS = ["utf-8-sig", "cp1252"]

# Cloud-sync placeholder files (OneDrive, etc.) are downloaded on first read.
# While that download is in flight, macOS can surface it as EDEADLK instead
# of just blocking, so retry a few times before giving up.
CLOUD_MATERIALIZE_RETRIES = 10
CLOUD_MATERIALIZE_DELAY = 1.0


def _read_with_retry(f):
    for attempt in range(CLOUD_MATERIALIZE_RETRIES):
        try:
            data = f.read()
            f.seek(0)
            return data
        except OSError as e:
            if e.errno == 11 and attempt < CLOUD_MATERIALIZE_RETRIES - 1:
                time.sleep(CLOUD_MATERIALIZE_DELAY)
                continue
            raise


def open_text(csv_path: Path):
    for encoding in ENCODINGS:
        try:
            f = csv_path.open(newline="", encoding=encoding)
            _read_with_retry(f)
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

    out_path = csv_path.with_suffix(".xlsx")
    try:
        wb.save(out_path)
    except (PermissionError, OSError):
        DOWNLOADS.mkdir(exist_ok=True)
        out_path = DOWNLOADS / (csv_path.stem + ".xlsx")
        wb.save(out_path)
    return out_path


def main(argv: list[str]) -> int:
    if not argv:
        print("Usage: csv_to_xlsx.py file1.csv [file2.csv ...]", file=sys.stderr)
        return 1

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

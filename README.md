# csv-to-xlsx

Converts CSV files to XLSX, writing the result to `~/Downloads`. Used as a
Finder Quick Action (right-click a `.csv` file → Quick Actions → Convert CSV
to XLSX).

## Setup

```
python3 -m venv .venv
.venv/bin/pip install openpyxl
```

## Usage (CLI)

```
.venv/bin/python3 csv_to_xlsx.py file1.csv file2.csv ...
```

## Setting up the Finder Quick Action

1. Open **Automator** → File → New → **Quick Action**.
2. Set "Workflow receives current" to **files or folders** in **Finder**.
3. Optionally set "Image" to something recognizable, and restrict file type
   to CSV via the checkbox/dropdown that appears (or leave unrestricted; the
   script itself skips non-CSV input).
4. In the search box, find the **Run Shell Script** action and drag it into
   the workflow area.
5. Set Shell to `/bin/zsh`, and "Pass input" to **as arguments**.
6. Paste this into the script box, replacing `/path/to/csv-to-xlsx` with
   wherever you cloned this repo (e.g. `~/code/csv-to-xlsx`):

   ```
   /path/to/csv-to-xlsx/.venv/bin/python3 \
     /path/to/csv-to-xlsx/csv_to_xlsx.py "$@"
   ```

7. Save as **Convert CSV to XLSX**.
8. Right-click any `.csv` file in Finder → Quick Actions → Convert CSV to
   XLSX. The `.xlsx` file appears in `~/Downloads`.

# csv-to-xlsx

Converts CSV files to XLSX, writing the result to `~/Downloads`. Used as a
Finder Quick Action (right-click a `.csv` file → Quick Actions → Convert CSV
to XLSX).

## Setup — step by step (no coding experience needed)

This turns into a right-click menu item in Finder. It takes about 5 minutes,
all one-time setup. You'll be pasting a few commands into the **Terminal**
app — that's expected, just follow along exactly.

### 1. Download this project

- Click the green **Code** button near the top of this page → **Download
  ZIP**.
- Find the downloaded ZIP (usually in your Downloads folder) and double-click
  it to unzip. You'll get a folder named `csv-to-xlsx-main`.
- Move that folder somewhere permanent, e.g. your Documents folder. Don't
  leave it in Downloads or delete it later — the Quick Action will need it to
  stay in place.

### 2. Open Terminal

- Press `⌘ Space`, type `Terminal`, press Enter. A window with text opens —
  this is normal, don't worry.

### 3. Go to the folder

- Type `cd ` (with a trailing space) into Terminal — don't press Enter yet.
- Now drag the `csv-to-xlsx-main` folder from Finder straight into the
  Terminal window. It'll paste the folder's path automatically.
- Press Enter.

### 4. Install the requirements

Paste this into Terminal and press Enter (macOS already includes everything
needed to run this — this just adds one small piece the script depends on):

```
python3 -m venv .venv && .venv/bin/pip install openpyxl
```

This may take a minute. When it's done, you'll see your prompt again.

### 5. Get the folder's exact path

Type this and press Enter:

```
pwd
```

Copy the line it prints (something like `/Users/yourname/Documents/csv-to-xlsx-main`).
You'll paste this into Automator in the next step — keep it handy.

### 6. Create the Finder Quick Action

1. Open **Automator** (⌘ Space, type `Automator`, press Enter).
2. **File → New**, then choose **Quick Action**, click **Choose**.
3. At the top of the workflow, set "Workflow receives current" to **files or
   folders** in **Finder**.
4. In the search box on the left, type `Run Shell Script`, and drag that
   action into the empty area on the right.
5. In the Run Shell Script box, set **Shell** to `/bin/zsh`, and **Pass
   input** to **as arguments**.
6. Delete any placeholder text in the script box and paste this in,
   replacing `PASTE_YOUR_PATH_HERE` with the path you copied in step 5
   (keep the quotes around `"$@"` exactly as shown):

   ```
   PASTE_YOUR_PATH_HERE/.venv/bin/python3 PASTE_YOUR_PATH_HERE/csv_to_xlsx.py "$@"
   ```

   For example, if `pwd` printed `/Users/yourname/Documents/csv-to-xlsx-main`,
   the line becomes:

   ```
   /Users/yourname/Documents/csv-to-xlsx-main/.venv/bin/python3 /Users/yourname/Documents/csv-to-xlsx-main/csv_to_xlsx.py "$@"
   ```

7. **File → Save**, name it **Convert CSV to XLSX**, click Save.

### 7. Use it

Right-click (or two-finger click on trackpad) any `.csv` file in Finder →
**Quick Actions** → **Convert CSV to XLSX**. The `.xlsx` version appears in
your **Downloads** folder a moment later.

Optional: you can also assign a keyboard shortcut to it in **System
Settings → Keyboard → Keyboard Shortcuts → Services**.

---

## For developers

### CLI usage

```
python3 -m venv .venv
.venv/bin/pip install openpyxl
.venv/bin/python3 csv_to_xlsx.py file1.csv file2.csv ...
```

### Notes on the Quick Action setup

Same as above, but if you cloned via `git clone` instead of downloading the
ZIP, substitute your clone's path for `PASTE_YOUR_PATH_HERE`.

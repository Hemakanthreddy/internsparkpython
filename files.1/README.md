# File Automation Tool

A Python command-line tool that automates common file-management chores:
**sorting** files into folders by extension, **renaming** files in bulk,
and **cleaning** a folder of empty/duplicate files. Every run is logged to
a `file_organizer.log` file inside the target folder, and every operation
is wrapped in exception handling so a single bad file never crashes the
whole run.

## Features

| Action   | What it does                                                                 |
|----------|-------------------------------------------------------------------------------|
| `sort`   | Moves each file into a sub-folder named after its extension (`.jpg` -> `jpg/`) |
| `rename` | Renames all files sequentially: `<prefix>_001.ext`, `<prefix>_002.ext`, ...    |
| `clean`  | Deletes empty files and duplicate files (matched by SHA-256 content hash)      |
| `all`    | Runs sort, then clean, in one pass                                            |

## Requirements

- Python 3.7+
- No external dependencies (uses only the standard library: `os`, `shutil`,
  `hashlib`, `logging`, `argparse`, `sys`, `datetime`)

## Usage

### 1. Interactive mode (menu-driven, asks for input)

```bash
python file_organizer.py
```

You'll be prompted for a folder path and asked to choose an operation
from a menu (1-4).

### 2. Command-line / scripted mode

```bash
python file_organizer.py --path ./my_folder --action sort
python file_organizer.py --path ./my_folder --action rename --prefix invoice
python file_organizer.py --path ./my_folder --action clean
python file_organizer.py --path ./my_folder --action all
```

| Flag       | Description                                            |
|------------|---------------------------------------------------------|
| `--path`   | Target directory to operate on (required in CLI mode)   |
| `--action` | `sort`, `rename`, `clean`, or `all`                      |
| `--prefix` | Prefix used for the `rename` action (default: `file`)   |

## Sample Input / Output

**Input folder (`sample_data/`) before running anything:**

```
sample_data/
├── report.txt        (contains "Report Q1")
├── report_copy.txt    (duplicate of report.txt — same content)
├── notes.txt
├── script.py
├── photo.jpg
└── empty_file.txt     (0 bytes)
```

**Step 1 — Clean:**
```bash
$ python file_organizer.py --path ./sample_data --action clean
2026-07-17 02:33:26 | INFO    | Automation run started for folder: ./sample_data | action=clean
2026-07-17 02:33:26 | INFO    | Starting CLEAN operation on: ./sample_data
2026-07-17 02:33:26 | INFO    | Removed duplicate: 'report.txt' (same content as 'report_copy.txt')
2026-07-17 02:33:26 | INFO    | Removed empty file: 'empty_file.txt'
2026-07-17 02:33:26 | INFO    | CLEAN complete. Empty files removed: 1, Duplicates removed: 1
2026-07-17 02:33:26 | INFO    | Automation run finished.
```

**Step 2 — Rename (prefix "demo"):**
```bash
$ python file_organizer.py --path ./sample_data --action rename --prefix demo
2026-07-17 02:33:28 | INFO    | Starting RENAME operation on: ./sample_data (prefix='demo')
2026-07-17 02:33:28 | INFO    | Renamed 'notes.txt' -> 'demo_001.txt'
2026-07-17 02:33:28 | INFO    | Renamed 'photo.jpg' -> 'demo_002.jpg'
2026-07-17 02:33:28 | INFO    | Renamed 'report_copy.txt' -> 'demo_003.txt'
2026-07-17 02:33:28 | INFO    | Renamed 'script.py' -> 'demo_004.py'
2026-07-17 02:33:28 | INFO    | RENAME complete. Total renamed: 4
```

**Step 3 — Sort by extension:**
```bash
$ python file_organizer.py --path ./sample_data --action sort
2026-07-17 02:33:31 | INFO    | Starting SORT operation on: ./sample_data
2026-07-17 02:33:31 | INFO    | Moved 'demo_002.jpg' -> 'jpg/'
2026-07-17 02:33:31 | INFO    | Moved 'demo_003.txt' -> 'txt/'
2026-07-17 02:33:31 | INFO    | Moved 'demo_004.py' -> 'py/'
2026-07-17 02:33:31 | INFO    | Moved 'demo_001.txt' -> 'txt/'
2026-07-17 02:33:31 | INFO    | SORT complete. Moved: 4, Skipped: 0
```

**Final folder structure:**
```
sample_data/
├── file_organizer.log
├── jpg/
│   └── demo_002.jpg
├── py/
│   └── demo_004.py
└── txt/
    ├── demo_001.txt
    └── demo_003.txt
```

All of the above log lines are also written automatically to
`sample_data/file_organizer.log` — nothing needs to be copy-pasted by hand.

## Design notes

- **Exception handling**: every file operation (`os.rename`, `shutil.move`,
  `os.remove`, reading a file for hashing) is wrapped in a `try/except`
  so one problem file (permissions error, file in use, etc.) is logged
  and skipped rather than crashing the whole script.
- **Logging**: uses Python's built-in `logging` module with both a
  console handler and a file handler, so you get real-time feedback
  and a permanent audit trail.
- **User input**: supports both an interactive menu (`input()` prompts)
  for casual use, and `argparse` flags for scripting/automation/CI use.
- **Safety**: `sort` and `rename` never overwrite an existing file —
  they log a warning and skip instead.

## License

MIT — free to use, modify, and share.

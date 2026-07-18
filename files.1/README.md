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

<img width="1392" height="786" alt="Screenshot 2026-07-17 180540" src="https://github.com/user-attachments/assets/51f4666d-afe7-4247-8e8d-5ed126e4d772" />
<img width="1536" height="862" alt="Screenshot 2026-07-17 200709" src="https://github.com/user-attachments/assets/b250a15a-6726-492c-882e-a3531b47c1aa" />
<img width="1536" height="861" alt="Screenshot 2026-07-17 200604" src="https://github.com/user-attachments/assets/2ed7f830-bfc1-4a6e-8ffe-cdd2c5b257d9" />
<img width="1521" height="855" alt="Screenshot 2026-07-17 181405" src="https://github.com/user-attachments/assets/57138d46-7efc-4c22-bb3d-d98e97ec1e8b" />


All of the above log lines are also written automatically to
`sample/file_organizer.log` — nothing needs to be copy-pasted by hand.

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
## report
[InternSpark_Task1_File_Automation.docx](https://github.com/user-attachments/files/30153319/InternSpark_Task1_File_Automation.docx)


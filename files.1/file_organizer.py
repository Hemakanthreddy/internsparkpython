#!/usr/bin/env python3
"""
file_organizer.py
------------------
A command-line file automation tool that can:
  1. SORT   -> organize files in a folder into sub-folders by file extension
  2. RENAME -> batch rename files with a prefix + sequential numbering
  3. CLEAN  -> remove empty files and duplicate files (by content hash)

Every run writes a timestamped log entry to 'file_organizer.log' in the
target directory, and also prints progress to the console.

Author : Hemakanth
Usage  : python file_organizer.py
         (interactive menu) OR
         python file_organizer.py --path <dir> --action sort|rename|clean
"""

import os
import sys
import shutil
import hashlib
import logging
import argparse
from datetime import datetime


# --------------------------------------------------------------------------
# Logging setup
# --------------------------------------------------------------------------
def setup_logger(target_dir: str) -> logging.Logger:
    """Configure a logger that writes to both console and a log file
    stored inside the target directory."""
    logger = logging.getLogger("file_organizer")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()  # avoid duplicate handlers on repeated calls

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (log lives inside the folder being processed)
    try:
        log_path = os.path.join(target_dir, "file_organizer.log")
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except OSError as e:
        # If we can't write a log file (e.g. permissions), keep going with
        # console-only logging instead of crashing the whole program.
        logger.warning(f"Could not create log file in '{target_dir}': {e}")

    return logger


# --------------------------------------------------------------------------
# Core operations
# --------------------------------------------------------------------------
def sort_by_extension(target_dir: str, logger: logging.Logger) -> None:
    """Move each file into a sub-folder named after its extension.
    Files with no extension go into a folder called 'no_extension'."""
    logger.info(f"Starting SORT operation on: {target_dir}")
    moved_count = 0
    skipped_count = 0

    try:
        entries = os.listdir(target_dir)
    except OSError as e:
        logger.error(f"Cannot read directory '{target_dir}': {e}")
        return

    for name in entries:
        full_path = os.path.join(target_dir, name)

        # Skip directories, the log file itself, and hidden files
        if os.path.isdir(full_path) or name == "file_organizer.log" or name.startswith("."):
            continue

        try:
            _, ext = os.path.splitext(name)
            folder_name = ext[1:].lower() if ext else "no_extension"
            dest_folder = os.path.join(target_dir, folder_name)

            os.makedirs(dest_folder, exist_ok=True)
            dest_path = os.path.join(dest_folder, name)

            # Avoid overwriting a file that already exists at destination
            if os.path.exists(dest_path):
                logger.warning(f"Skipped '{name}': a file already exists in '{folder_name}/'")
                skipped_count += 1
                continue

            shutil.move(full_path, dest_path)
            logger.info(f"Moved '{name}' -> '{folder_name}/'")
            moved_count += 1

        except (OSError, shutil.Error) as e:
            logger.error(f"Failed to move '{name}': {e}")
            skipped_count += 1

    logger.info(f"SORT complete. Moved: {moved_count}, Skipped: {skipped_count}")


def rename_sequential(target_dir: str, logger: logging.Logger, prefix: str = "file") -> None:
    """Rename all files in the folder to '<prefix>_001.ext', '<prefix>_002.ext', etc.
    Keeps original extensions intact."""
    logger.info(f"Starting RENAME operation on: {target_dir} (prefix='{prefix}')")

    try:
        entries = sorted(
            f for f in os.listdir(target_dir)
            if os.path.isfile(os.path.join(target_dir, f)) and f != "file_organizer.log"
        )
    except OSError as e:
        logger.error(f"Cannot read directory '{target_dir}': {e}")
        return

    renamed_count = 0
    for index, name in enumerate(entries, start=1):
        old_path = os.path.join(target_dir, name)
        _, ext = os.path.splitext(name)
        new_name = f"{prefix}_{index:03d}{ext.lower()}"
        new_path = os.path.join(target_dir, new_name)

        try:
            if os.path.exists(new_path) and new_path != old_path:
                logger.warning(f"Skipped renaming '{name}': target '{new_name}' already exists")
                continue
            os.rename(old_path, new_path)
            logger.info(f"Renamed '{name}' -> '{new_name}'")
            renamed_count += 1
        except OSError as e:
            logger.error(f"Failed to rename '{name}': {e}")

    logger.info(f"RENAME complete. Total renamed: {renamed_count}")


def _file_hash(path: str, block_size: int = 65536) -> str:
    """Return the SHA-256 hash of a file's contents."""
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            sha256.update(block)
    return sha256.hexdigest()


def clean_files(target_dir: str, logger: logging.Logger) -> None:
    """Remove empty files and duplicate files (same content hash),
    keeping only the first occurrence of each duplicate set."""
    logger.info(f"Starting CLEAN operation on: {target_dir}")

    seen_hashes = {}
    removed_empty = 0
    removed_duplicates = 0

    try:
        entries = [
            f for f in os.listdir(target_dir)
            if os.path.isfile(os.path.join(target_dir, f)) and f != "file_organizer.log"
        ]
    except OSError as e:
        logger.error(f"Cannot read directory '{target_dir}': {e}")
        return

    for name in entries:
        full_path = os.path.join(target_dir, name)
        try:
            if os.path.getsize(full_path) == 0:
                os.remove(full_path)
                logger.info(f"Removed empty file: '{name}'")
                removed_empty += 1
                continue

            file_hash = _file_hash(full_path)
            if file_hash in seen_hashes:
                os.remove(full_path)
                logger.info(f"Removed duplicate: '{name}' (same content as '{seen_hashes[file_hash]}')")
                removed_duplicates += 1
            else:
                seen_hashes[file_hash] = name

        except (OSError, IOError) as e:
            logger.error(f"Failed to process '{name}': {e}")

    logger.info(
        f"CLEAN complete. Empty files removed: {removed_empty}, "
        f"Duplicates removed: {removed_duplicates}"
    )


# --------------------------------------------------------------------------
# Interactive CLI
# --------------------------------------------------------------------------
def interactive_menu() -> None:
    print("=" * 55)
    print(" FILE AUTOMATION TOOL - Sort / Rename / Clean")
    print("=" * 55)

    target_dir = input("Enter the folder path to operate on: ").strip()

    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory.")
        return

    logger = setup_logger(target_dir)
    logger.info(f"Session started by user for folder: {target_dir}")

    print("\nChoose an operation:")
    print("  1. Sort files into folders by extension")
    print("  2. Rename files sequentially (e.g. file_001.txt)")
    print("  3. Clean empty files and duplicates")
    print("  4. Run ALL (sort -> rename -> clean)")
    choice = input("Enter choice [1-4]: ").strip()

    try:
        if choice == "1":
            sort_by_extension(target_dir, logger)
        elif choice == "2":
            prefix = input("Enter filename prefix (default 'file'): ").strip() or "file"
            rename_sequential(target_dir, logger, prefix)
        elif choice == "3":
            clean_files(target_dir, logger)
        elif choice == "4":
            sort_by_extension(target_dir, logger)
            clean_files(target_dir, logger)
        else:
            print("Invalid choice. Please run the script again and pick 1-4.")
            logger.warning(f"User entered invalid menu choice: '{choice}'")
    except Exception as e:
        # Catch-all safety net so the whole script never crashes silently
        logger.error(f"Unexpected error during operation: {e}")
        print(f"An unexpected error occurred: {e}")
    finally:
        logger.info("Session ended.\n")


# --------------------------------------------------------------------------
# Non-interactive CLI (for automation / scripting / CI use)
# --------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Automate file sorting, renaming, and cleaning.")
    parser.add_argument("--path", help="Target directory to operate on")
    parser.add_argument("--action", choices=["sort", "rename", "clean", "all"], help="Operation to run")
    parser.add_argument("--prefix", default="file", help="Prefix to use for the rename action")
    args = parser.parse_args()

    # If no CLI args were given at all, fall back to the interactive menu
    if not args.path and not args.action:
        interactive_menu()
        return

    if not args.path or not os.path.isdir(args.path):
        print("Error: please provide a valid directory with --path")
        sys.exit(1)

    logger = setup_logger(args.path)
    logger.info(f"Automation run started for folder: {args.path} | action={args.action}")

    try:
        if args.action == "sort":
            sort_by_extension(args.path, logger)
        elif args.action == "rename":
            rename_sequential(args.path, logger, args.prefix)
        elif args.action == "clean":
            clean_files(args.path, logger)
        elif args.action == "all":
            sort_by_extension(args.path, logger)
            clean_files(args.path, logger)
    except Exception as e:
        logger.error(f"Unexpected error during automation run: {e}")
        sys.exit(1)
    finally:
        logger.info("Automation run finished.\n")


if __name__ == "__main__":
    main()

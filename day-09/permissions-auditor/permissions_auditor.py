#!/usr/bin/env python3
"""
Linux Permissions Auditor - Learning Project

Purpose:
Inspect file and directory permissions inside a designated lab folder.

Limitations:
- This is a learning tool, not a production security scanner.
- A permission mode alone does not prove that a file is vulnerable.
- ACLs and other security controls are not evaluated.
"""

import stat
from pathlib import Path

LAB_DIRECTORY = Path.home() / "cybersecurity-labs" / "day-09"

def describe_permissions(path):
    """Return basic metadata for one filesystem entry."""

    file_stat = path.lstat()
    mode = file_stat.st_mode

    if stat.S_ISLNK(mode):
        file_type = "SYMBOLIC LINK"
    elif stat.S_ISDIR(mode):
        file_type = "DIRECTORY"
    elif stat.S_ISREG(mode):
        file_type = "REGULAR FILE"
    else:
        file_type = "OTHER"

    permissions = stat.filemode(mode)
    numeric_mode = stat.S_IMODE(mode)

    return {
        "name": str(path.relative_to(LAB_DIRECTORY)),
        "type": file_type,
        "symbolic": permissions,
        "numeric": format(numeric_mode, "04o"),
        "owner_uid": file_stat.st_uid,
        "group_gid": file_stat.st_gid,
        "world_writable": bool(numeric_mode & stat.S_IWOTH),
        "ordinary_mode_777": numeric_mode == 0o777,
    }

def audit_directory(root):
    """Inspect entries below the selected lab directory."""

    if not root.exists():
        raise FileNotFoundError(
            f"Lab directory does not exist: {root}"
        )

    if not root.is_dir():
        raise NotADirectoryError(
            f"Expected a directory: {root}"
        )

    print("LINUX PERMISSIONS AUDITOR")
    print("=" * 60)
    print(f"Lab directory: {root}")
    print("Scope: learning directory only")
    print()

    entries = sorted(
        root.rglob("*"),
        key=lambda item: str(item)
    )

    if not entries:
        print("No entries found in the lab directory.")
        return

    for path in entries:
        try:
            result = describe_permissions(path)

            print(f"Name:        {result['name']}")
            print(f"Type:        {result['type']}")
            print(f"Permissions: {result['symbolic']}")
            print(f"Numeric:     {result['numeric']}")
            print(f"Owner UID:   {result['owner_uid']}")
            print(f"Group GID:   {result['group_gid']}")

            if result["ordinary_mode_777"]:
                print(
                    "REVIEW: ordinary permission bits are 777."
                )
                print(
                    "This is a review flag, not proof of a "
                    "vulnerability."
                )

            if result["world_writable"]:
                print(
                    "REVIEW: others have write permission."
                )
                print(
                    "Determine whether this access is "
                    "appropriate for the resource."
                )

            print("-" * 60)

        except OSError as error:
            print(f"Could not inspect {path}: {error}")
            print("-" * 60)

def main():
    try:
        audit_directory(LAB_DIRECTORY)
    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"Configuration error: {error}")
    except PermissionError as error:
        print(f"Access denied while inspecting the lab: {error}")

if __name__ == "__main__":
    main()

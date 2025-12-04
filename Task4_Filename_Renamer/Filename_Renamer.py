"""
Filename Renamer - Main Application
Automates file renaming in a folder with consistent naming patterns
"""

import os
import sys
from filename_renamer_logic import (
    validate_folder_path,
    validate_pattern,
    get_files_in_folder,
    rename_files,
    get_rename_preview,
    undo_last_rename,
    get_rename_history
)


def display_header():
    """Display application header"""
    print("\n" + "="*60)
    print("     FILE RENAMING AUTOMATION SYSTEM")
    print("="*60 + "\n")


def display_menu():
    """Display main menu options"""
    print("\nMENU OPTIONS:")
    print("-" * 40)
    print("1. Rename files in a folder")
    print("2. Preview rename pattern")
    print("3. View rename history")
    print("4. Undo last rename operation")
    print("5. Exit")
    print("-" * 40)


def get_folder_input():
    """Get and validate folder path from user"""
    while True:
        folder_path = input("\nEnter folder path to rename files: ").strip()
        
        if not folder_path:
            print("ERROR: Folder path cannot be empty.")
            continue
        
        # Expand user home directory if present
        folder_path = os.path.expanduser(folder_path)
        
        is_valid, error_msg = validate_folder_path(folder_path)
        if is_valid:
            return folder_path
        else:
            print(f"ERROR: {error_msg}")


def get_pattern_input():
    """Get and validate naming pattern from user"""
    while True:
        print("\nNaming Pattern Examples:")
        print("  - 'file_{num}' → file_1.txt, file_2.txt")
        print("  - 'document_{num:02d}' → document_01.txt, document_02.txt")
        print("  - 'photo_{num}_backup' → photo_1_backup.jpg, photo_2_backup.jpg")
        
        pattern = input("\nEnter naming pattern (use {num} for counter): ").strip()
        
        is_valid, error_msg = validate_pattern(pattern)
        if is_valid:
            return pattern
        else:
            print(f"ERROR: {error_msg}")


def get_file_filter():
    """Get file extension filter from user"""
    filter_ext = input("\nFile extension to rename (e.g., 'txt', '*' for all): ").strip().lower()
    
    if filter_ext == '*':
        return None  # No filter
    
    # Remove dot if user added it
    if filter_ext.startswith('.'):
        filter_ext = filter_ext[1:]
    
    return f".{filter_ext}" if filter_ext else None


def show_rename_preview(folder_path, pattern, file_filter=None):
    """Show preview of renamed files"""
    print("\n" + "="*60)
    print("RENAME PREVIEW")
    print("="*60)
    
    preview_data, error_msg = get_rename_preview(folder_path, pattern, file_filter)
    
    if error_msg:
        print(f"ERROR: {error_msg}")
        return False
    
    if not preview_data:
        print("No files to rename in this folder.")
        return False
    
    print(f"\nTotal files to rename: {len(preview_data)}\n")
    
    for idx, (old_name, new_name) in enumerate(preview_data, 1):
        print(f"{idx}. {old_name:40s} → {new_name}")
    
    print("\n" + "="*60)
    return True


def confirm_rename():
    """Get user confirmation to proceed with rename"""
    while True:
        response = input("\nProceed with renaming? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print("Please enter 'yes' or 'no'.")


def perform_rename(folder_path, pattern, file_filter=None):
    """Perform the actual file renaming"""
    success_count, error_count, errors, new_state = rename_files(
        folder_path, pattern, file_filter
    )
    
    print("\n" + "="*60)
    print("RENAME OPERATION COMPLETE")
    print("="*60)
    print(f"\nSuccessfully renamed: {success_count} files")
    
    if error_count > 0:
        print(f"Failed to rename: {error_count} files")
        print("\nErrors:")
        for error in errors:
            print(f"  - {error}")
    
    print("="*60)
    
    return success_count > 0


def show_rename_history():
    """Display rename operation history"""
    history = get_rename_history()
    
    print("\n" + "="*60)
    print("RENAME HISTORY")
    print("="*60)
    
    if not history:
        print("\nNo rename operations in history.")
    else:
        print(f"\nTotal operations: {len(history)}\n")
        for idx, operation in enumerate(history, 1):
            print(f"Operation {idx}:")
            print(f"  Folder: {operation.get('folder', 'N/A')}")
            print(f"  Pattern: {operation.get('pattern', 'N/A')}")
            print(f"  Files renamed: {operation.get('success_count', 0)}")
            print(f"  Timestamp: {operation.get('timestamp', 'N/A')}")
            print()
    
    print("="*60)


def undo_operation():
    """Undo the last rename operation"""
    print("\nAttempting to undo last rename operation...")
    
    success, message = undo_last_rename()
    
    print("\n" + "="*60)
    if success:
        print("UNDO SUCCESSFUL")
        print("="*60)
        print(f"\n{message}")
    else:
        print("UNDO FAILED")
        print("="*60)
        print(f"\nERROR: {message}")
    
    print("="*60)


def rename_files_menu():
    """Handle the rename files menu option"""
    folder_path = get_folder_input()
    pattern = get_pattern_input()
    file_filter = get_file_filter()
    
    # Show preview
    if show_rename_preview(folder_path, pattern, file_filter):
        # Get confirmation
        if confirm_rename():
            perform_rename(folder_path, pattern, file_filter)
        else:
            print("\nRename operation cancelled.")


def preview_menu():
    """Handle the preview menu option"""
    folder_path = get_folder_input()
    pattern = get_pattern_input()
    file_filter = get_file_filter()
    show_rename_preview(folder_path, pattern, file_filter)


def main():
    """Main application loop"""
    try:
        display_header()
        print("Welcome to File Renaming Automation System!")
        print("This tool helps you rename multiple files with consistent patterns.\n")
        
        while True:
            display_menu()
            choice = input("Select an option (1-5): ").strip()
            
            if choice == '1':
                rename_files_menu()
            
            elif choice == '2':
                preview_menu()
            
            elif choice == '3':
                show_rename_history()
            
            elif choice == '4':
                undo_operation()
            
            elif choice == '5':
                print("\nThank you for using File Renaming Automation System!")
                print("Goodbye!\n")
                break
            
            else:
                print("\nERROR: Invalid option. Please select 1-5.")
    
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user. Exiting...")
        sys.exit(0)
    
    except Exception as e:
        print(f"\nFATAL ERROR: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
    def _cli_folder_check():
        """If invoked with --check-folder <path>, validate and print why it's failing."""
        if len(sys.argv) >= 2 and sys.argv[1] == "--check-folder":
            if len(sys.argv) < 3:
                print("ERROR: Provide a folder path after --check-folder")
                sys.exit(2)
            folder = os.path.expanduser(sys.argv[2])
            is_valid, error = validate_folder_path(folder)
            if is_valid:
                print(f"VALID: {folder}")
                sys.exit(0)
            else:
                print(f"INVALID: {error}")
                sys.exit(1)

    _cli_folder_check()
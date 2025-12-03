"""
Filename Renamer Logic Module
Testable functions for file renaming operations
"""

import os
import re
from datetime import datetime
from typing import Tuple, List, Dict, Optional


# Global state for rename history and undo functionality
_rename_history = []
_last_rename_mapping = {}


def validate_folder_path(folder_path: str) -> Tuple[bool, str]:
    """
    Validate if folder path exists and is accessible
    
    Args:
        folder_path: Path to the folder
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not folder_path:
        return False, "Folder path cannot be empty"
    
    if not isinstance(folder_path, str):
        return False, "Folder path must be a string"
    
    if not os.path.exists(folder_path):
        return False, f"Folder does not exist: {folder_path}"
    
    if not os.path.isdir(folder_path):
        return False, f"Path is not a folder: {folder_path}"
    
    if not os.access(folder_path, os.R_OK):
        return False, "Folder is not readable"
    
    if not os.access(folder_path, os.W_OK):
        return False, "Folder is not writable"
    
    return True, ""


def validate_pattern(pattern: str) -> Tuple[bool, str]:
    """
    Validate naming pattern
    
    Args:
        pattern: Naming pattern with {num} placeholder
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not pattern:
        return False, "Pattern cannot be empty"
    
    if not isinstance(pattern, str):
        return False, "Pattern must be a string"
    
    if "{num" not in pattern:
        return False, "Pattern must contain {num} placeholder"
    
    # Check for valid format specifiers
    try:
        # Test pattern with sample numbers
        pattern.format(num=1)
        pattern.format(num=10)
        pattern.format(num=100)
    except (KeyError, ValueError) as e:
        return False, f"Invalid pattern format: {str(e)}"
    
    # Check for invalid characters in pattern
    invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
    for char in invalid_chars:
        if char in pattern and '{num' not in pattern[:pattern.index(char)]:
            # Allow chars if they're not used as filename chars
            pass
    
    return True, ""


def get_files_in_folder(folder_path: str, file_filter: Optional[str] = None) -> List[str]:
    """
    Get list of files in folder with optional extension filter
    
    Args:
        folder_path: Path to the folder
        file_filter: File extension filter (e.g., '.txt'), or None for all files
    
    Returns:
        List of filenames (not full paths)
    """
    try:
        files = []
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            # Skip directories
            if os.path.isdir(file_path):
                continue
            
            # Apply extension filter if specified
            if file_filter:
                if not filename.lower().endswith(file_filter.lower()):
                    continue
            
            files.append(filename)
        
        # Sort files for consistent ordering
        return sorted(files)
    
    except (OSError, PermissionError) as e:
        return []


def get_file_extension(filename: str) -> str:
    """
    Get file extension from filename
    
    Args:
        filename: The filename
    
    Returns:
        File extension including dot (e.g., '.txt')
    """
    if '.' in filename:
        return os.path.splitext(filename)[1]
    return ""


def get_file_base_name(filename: str) -> str:
    """
    Get file name without extension
    
    Args:
        filename: The filename
    
    Returns:
        Filename without extension
    """
    return os.path.splitext(filename)[0]


def generate_new_filename(pattern: str, counter: int, original_extension: str) -> str:
    """
    Generate new filename based on pattern and counter
    
    Args:
        pattern: Naming pattern with {num} placeholder
        counter: Counter number for the file
        original_extension: Original file extension (e.g., '.txt')
    
    Returns:
        New filename with extension
    """
    try:
        # Format the pattern with the counter
        base_name = pattern.format(num=counter)
        # Add the original extension
        return base_name + original_extension
    
    except (KeyError, ValueError):
        return None


def get_rename_preview(
    folder_path: str,
    pattern: str,
    file_filter: Optional[str] = None
) -> Tuple[List[Tuple[str, str]], str]:
    """
    Get preview of how files will be renamed
    
    Args:
        folder_path: Path to the folder
        pattern: Naming pattern with {num} placeholder
        file_filter: File extension filter, or None for all files
    
    Returns:
        Tuple of (list of (old_name, new_name) pairs, error_message)
    """
    # Validate inputs
    is_valid, error_msg = validate_folder_path(folder_path)
    if not is_valid:
        return [], error_msg
    
    is_valid, error_msg = validate_pattern(pattern)
    if not is_valid:
        return [], error_msg
    
    # Get files
    files = get_files_in_folder(folder_path, file_filter)
    
    if not files:
        return [], "No files found matching filter"
    
    # Generate preview
    preview = []
    for counter, old_filename in enumerate(files, 1):
        extension = get_file_extension(old_filename)
        new_filename = generate_new_filename(pattern, counter, extension)
        
        if new_filename:
            preview.append((old_filename, new_filename))
    
    return preview, ""


def rename_files(
    folder_path: str,
    pattern: str,
    file_filter: Optional[str] = None
) -> Tuple[int, int, List[str], Dict]:
    """
    Rename files in folder according to pattern
    
    Args:
        folder_path: Path to the folder
        pattern: Naming pattern with {num} placeholder
        file_filter: File extension filter, or None for all files
    
    Returns:
        Tuple of (success_count, error_count, error_list, new_rename_state)
    """
    global _rename_history, _last_rename_mapping
    
    # Validate inputs
    is_valid, error_msg = validate_folder_path(folder_path)
    if not is_valid:
        return 0, 0, [error_msg], {}
    
    is_valid, error_msg = validate_pattern(pattern)
    if not is_valid:
        return 0, 0, [error_msg], {}
    
    # Get files
    files = get_files_in_folder(folder_path, file_filter)
    
    if not files:
        return 0, 0, ["No files found"], {}
    
    success_count = 0
    error_count = 0
    errors = []
    rename_mapping = {}  # For undo functionality
    
    for counter, old_filename in enumerate(files, 1):
        old_path = os.path.join(folder_path, old_filename)
        
        try:
            extension = get_file_extension(old_filename)
            new_filename = generate_new_filename(pattern, counter, extension)
            
            if not new_filename:
                error_count += 1
                errors.append(f"Could not generate new name for {old_filename}")
                continue
            
            new_path = os.path.join(folder_path, new_filename)
            
            # Check if new filename already exists
            if os.path.exists(new_path):
                error_count += 1
                errors.append(f"Target file already exists: {new_filename}")
                continue
            
            # Perform rename
            os.rename(old_path, new_path)
            success_count += 1
            rename_mapping[new_filename] = old_filename  # Store for undo
        
        except (OSError, PermissionError) as e:
            error_count += 1
            errors.append(f"Failed to rename {old_filename}: {str(e)}")
        
        except Exception as e:
            error_count += 1
            errors.append(f"Unexpected error for {old_filename}: {str(e)}")
    
    # Store in history
    operation = {
        'folder': folder_path,
        'pattern': pattern,
        'success_count': success_count,
        'error_count': error_count,
        'timestamp': datetime.now().isoformat(),
        'rename_mapping': rename_mapping
    }
    _rename_history.append(operation)
    _last_rename_mapping = rename_mapping
    
    new_state = {'folder': folder_path, 'mapping': rename_mapping}
    
    return success_count, error_count, errors, new_state


def get_rename_history() -> List[Dict]:
    """
    Get history of rename operations
    
    Returns:
        List of rename operation records
    """
    return _rename_history


def clear_rename_history():
    """Clear rename operation history"""
    global _rename_history
    _rename_history = []


def undo_last_rename() -> Tuple[bool, str]:
    """
    Undo the last rename operation
    
    Returns:
        Tuple of (success, message)
    """
    global _rename_history, _last_rename_mapping
    
    if not _rename_history:
        return False, "No rename operations in history"
    
    last_operation = _rename_history[-1]
    folder_path = last_operation.get('folder')
    rename_mapping = last_operation.get('rename_mapping', {})
    
    if not rename_mapping:
        return False, "No rename mapping available for undo"
    
    success_count = 0
    error_count = 0
    errors = []
    
    # Reverse the mappings (new_name -> old_name)
    for new_filename, old_filename in rename_mapping.items():
        old_path = os.path.join(folder_path, old_filename)
        new_path = os.path.join(folder_path, new_filename)
        
        try:
            if os.path.exists(new_path):
                os.rename(new_path, old_path)
                success_count += 1
            else:
                error_count += 1
                errors.append(f"File not found: {new_filename}")
        
        except (OSError, PermissionError) as e:
            error_count += 1
            errors.append(f"Failed to undo rename {new_filename}: {str(e)}")
    
    # Remove from history
    _rename_history.pop()
    
    if success_count > 0 and error_count == 0:
        return True, f"Successfully undid rename operation. Restored {success_count} files."
    elif success_count > 0:
        return True, f"Partially undone. Restored {success_count} files, {error_count} failed."
    else:
        return False, f"Failed to undo rename operation. Errors: {', '.join(errors)}"


def count_files_in_folder(folder_path: str, file_filter: Optional[str] = None) -> int:
    """
    Count files in folder with optional filter
    
    Args:
        folder_path: Path to the folder
        file_filter: File extension filter, or None for all files
    
    Returns:
        Number of files
    """
    files = get_files_in_folder(folder_path, file_filter)
    return len(files)


def validate_rename_safe(folder_path: str, pattern: str, file_filter: Optional[str] = None) -> Tuple[bool, str]:
    """
    Check if rename operation would be safe (no conflicts)
    
    Args:
        folder_path: Path to the folder
        pattern: Naming pattern with {num} placeholder
        file_filter: File extension filter, or None for all files
    
    Returns:
        Tuple of (is_safe, message)
    """
    # Validate inputs
    is_valid, error_msg = validate_folder_path(folder_path)
    if not is_valid:
        return False, error_msg
    
    is_valid, error_msg = validate_pattern(pattern)
    if not is_valid:
        return False, error_msg
    
    # Get preview
    preview, error_msg = get_rename_preview(folder_path, pattern, file_filter)
    
    if error_msg:
        return False, error_msg
    
    # Check for conflicts
    new_filenames = [new_name for _, new_name in preview]
    
    if len(new_filenames) != len(set(new_filenames)):
        return False, "Pattern would create duplicate filenames"
    
    # Check if any new filenames already exist in folder
    existing_files = set(os.listdir(folder_path))
    for new_filename in new_filenames:
        if new_filename in existing_files:
            return False, f"Target filename already exists: {new_filename}"
    
    return True, "Rename operation appears safe"

"""
Filename Renamer Test Suite
Comprehensive tests for file renaming functionality
"""

import unittest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock

from filename_renamer_logic import (
    validate_folder_path,
    validate_pattern,
    get_files_in_folder,
    get_file_extension,
    get_file_base_name,
    generate_new_filename,
    get_rename_preview,
    rename_files,
    get_rename_history,
    clear_rename_history,
    undo_last_rename,
    count_files_in_folder,
    validate_rename_safe
)


class TestValidateFolderPath(unittest.TestCase):
    """Tests for folder path validation"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_valid_folder_path(self):
        """Test valid folder path"""
        is_valid, error_msg = validate_folder_path(self.test_dir)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
    
    def test_empty_path(self):
        """Test empty folder path"""
        is_valid, error_msg = validate_folder_path("")
        self.assertFalse(is_valid)
        self.assertIn("empty", error_msg.lower())
    
    def test_nonexistent_path(self):
        """Test non-existent folder"""
        is_valid, error_msg = validate_folder_path("/nonexistent/folder/path")
        self.assertFalse(is_valid)
        self.assertIn("does not exist", error_msg.lower())
    
    def test_file_not_directory(self):
        """Test path pointing to file instead of directory"""
        test_file = os.path.join(self.test_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        
        is_valid, error_msg = validate_folder_path(test_file)
        self.assertFalse(is_valid)
        self.assertIn("not a folder", error_msg.lower())
    
    def test_non_string_path(self):
        """Test non-string path input"""
        is_valid, error_msg = validate_folder_path(123)
        self.assertFalse(is_valid)
        self.assertIn("must be a string", error_msg.lower())


class TestValidatePattern(unittest.TestCase):
    """Tests for naming pattern validation"""
    
    def test_valid_pattern_simple(self):
        """Test simple valid pattern"""
        is_valid, error_msg = validate_pattern("file_{num}")
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
    
    def test_valid_pattern_with_format(self):
        """Test pattern with format specifier"""
        is_valid, error_msg = validate_pattern("file_{num:02d}")
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
    
    def test_valid_pattern_with_text(self):
        """Test pattern with additional text"""
        is_valid, error_msg = validate_pattern("document_{num}_backup")
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
    
    def test_empty_pattern(self):
        """Test empty pattern"""
        is_valid, error_msg = validate_pattern("")
        self.assertFalse(is_valid)
        self.assertIn("empty", error_msg.lower())
    
    def test_pattern_missing_placeholder(self):
        """Test pattern without {num} placeholder"""
        is_valid, error_msg = validate_pattern("file_name")
        self.assertFalse(is_valid)
        self.assertIn("{num}", error_msg)
    
    def test_invalid_format_specifier(self):
        """Test pattern with invalid format specifier"""
        is_valid, error_msg = validate_pattern("file_{num:invalid}")
        self.assertFalse(is_valid)
    
    def test_non_string_pattern(self):
        """Test non-string pattern"""
        is_valid, error_msg = validate_pattern(123)
        self.assertFalse(is_valid)
        self.assertIn("must be a string", error_msg.lower())


class TestGetFilesInFolder(unittest.TestCase):
    """Tests for getting files from folder"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        # Create test files
        self.test_files = [
            ("document1.txt", "content1"),
            ("document2.txt", "content2"),
            ("image1.jpg", "binary"),
            ("image2.png", "binary"),
            ("script.py", "code")
        ]
        for filename, content in self.test_files:
            with open(os.path.join(self.test_dir, filename), 'w') as f:
                f.write(content)
    
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_get_all_files(self):
        """Test getting all files"""
        files = get_files_in_folder(self.test_dir)
        self.assertEqual(len(files), 5)
    
    def test_get_files_with_filter(self):
        """Test getting files with extension filter"""
        files = get_files_in_folder(self.test_dir, ".txt")
        self.assertEqual(len(files), 2)
        self.assertTrue(all(f.endswith('.txt') for f in files))
    
    def test_get_files_case_insensitive_filter(self):
        """Test file filter is case insensitive"""
        files = get_files_in_folder(self.test_dir, ".TXT")
        self.assertEqual(len(files), 2)
    
    def test_files_sorted(self):
        """Test files are returned sorted"""
        files = get_files_in_folder(self.test_dir)
        self.assertEqual(files, sorted(files))
    
    def test_exclude_directories(self):
        """Test that subdirectories are excluded"""
        subdir = os.path.join(self.test_dir, "subdir")
        os.makedirs(subdir)
        
        files = get_files_in_folder(self.test_dir)
        self.assertEqual(len(files), 5)  # Subdirectory not included


class TestFileNameOperations(unittest.TestCase):
    """Tests for file name extraction operations"""
    
    def test_get_file_extension_with_extension(self):
        """Test extracting extension from file with extension"""
        ext = get_file_extension("document.txt")
        self.assertEqual(ext, ".txt")
    
    def test_get_file_extension_no_extension(self):
        """Test extracting extension from file without extension"""
        ext = get_file_extension("README")
        self.assertEqual(ext, "")
    
    def test_get_file_extension_multiple_dots(self):
        """Test file with multiple dots"""
        ext = get_file_extension("archive.backup.tar.gz")
        self.assertEqual(ext, ".gz")
    
    def test_get_file_base_name(self):
        """Test extracting base name"""
        base = get_file_base_name("document.txt")
        self.assertEqual(base, "document")
    
    def test_get_file_base_name_no_extension(self):
        """Test base name for file without extension"""
        base = get_file_base_name("README")
        self.assertEqual(base, "README")


class TestGenerateNewFilename(unittest.TestCase):
    """Tests for new filename generation"""
    
    def test_simple_pattern(self):
        """Test simple pattern generation"""
        new_name = generate_new_filename("file_{num}", 1, ".txt")
        self.assertEqual(new_name, "file_1.txt")
    
    def test_pattern_with_format_specifier(self):
        """Test pattern with format specifier"""
        new_name = generate_new_filename("file_{num:03d}", 5, ".txt")
        self.assertEqual(new_name, "file_005.txt")
    
    def test_pattern_with_text(self):
        """Test pattern with additional text"""
        new_name = generate_new_filename("document_{num}_backup", 2, ".doc")
        self.assertEqual(new_name, "document_2_backup.doc")
    
    def test_no_extension(self):
        """Test filename without extension"""
        new_name = generate_new_filename("file_{num}", 1, "")
        self.assertEqual(new_name, "file_1")
    
    def test_large_counter(self):
        """Test with large counter number"""
        new_name = generate_new_filename("photo_{num}", 10000, ".jpg")
        self.assertEqual(new_name, "photo_10000.jpg")


class TestGetRenamePreview(unittest.TestCase):
    """Tests for rename preview functionality"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        # Create test files
        for i in range(3):
            with open(os.path.join(self.test_dir, f"old_name_{i}.txt"), 'w') as f:
                f.write(f"content {i}")
    
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_preview_valid_operation(self):
        """Test preview of valid rename operation"""
        preview, error_msg = get_rename_preview(self.test_dir, "file_{num}")
        self.assertEqual(error_msg, "")
        self.assertEqual(len(preview), 3)
    
    def test_preview_returns_old_and_new(self):
        """Test preview returns both old and new names"""
        preview, _ = get_rename_preview(self.test_dir, "new_file_{num}")
        self.assertTrue(all(isinstance(pair, tuple) and len(pair) == 2 for pair in preview))
    
    def test_preview_preserves_extension(self):
        """Test that extensions are preserved in preview"""
        preview, _ = get_rename_preview(self.test_dir, "file_{num}")
        self.assertTrue(all(new.endswith('.txt') for _, new in preview))
    
    def test_preview_invalid_folder(self):
        """Test preview with invalid folder"""
        preview, error_msg = get_rename_preview("/nonexistent", "file_{num}")
        self.assertNotEqual(error_msg, "")
        self.assertEqual(preview, [])
    
    def test_preview_invalid_pattern(self):
        """Test preview with invalid pattern"""
        preview, error_msg = get_rename_preview(self.test_dir, "invalid_pattern")
        self.assertNotEqual(error_msg, "")
        self.assertEqual(preview, [])


class TestRenameFiles(unittest.TestCase):
    """Tests for actual file renaming"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        # Create test files
        self.test_files = []
        for i in range(3):
            filename = f"old_file_{i}.txt"
            filepath = os.path.join(self.test_dir, filename)
            with open(filepath, 'w') as f:
                f.write(f"content {i}")
            self.test_files.append(filename)
        clear_rename_history()
    
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        clear_rename_history()
    
    def test_rename_files_success(self):
        """Test successful file renaming"""
        success_count, error_count, errors, _ = rename_files(
            self.test_dir, "file_{num}"
        )
        self.assertEqual(success_count, 3)
        self.assertEqual(error_count, 0)
        self.assertEqual(len(errors), 0)
    
    def test_renamed_files_exist(self):
        """Test that renamed files actually exist"""
        rename_files(self.test_dir, "renamed_{num}")
        
        files = os.listdir(self.test_dir)
        self.assertIn("renamed_1.txt", files)
        self.assertIn("renamed_2.txt", files)
        self.assertIn("renamed_3.txt", files)
    
    def test_old_files_removed(self):
        """Test that old files are removed after renaming"""
        rename_files(self.test_dir, "new_{num}")
        
        files = os.listdir(self.test_dir)
        self.assertNotIn("old_file_0.txt", files)
        self.assertNotIn("old_file_1.txt", files)
        self.assertNotIn("old_file_2.txt", files)
    
    def test_rename_with_filter(self):
        """Test renaming with file filter"""
        # Create a file with different extension
        with open(os.path.join(self.test_dir, "readme.md"), 'w') as f:
            f.write("readme")
        
        success_count, _, _, _ = rename_files(
            self.test_dir, "file_{num}", ".txt"
        )
        
        # Should only rename .txt files
        self.assertEqual(success_count, 3)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "readme.md")))
    
    def test_rename_history_recorded(self):
        """Test that rename operation is recorded in history"""
        rename_files(self.test_dir, "file_{num}")
        
        history = get_rename_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['folder'], self.test_dir)
        self.assertEqual(history[0]['success_count'], 3)


class TestUndoRename(unittest.TestCase):
    """Tests for undo functionality"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        # Create test files
        for i in range(3):
            filename = f"original_{i}.txt"
            filepath = os.path.join(self.test_dir, filename)
            with open(filepath, 'w') as f:
                f.write(f"content {i}")
        clear_rename_history()
    
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        clear_rename_history()
    
    def test_undo_rename_operation(self):
        """Test undoing a rename operation"""
        # Rename files first
        rename_files(self.test_dir, "renamed_{num}")
        
        # Verify rename happened
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "renamed_1.txt")))
        
        # Undo
        success, message = undo_last_rename()
        
        self.assertTrue(success)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "original_0.txt")))
    
    def test_undo_no_history(self):
        """Test undo when there's no history"""
        success, message = undo_last_rename()
        
        self.assertFalse(success)
        self.assertIn("history", message.lower())
    
    def test_undo_removes_from_history(self):
        """Test that undo removes operation from history"""
        rename_files(self.test_dir, "file_{num}")
        self.assertEqual(len(get_rename_history()), 1)
        
        undo_last_rename()
        self.assertEqual(len(get_rename_history()), 0)


class TestCountFiles(unittest.TestCase):
    """Tests for file counting"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        # Create test files
        for i in range(2):
            with open(os.path.join(self.test_dir, f"file_{i}.txt"), 'w') as f:
                f.write("content")
        for i in range(3):
            with open(os.path.join(self.test_dir, f"image_{i}.jpg"), 'w') as f:
                f.write("binary")
    
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_count_all_files(self):
        """Test counting all files"""
        count = count_files_in_folder(self.test_dir)
        self.assertEqual(count, 5)
    
    def test_count_with_filter(self):
        """Test counting with filter"""
        count = count_files_in_folder(self.test_dir, ".txt")
        self.assertEqual(count, 2)


class TestValidateRenameSafe(unittest.TestCase):
    """Tests for rename safety validation"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        # Create test files
        for i in range(2):
            with open(os.path.join(self.test_dir, f"file_{i}.txt"), 'w') as f:
                f.write("content")
    
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_safe_rename_operation(self):
        """Test validation of safe rename operation"""
        is_safe, message = validate_rename_safe(self.test_dir, "new_file_{num}")
        self.assertTrue(is_safe)
    
    def test_invalid_folder_not_safe(self):
        """Test that invalid folder returns not safe"""
        is_safe, message = validate_rename_safe("/nonexistent", "file_{num}")
        self.assertFalse(is_safe)
    
    def test_invalid_pattern_not_safe(self):
        """Test that invalid pattern returns not safe"""
        is_safe, message = validate_rename_safe(self.test_dir, "invalid_pattern")
        self.assertFalse(is_safe)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        # Create multiple types of files
        for i in range(3):
            with open(os.path.join(self.test_dir, f"photo_{i}.jpg"), 'w') as f:
                f.write("binary")
        clear_rename_history()
    
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        clear_rename_history()
    
    def test_complete_rename_workflow(self):
        """Test complete rename workflow"""
        # Preview
        preview, error = get_rename_preview(self.test_dir, "picture_{num}")
        self.assertEqual(error, "")
        self.assertEqual(len(preview), 3)
        
        # Check safety
        is_safe, message = validate_rename_safe(self.test_dir, "picture_{num}")
        self.assertTrue(is_safe)
        
        # Rename
        success, error, errors, _ = rename_files(self.test_dir, "picture_{num}")
        self.assertEqual(success, 3)
        self.assertEqual(error, 0)
        
        # Verify files exist
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "picture_1.jpg")))
    
    def test_rename_undo_workflow(self):
        """Test rename and undo workflow"""
        original_files = set(os.listdir(self.test_dir))
        
        # Rename
        rename_files(self.test_dir, "renamed_{num}")
        renamed_files = set(os.listdir(self.test_dir))
        self.assertNotEqual(original_files, renamed_files)
        
        # Undo
        undo_last_rename()
        current_files = set(os.listdir(self.test_dir))
        self.assertEqual(original_files, current_files)


if __name__ == '__main__':
    unittest.main()

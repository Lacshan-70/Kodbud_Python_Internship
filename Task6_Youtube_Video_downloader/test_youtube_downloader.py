"""
================================================================================
                    YOUTUBE VIDEO DOWNLOADER - TEST CASES
================================================================================

TEST SUITE DESCRIPTION:
    This test module validates all functionalities of the YouTube Video
    Downloader application including URL validation, folder validation,
    and video information retrieval with error handling.

TEST COVERAGE:
    1. YouTube URL validation
    2. Folder path validation
    3. Invalid link error handling
    4. Video information retrieval
    5. Stream selection
    6. File size calculation
    7. Safe filename generation
    8. General input validation

DEVELOPED BY: Lacshan Shakthivel
DATE: December 3, 2025

================================================================================
"""

import unittest
import sys
import os
import tempfile
from unittest.mock import patch, MagicMock

# Get the directory of the current script and add it to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from youtube_downloader_logic import (
    validate_url, validate_folder, get_video_info, get_best_stream,
    get_file_size_mb, get_safe_filename, validate_input
)


class TestValidateUrl(unittest.TestCase):
    """
    Test cases for the validate_url() function.
    """
    
    def test_valid_youtube_com_url(self):
        """Test valid youtube.com URL"""
        is_valid, error = validate_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_valid_youtu_be_url(self):
        """Test valid youtu.be short URL"""
        is_valid, error = validate_url("https://youtu.be/dQw4w9WgXcQ")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_valid_url_http(self):
        """Test valid URL with http"""
        is_valid, error = validate_url("http://www.youtube.com/watch?v=dQw4w9WgXcQ")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_valid_url_with_playlist(self):
        """Test valid YouTube playlist URL"""
        is_valid, error = validate_url("https://www.youtube.com/playlist?list=PLxxxxx")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_invalid_url_empty(self):
        """Test invalid empty URL"""
        is_valid, error = validate_url("")
        self.assertFalse(is_valid)
        self.assertIn("empty", error.lower())
    
    def test_invalid_url_whitespace(self):
        """Test invalid whitespace-only URL"""
        is_valid, error = validate_url("   ")
        self.assertFalse(is_valid)
        self.assertIn("empty", error.lower())
    
    def test_invalid_url_no_https(self):
        """Test invalid URL without http/https"""
        is_valid, error = validate_url("www.youtube.com/watch?v=dQw4w9WgXcQ")
        self.assertFalse(is_valid)
        self.assertIn("http", error.lower())
    
    def test_invalid_url_not_youtube(self):
        """Test invalid non-YouTube URL"""
        is_valid, error = validate_url("https://www.google.com")
        self.assertFalse(is_valid)
        self.assertIn("youtube", error.lower())
    
    def test_invalid_url_ftp_protocol(self):
        """Test invalid FTP protocol"""
        is_valid, error = validate_url("ftp://youtube.com/video")
        self.assertFalse(is_valid)
        self.assertIn("http", error.lower())
    
    def test_valid_url_with_trailing_spaces(self):
        """Test URL with trailing spaces (should be trimmed)"""
        is_valid, error = validate_url("  https://www.youtube.com/watch?v=dQw4w9WgXcQ  ")
        self.assertTrue(is_valid)
        self.assertIsNone(error)


class TestValidateFolder(unittest.TestCase):
    """
    Test cases for the validate_folder() function.
    """
    
    def test_valid_temp_folder(self):
        """Test validation of valid temporary folder"""
        with tempfile.TemporaryDirectory() as temp_dir:
            is_valid, error = validate_folder(temp_dir)
            self.assertTrue(is_valid)
            self.assertIsNone(error)
    
    def test_valid_current_directory(self):
        """Test validation of current directory"""
        current_dir = os.getcwd()
        is_valid, error = validate_folder(current_dir)
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_invalid_folder_empty_path(self):
        """Test invalid empty folder path"""
        is_valid, error = validate_folder("")
        self.assertFalse(is_valid)
        self.assertIn("empty", error.lower())
    
    def test_invalid_folder_whitespace(self):
        """Test invalid whitespace-only folder path"""
        is_valid, error = validate_folder("   ")
        self.assertFalse(is_valid)
        self.assertIn("empty", error.lower())
    
    def test_invalid_folder_nonexistent(self):
        """Test invalid non-existent folder"""
        is_valid, error = validate_folder("/nonexistent/folder/path/12345")
        self.assertFalse(is_valid)
        self.assertIn("does not exist", error)
    
    def test_invalid_folder_is_file(self):
        """Test invalid path that is a file, not directory"""
        with tempfile.NamedTemporaryFile() as temp_file:
            is_valid, error = validate_folder(temp_file.name)
            self.assertFalse(is_valid)
            self.assertIn("not a directory", error)
    
    def test_valid_folder_with_leading_trailing_spaces(self):
        """Test folder path with leading/trailing spaces"""
        with tempfile.TemporaryDirectory() as temp_dir:
            is_valid, error = validate_folder(f"  {temp_dir}  ")
            self.assertTrue(is_valid)
            self.assertIsNone(error)


class TestGetVideoInfo(unittest.TestCase):
    """
    Test cases for the get_video_info() function.
    """
    
    @patch('youtube_downloader_logic.YouTube')
    def test_valid_video_retrieval(self, mock_youtube):
        """Test successful video information retrieval"""
        mock_yt = MagicMock()
        mock_youtube.return_value = mock_yt
        
        yt, error = get_video_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        
        self.assertIsNotNone(yt)
        self.assertIsNone(error)
        mock_youtube.assert_called_once()
    
    @patch('youtube_downloader_logic.YouTube')
    def test_invalid_url_format(self, mock_youtube):
        """Test RegexMatchError handling"""
        from pytube.exceptions import RegexMatchError
        mock_youtube.side_effect = RegexMatchError("pattern", "string")
        
        yt, error = get_video_info("invalid_url")
        
        self.assertIsNone(yt)
        self.assertIn("Invalid YouTube URL format", error)
    
    @patch('youtube_downloader_logic.YouTube')
    def test_video_unavailable(self, mock_youtube):
        """Test VideoUnavailable handling"""
        from pytube.exceptions import VideoUnavailable
        mock_youtube.side_effect = VideoUnavailable("Video not available")
        
        yt, error = get_video_info("https://www.youtube.com/watch?v=deleted")
        
        self.assertIsNone(yt)
        self.assertIn("unavailable", error.lower())
    
    @patch('youtube_downloader_logic.YouTube')
    def test_generic_exception(self, mock_youtube):
        """Test generic exception handling"""
        mock_youtube.side_effect = Exception("Network error")
        
        yt, error = get_video_info("https://www.youtube.com/watch?v=test")
        
        self.assertIsNone(yt)
        self.assertIn("Error accessing video", error)


class TestGetBestStream(unittest.TestCase):
    """
    Test cases for the get_best_stream() function.
    """
    
    def test_get_best_stream_progressive(self):
        """Test stream selection with progressive available"""
        mock_yt = MagicMock()
        mock_stream = MagicMock()
        mock_stream.resolution = "720p"
        
        mock_yt.streams.filter().order_by().desc().first.return_value = mock_stream
        
        stream, error = get_best_stream(mock_yt)
        
        self.assertEqual(stream, mock_stream)
        self.assertIsNone(error)
    
    def test_get_best_stream_fallback(self):
        """Test stream selection fallback to highest resolution"""
        mock_yt = MagicMock()
        mock_stream = MagicMock()
        
        mock_yt.streams.filter().order_by().desc().first.return_value = None
        mock_yt.streams.get_highest_resolution.return_value = mock_stream
        
        stream, error = get_best_stream(mock_yt)
        
        self.assertEqual(stream, mock_stream)
        self.assertIsNone(error)
    
    def test_get_best_stream_no_streams(self):
        """Test when no streams are available"""
        mock_yt = MagicMock()
        
        mock_yt.streams.filter().order_by().desc().first.return_value = None
        mock_yt.streams.get_highest_resolution.return_value = None
        
        stream, error = get_best_stream(mock_yt)
        
        self.assertIsNone(stream)
        self.assertIn("no downloadable streams", error.lower())
    
    def test_get_best_stream_exception(self):
        """Test exception handling in stream selection"""
        mock_yt = MagicMock()
        mock_yt.streams.filter.side_effect = Exception("API error")
        
        stream, error = get_best_stream(mock_yt)
        
        self.assertIsNone(stream)
        self.assertIn("Error selecting stream", error)


class TestGetFileSizeMb(unittest.TestCase):
    """
    Test cases for the get_file_size_mb() function.
    """
    
    def test_file_size_mb_conversion(self):
        """Test file size conversion to MB"""
        mock_stream = MagicMock()
        mock_stream.filesize = 1024 * 1024 * 100  # 100 MB
        
        size_mb = get_file_size_mb(mock_stream)
        
        self.assertEqual(size_mb, 100.0)
    
    def test_file_size_mb_small_file(self):
        """Test small file size conversion"""
        mock_stream = MagicMock()
        mock_stream.filesize = 1024 * 512  # 0.5 MB
        
        size_mb = get_file_size_mb(mock_stream)
        
        self.assertAlmostEqual(size_mb, 0.5, places=2)
    
    def test_file_size_mb_zero(self):
        """Test zero file size"""
        mock_stream = MagicMock()
        mock_stream.filesize = 0
        
        size_mb = get_file_size_mb(mock_stream)
        
        self.assertEqual(size_mb, 0.0)
    
    def test_file_size_mb_none(self):
        """Test None stream"""
        size_mb = get_file_size_mb(None)
        
        self.assertEqual(size_mb, 0.0)


class TestGetSafeFilename(unittest.TestCase):
    """
    Test cases for the get_safe_filename() function.
    """
    
    def test_safe_filename_valid(self):
        """Test valid filename"""
        safe_name = get_safe_filename("My Video Title")
        self.assertEqual(safe_name, "My Video Title")
    
    def test_safe_filename_invalid_chars(self):
        """Test removal of invalid characters"""
        safe_name = get_safe_filename('Video <Title> "with" invalid | chars?')
        self.assertNotIn('<', safe_name)
        self.assertNotIn('>', safe_name)
        self.assertNotIn('"', safe_name)
        self.assertNotIn('|', safe_name)
        self.assertNotIn('?', safe_name)
    
    def test_safe_filename_all_invalid(self):
        """Test filename with all invalid characters"""
        safe_name = get_safe_filename('<<<>>>???:::|||||')
        self.assertNotIn('<', safe_name)
        self.assertNotIn('>', safe_name)
        self.assertNotIn('?', safe_name)
        self.assertTrue(len(safe_name) > 0)
    
    def test_safe_filename_truncate_long(self):
        """Test truncation of long filename"""
        long_title = "a" * 250
        safe_name = get_safe_filename(long_title, max_length=200)
        self.assertEqual(len(safe_name), 200)
    
    def test_safe_filename_empty(self):
        """Test empty title fallback"""
        safe_name = get_safe_filename("")
        self.assertEqual(safe_name, "video")
    
    def test_safe_filename_none(self):
        """Test None title fallback"""
        safe_name = get_safe_filename(None)
        self.assertEqual(safe_name, "video")
    
    def test_safe_filename_whitespace_trimmed(self):
        """Test whitespace trimming"""
        safe_name = get_safe_filename("   Title with spaces   ")
        self.assertEqual(safe_name, "Title with spaces")


class TestValidateInput(unittest.TestCase):
    """
    Test cases for the validate_input() function.
    """
    
    def test_validate_input_general_valid(self):
        """Test general input validation - valid"""
        result = validate_input("valid input")
        self.assertTrue(result)
    
    def test_validate_input_general_empty(self):
        """Test general input validation - empty"""
        result = validate_input("")
        self.assertFalse(result)
    
    def test_validate_input_url_valid(self):
        """Test URL input validation - valid"""
        result = validate_input("https://www.youtube.com/watch?v=test", input_type="url")
        self.assertTrue(result)
    
    def test_validate_input_url_invalid(self):
        """Test URL input validation - invalid"""
        result = validate_input("not a youtube url", input_type="url")
        self.assertFalse(result)
    
    def test_validate_input_folder_valid(self):
        """Test folder input validation - valid"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = validate_input(temp_dir, input_type="folder")
            self.assertTrue(result)
    
    def test_validate_input_folder_invalid(self):
        """Test folder input validation - invalid"""
        result = validate_input("/nonexistent/path", input_type="folder")
        self.assertFalse(result)
    
    def test_validate_input_choice_yes(self):
        """Test choice input validation - yes"""
        result = validate_input("yes", input_type="choice")
        self.assertTrue(result)
    
    def test_validate_input_choice_y(self):
        """Test choice input validation - y"""
        result = validate_input("y", input_type="choice")
        self.assertTrue(result)
    
    def test_validate_input_choice_no(self):
        """Test choice input validation - no"""
        result = validate_input("no", input_type="choice")
        self.assertTrue(result)
    
    def test_validate_input_choice_n(self):
        """Test choice input validation - n"""
        result = validate_input("n", input_type="choice")
        self.assertTrue(result)
    
    def test_validate_input_choice_invalid(self):
        """Test choice input validation - invalid"""
        result = validate_input("maybe", input_type="choice")
        self.assertFalse(result)
    
    def test_validate_input_choice_case_insensitive(self):
        """Test choice input validation - case insensitive"""
        result = validate_input("YES", input_type="choice")
        self.assertTrue(result)


class TestIntegration(unittest.TestCase):
    """
    Integration tests for URL and folder validation workflow.
    """
    
    def test_workflow_valid_url_and_folder(self):
        """Test complete workflow with valid inputs"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        is_valid_url, _ = validate_url(url)
        self.assertTrue(is_valid_url)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            is_valid_folder, _ = validate_folder(temp_dir)
            self.assertTrue(is_valid_folder)
    
    def test_workflow_invalid_url(self):
        """Test workflow with invalid URL"""
        url = "not a url"
        is_valid_url, error = validate_url(url)
        self.assertFalse(is_valid_url)
        self.assertIsNotNone(error)
    
    def test_workflow_invalid_folder(self):
        """Test workflow with invalid folder"""
        with tempfile.TemporaryDirectory() as temp_dir:
            valid_folder_path = temp_dir
        
        # Now the temp folder is deleted
        is_valid_folder, error = validate_folder(valid_folder_path)
        self.assertFalse(is_valid_folder)
        self.assertIsNotNone(error)


def run_test_summary():
    """
    Run all tests and display a summary report.
    """
    print("\n" + "="*80)
    print("RUNNING YOUTUBE VIDEO DOWNLOADER TEST SUITE")
    print("="*80 + "\n")
    
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestValidateUrl))
    suite.addTests(loader.loadTestsFromTestCase(TestValidateFolder))
    suite.addTests(loader.loadTestsFromTestCase(TestGetVideoInfo))
    suite.addTests(loader.loadTestsFromTestCase(TestGetBestStream))
    suite.addTests(loader.loadTestsFromTestCase(TestGetFileSizeMb))
    suite.addTests(loader.loadTestsFromTestCase(TestGetSafeFilename))
    suite.addTests(loader.loadTestsFromTestCase(TestValidateInput))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*80 + "\n")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_test_summary()
    sys.exit(0 if success else 1)

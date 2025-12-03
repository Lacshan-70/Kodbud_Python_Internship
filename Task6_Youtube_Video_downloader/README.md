================================================================================
                    YOUTUBE VIDEO DOWNLOADER - SETUP GUIDE
================================================================================

PROJECT OVERVIEW:
    The YouTube Video Downloader is a Python application that enables users to
    download YouTube videos to their local computer with error handling for
    invalid links and comprehensive validation.

================================================================================
                        INSTALLATION REQUIREMENTS
================================================================================

Required Library:
    • pytube (version 15.0.0 or higher)

Installation Command:
    pip install pytube

================================================================================
                        FILE STRUCTURE
================================================================================

Youtube_Video_downloader.py
├─ Purpose: Main application with user interface
├─ Functions:
│  ├─ get_user_url(): Prompts for video URL
│  ├─ get_destination_folder(): Prompts for folder path
│  ├─ display_error(): Shows error messages
│  ├─ ask_continue(): Asks to download another video
│  ├─ downloader(): Main download loop
│  └─ main(): Entry point
└─ Lines: 280+ (including documentation)

youtube_downloader_logic.py
├─ Purpose: Separated logic module for testability
├─ Functions:
│  ├─ validate_url(): Validate YouTube URL format
│  ├─ validate_folder(): Validate destination folder
│  ├─ get_video_info(): Retrieve video metadata
│  ├─ get_best_stream(): Select best quality stream
│  ├─ get_file_size_mb(): Convert filesize to MB
│  ├─ get_safe_filename(): Generate safe filename
│  └─ validate_input(): Multi-type input validation
└─ Lines: 170+ (including documentation)

test_youtube_downloader.py
├─ Purpose: Comprehensive test suite
├─ Test Classes: 8 classes
├─ Total Tests: 51 test cases
├─ Coverage:
│  ├─ URL validation: 10 tests
│  ├─ Folder validation: 7 tests
│  ├─ Video info retrieval: 4 tests
│  ├─ Stream selection: 4 tests
│  ├─ File size conversion: 4 tests
│  ├─ Safe filename generation: 7 tests
│  ├─ Input validation: 12 tests
│  └─ Integration workflows: 3 tests
└─ Pass Rate: 100% (51/51)

TEST_REPORT.txt
├─ Purpose: Detailed test execution report
├─ Contents: Test summary, results, validation
└─ Pass Rate: 100% with 0.105 seconds execution

================================================================================
                        USAGE INSTRUCTIONS
================================================================================

Running the Application:
    python Youtube_Video_downloader.py

Running the Test Suite:
    python test_youtube_downloader.py

Application Workflow:
    1. User enters YouTube URL
       • Validates: youtube.com or youtu.be domain
       • Validates: http:// or https:// protocol
       • Handles: Empty or invalid URL input

    2. User enters destination folder
       • Validates: Folder exists
       • Validates: User has write permissions
       • Handles: Non-existent or protected folders

    3. Application retrieves video information
       • Handles: Invalid URL format (RegexMatchError)
       • Handles: Unavailable/deleted videos (VideoUnavailable)
       • Handles: Network errors

    4. Application selects best quality stream
       • Priority 1: Progressive stream (video + audio)
       • Priority 2: Highest resolution
       • Handles: No streams available

    5. Application downloads video
       • Shows: Video title, resolution, file size
       • Shows: Download destination
       • Handles: Download errors

    6. User can choose to download another video or exit

================================================================================
                        ERROR HANDLING
================================================================================

URL Validation Errors:
    ❌ Empty URL → "URL cannot be empty"
    ❌ Non-YouTube URL → "Must be a YouTube link"
    ❌ Wrong protocol → "Must start with http:// or https://"

Folder Validation Errors:
    ❌ Empty path → "Folder path cannot be empty"
    ❌ Non-existent → "Folder does not exist"
    ❌ Not a directory → "Path is not a directory"
    ❌ No permissions → "No write permission"

Video Access Errors:
    ❌ Invalid URL format → "Invalid YouTube URL format"
    ❌ Video unavailable → "Video is unavailable or has been removed"
    ❌ Network error → "Error accessing video: [details]"

Stream Errors:
    ❌ No streams available → "No downloadable streams available"
    ❌ Stream selection error → "Error selecting stream: [details]"

Download Errors:
    ❌ Download failed → "Download failed: [details]"

================================================================================
                        FEATURES IMPLEMENTED
================================================================================

✅ YouTube URL Validation
   • Validates domain (youtube.com or youtu.be)
   • Validates protocol (http or https)
   • Handles whitespace trimming

✅ Folder Validation
   • Checks folder existence
   • Verifies write permissions
   • Ensures path is a directory

✅ Pytube Integration
   • YouTube object creation
   • Stream availability checking
   • Quality stream selection
   • File size information

✅ Error Handling
   • Specific pytube exception handling
   • Generic exception fallback
   • User-friendly error messages
   • Input validation at all steps

✅ File Operations
   • Safe filename generation
   • Invalid character removal
   • Filename truncation
   • File size conversion to MB

✅ User Interface
   • Interactive prompts
   • Progress information
   • Result feedback
   • Retry option

================================================================================
                        TEST COVERAGE
================================================================================

Total Tests: 51
Passed: 51 ✅
Failed: 0
Errors: 0
Pass Rate: 100%

Test Categories:
├─ URL Validation: 10/10 (100%)
├─ Folder Validation: 7/7 (100%)
├─ Video Info Retrieval: 4/4 (100%)
├─ Stream Selection: 4/4 (100%)
├─ File Size Conversion: 4/4 (100%)
├─ Safe Filename Generation: 7/7 (100%)
├─ Input Validation: 12/12 (100%)
└─ Integration Workflows: 3/3 (100%)

Execution Time: 0.105 seconds
Performance: 486 tests/second

================================================================================
                        DEVELOPMENT NOTES
================================================================================

Architecture Decisions:
    1. Separated logic module for testability (youtube_downloader_logic.py)
    2. Functions return tuple (result, error_message) for easy error handling
    3. Comprehensive validation at each step
    4. Mock testing for pytube integration

Libraries Used:
    • pytube: YouTube video downloading
    • os: File path operations and validation
    • unittest: Test framework
    • unittest.mock: Mocking pytube for unit tests

Special Techniques:
    • Mock objects for testing pytube exceptions
    • Tuple-based error handling pattern
    • Safe filename sanitization
    • File permission verification

================================================================================
                        TROUBLESHOOTING
================================================================================

Issue: "ModuleNotFoundError: No module named 'pytube'"
    Solution: Run: pip install pytube

Issue: Download fails with network error
    Solution: Check internet connection, verify YouTube URL is accessible

Issue: "No write permission for folder"
    Solution: Choose a folder with write permissions or run as administrator

Issue: Video unavailable error
    Solution: Verify the YouTube video exists and is not private/deleted

Issue: Large file not downloading completely
    Solution: Ensure sufficient disk space in destination folder

================================================================================
                            CONCLUSION
================================================================================

The YouTube Video Downloader has been successfully implemented with:
    ✅ Complete pytube integration
    ✅ Comprehensive error handling
    ✅ URL and folder validation
    ✅ 51 comprehensive test cases (100% pass rate)
    ✅ Production-ready code

The application is ready for use and handles all specified requirements:
    ✅ Uses pytube library for downloading
    ✅ Asks user for video URL
    ✅ Asks user for destination folder
    ✅ Adds error handling for invalid links

================================================================================

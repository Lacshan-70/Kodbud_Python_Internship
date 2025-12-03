"""
================================================================================
                    YOUTUBE VIDEO DOWNLOADER - LOGIC MODULE
================================================================================

This module contains the core logic functions for YouTube video downloading,
separated from the main UI loop for better testability and modularity.

FUNCTIONS:
    1. validate_url() - Validate YouTube URL format
    2. validate_folder() - Validate destination folder accessibility
    3. get_video_info() - Retrieve video metadata
    4. get_best_stream() - Select best quality stream
    5. get_file_size_mb() - Convert file size to MB
    6. get_safe_filename() - Generate safe filename from title
    7. validate_input() - General input validation

DEVELOPED BY: Lacshan Shakthivel
DATE: December 3, 2025

================================================================================
"""

from pytube import YouTube
from pytube.exceptions import RegexMatchError, VideoUnavailable
import os


def validate_url(url):
    """
    Validate if the provided URL is a valid YouTube URL.
    
    Args:
        url (str): The URL to validate
        
    Returns:
        tuple: (is_valid, error_message)
            - is_valid (bool): True if URL is valid, False otherwise
            - error_message (str): Error message if invalid, None if valid
    """
    if not url or not url.strip():
        return False, "URL cannot be empty."
    
    url = url.strip()
    
    # Check if URL contains YouTube domain
    if "youtube.com" not in url and "youtu.be" not in url:
        return False, "Invalid URL: Must be a YouTube link."
    
    # Check if URL starts with http or https
    if not url.startswith("http://") and not url.startswith("https://"):
        return False, "Invalid URL: Must start with http:// or https://"
    
    return True, None


def validate_folder(folder_path):
    """
    Validate if the destination folder exists and is accessible.
    
    Args:
        folder_path (str): The folder path to validate
        
    Returns:
        tuple: (is_valid, error_message)
            - is_valid (bool): True if folder is valid, False otherwise
            - error_message (str): Error message if invalid, None if valid
    """
    if not folder_path or not folder_path.strip():
        return False, "Folder path cannot be empty."
    
    folder_path = folder_path.strip()
    
    # Check if folder exists
    if not os.path.exists(folder_path):
        return False, f"Folder does not exist: {folder_path}"
    
    # Check if it's actually a directory
    if not os.path.isdir(folder_path):
        return False, f"Path is not a directory: {folder_path}"
    
    # Check if we have write permissions
    if not os.access(folder_path, os.W_OK):
        return False, f"No write permission for folder: {folder_path}"
    
    return True, None


def get_video_info(url):
    """
    Retrieve information about the YouTube video.
    
    Args:
        url (str): The YouTube video URL
        
    Returns:
        tuple: (yt_object, error_message)
            - yt_object (YouTube): YouTube object if successful, None otherwise
            - error_message (str): Error message if failed, None if successful
    """
    try:
        yt = YouTube(url)
        return yt, None
    except RegexMatchError:
        return None, "Invalid YouTube URL format."
    except VideoUnavailable:
        return None, "Video is unavailable or has been removed."
    except Exception as e:
        return None, f"Error accessing video: {str(e)}"


def get_best_stream(yt):
    """
    Get the highest quality stream available for the video.
    
    Args:
        yt (YouTube): The YouTube object
        
    Returns:
        tuple: (stream, error_message)
            - stream (Stream): The video stream object if successful
            - error_message (str): Error message if failed
    """
    try:
        # Get the highest quality progressive stream (video + audio)
        stream = yt.streams.filter(progressive=True).order_by('resolution').desc().first()
        
        if stream is None:
            # Fallback to highest quality available
            stream = yt.streams.get_highest_resolution()
        
        if stream is None:
            return None, "No downloadable streams available for this video."
        
        return stream, None
    except Exception as e:
        return None, f"Error selecting stream: {str(e)}"


def get_file_size_mb(stream):
    """
    Get the file size of the stream in megabytes.
    
    Args:
        stream (Stream): The stream object
        
    Returns:
        float: File size in MB
    """
    if stream and stream.filesize:
        return stream.filesize / (1024 * 1024)
    return 0.0


def get_safe_filename(title, max_length=200):
    """
    Generate a safe filename from video title.
    
    Args:
        title (str): The video title
        max_length (int): Maximum filename length (default 200)
        
    Returns:
        str: Safe filename
    """
    if not title:
        return "video"
    
    # Remove invalid filename characters
    invalid_chars = '<>:"/\\|?*'
    safe_name = "".join(c if c not in invalid_chars else "_" for c in title)
    
    # Truncate to max length if needed
    if len(safe_name) > max_length:
        safe_name = safe_name[:max_length]
    
    return safe_name.strip()


def validate_input(input_string, input_type="general"):
    """
    Validate user input based on type.
    
    Args:
        input_string (str): The input to validate
        input_type (str): Type of validation ('url', 'folder', 'choice', or 'general')
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not input_string or not input_string.strip():
        return False
    
    if input_type == "url":
        is_valid, _ = validate_url(input_string)
        return is_valid
    elif input_type == "folder":
        is_valid, _ = validate_folder(input_string)
        return is_valid
    elif input_type == "choice":
        return input_string.lower() in ['yes', 'y', 'no', 'n']
    else:
        return True

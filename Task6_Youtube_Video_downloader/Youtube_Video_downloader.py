"""
================================================================================
                    YOUTUBE VIDEO DOWNLOADER APPLICATION
================================================================================

PROGRAM DESCRIPTION:
    This application allows users to download YouTube videos to their local
    computer. It provides a user-friendly interface for downloading videos
    with various quality options and comprehensive error handling.

KEY FEATURES:
    1. Download YouTube videos by URL
    2. Choose destination folder for downloads
    3. Select video quality (highest available by default)
    4. Comprehensive error handling for invalid links
    5. Progress display during download
    6. File naming with video title

LIBRARY USED:
    • pytube: Python library for downloading YouTube videos
    • os: For file path operations

ERROR HANDLING:
    • Invalid URL validation
    • Network connection errors
    • Folder accessibility checks
    • Video availability verification

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


def download_video(yt, stream, folder_path):
    """
    Download the video to the specified folder.
    
    Args:
        yt (YouTube): The YouTube object
        stream (Stream): The stream to download
        folder_path (str): The destination folder
        
    Returns:
        tuple: (success, message)
            - success (bool): True if successful, False otherwise
            - message (str): Success or error message
    """
    try:
        print("\n" + "="*60)
        print("DOWNLOADING VIDEO")
        print("="*60)
        print(f"Title: {yt.title}")
        print(f"Resolution: {stream.resolution}")
        print(f"File Size: ~{stream.filesize / (1024*1024):.2f} MB")
        print(f"Destination: {folder_path}")
        print("-"*60)
        
        # Download the stream
        stream.download(output_path=folder_path)
        
        filename = stream.default_filename if stream.default_filename else yt.title
        return True, f"✅ Video downloaded successfully: {filename}"
    
    except Exception as e:
        return False, f"❌ Download failed: {str(e)}"


def get_user_url():
    """
    Prompt user to enter a YouTube URL.
    
    Returns:
        str: The entered URL
    """
    print("\n" + "="*60)
    print("YOUTUBE VIDEO DOWNLOADER")
    print("="*60)
    url = input("\nEnter YouTube URL: ").strip()
    return url


def get_destination_folder():
    """
    Prompt user to enter the destination folder path.
    
    Returns:
        str: The destination folder path
    """
    folder = input("Enter destination folder path: ").strip()
    return folder


def display_error(error_message):
    """
    Display error message to user.
    
    Args:
        error_message (str): The error message to display
    """
    print(f"\n❌ Error: {error_message}\n")


def ask_continue():
    """
    Ask user if they want to download another video.
    
    Returns:
        bool: True if user wants to continue, False otherwise
    """
    print("\n" + "-"*60)
    choice = input("Download another video? (yes/no): ").strip().lower()
    return choice in ['yes', 'y']


def downloader():
    """
    Main downloader loop - handles the complete download workflow.
    """
    while True:
        # Get URL from user
        url = get_user_url()
        
        # Validate URL
        is_valid_url, url_error = validate_url(url)
        if not is_valid_url:
            display_error(url_error)
            continue
        
        # Get destination folder
        folder = get_destination_folder()
        
        # Validate folder
        is_valid_folder, folder_error = validate_folder(folder)
        if not is_valid_folder:
            display_error(folder_error)
            continue
        
        # Get video information
        yt, video_error = get_video_info(url)
        if yt is None:
            display_error(video_error)
            continue
        
        # Get best stream
        stream, stream_error = get_best_stream(yt)
        if stream is None:
            display_error(stream_error)
            continue
        
        # Download video
        success, message = download_video(yt, stream, folder)
        print(message)
        
        # Ask if user wants to continue
        if not ask_continue():
            print("\n" + "="*60)
            print("Thank you for using YouTube Video Downloader!")
            print("="*60 + "\n")
            break


def main():
    """
    Entry point of the application.
    """
    try:
        downloader()
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("Application terminated by user.")
        print("="*60 + "\n")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}\n")


if __name__ == "__main__":
    main()

# youtube.py
import webbrowser

VIDEO_ID = "6zNHZkT3DXk"

def play_youtube_video_in_brave():
    # YouTube URL with the video ID
    youtube_url = f"https://www.youtube.com/watch?v={VIDEO_ID}"
    
    # Open the URL in the Brave browser (on macOS)
    try:
        webbrowser.get("open -a /Applications/Brave\ Browser.app %s").open(youtube_url)
    except webbrowser.Error:
        print("Failed to open the Brave browser. Please make sure it's installed and try again.")
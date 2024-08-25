from pytube import YouTube
from pytube import Playlist

playlist = Playlist("https://www.youtube.com/playlist?list=PLs8CZ4blcEKvtVJ7LbOSP5NdNxEndzvDG").video_urls

for video_link in playlist:
  
    try:
        YouTube(video_link).streams.first().download()
    
    except:
        print(video_link + " unavailable")
        
# Amb aquest codi:
    # 52 videos downloaded
    # 59 videos unavailable
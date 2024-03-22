import requests
from pytube import YouTube
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
}

def get_url():
    while True:
        try:
            url = input("Playlist URL: ")
            return url
        except Exception as e:
            print("Invalid URL.")

def get_video_links(url):
    try:
        pagereq = requests.get(url, headers=headers)
        pagesoup = BeautifulSoup(pagereq.content, "html.parser")
        page = pagesoup.find_all("script")
        page = str(page).split(",")
        videos = []
        for video in page:
            if "watch?" in str(video):
                if '"url":' in str(video) and "i.ytimg.com" not in str(video):
                    video = video.split('"url":"')[1].split(r"\u0026list")[0]
                    videos.append(f"https://youtube.com{video}")
        return videos
    except Exception as e:
        print("Error fetching video links:", e)
        return []


def download_video(link):
    try:
        youtubeObject = YouTube(link)
        youtubeObject = youtubeObject.streams.get_audio_only()
        #youtubeObject = youtubeObject.streams.get_highest_resolution()
        youtubeObject.download()
        print("Download completed successfully")
    except KeyboardInterrupt:
        print("\nFinishing...")
    except Exception as e:
        print("An error has occurred while downloading:", e)

if __name__ == "__main__":
    try:
        url = get_url()
        videos = get_video_links(url)
        for link in videos:
            download_video(link)
    except KeyboardInterrupt:
        print("\nFinishing...")

import os
import requests
import random

PEXELS_API_KEY = "API_KEY"
PIXABAY_API_KEY = "API_KEY"

SEARCH_QUERIES = ["atomic bomb", "nuclear explosion", "radiation effects"]
MAX_VIDEOS = 10  # Общее число видео
VIDEO_FOLDER = "videos"
os.makedirs(VIDEO_FOLDER, exist_ok=True)


def search_pexels_videos(query, max_results=5):
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": max_results}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return [v["video_files"][0]["link"] for v in response.json().get("videos", [])]
    return []


def search_pixabay_videos(query, max_results=5):
    url = f"https://pixabay.com/api/videos/?key={PIXABAY_API_KEY}&q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return [v["videos"]["large"]["url"] for v in response.json().get("hits", [])[:max_results]]
    return []


def search_coverr_videos(query, max_results=5):
    url = f"https://coverr.co/api/videos?query={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return [f"https://coverr.co{v['video']['mp4']}" for v in response.json().get("videos", [])[:max_results]]
    return []


def download_video(video_url, save_path):
    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        return save_path
    return None


def main():
    print("Поиск видео...")
    all_videos = []

    for query in SEARCH_QUERIES:
        all_videos.extend(search_pexels_videos(query, max_results=3))
        all_videos.extend(search_pixabay_videos(query, max_results=3))
        all_videos.extend(search_coverr_videos(query, max_results=3))

    random.shuffle(all_videos)
    selected_videos = all_videos[:MAX_VIDEOS]

    print(f"Скачиваем {len(selected_videos)} видео...")
    video_files = []
    for i, url in enumerate(selected_videos):
        filename = os.path.join(VIDEO_FOLDER, f"video_{i}.mp4")
        if download_video(url, filename):
            video_files.append(filename)

    print("Скачаны файлы:", video_files)


if __name__ == "__main__":
    main()

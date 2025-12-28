import requests
import os

urls = [
    "https://raw.githubusercontent.com/chinese-poetry/chinese-poetry/master/%E5%85%A8%E5%94%90%E8%AF%97/poet.tang.0.json",
    "https://raw.githubusercontent.com/chinese-poetry/chinese-poetry/master/%E5%85%A8%E5%94%90%E8%AF%97/poet.tang.1.json",
    "https://raw.githubusercontent.com/chinese-poetry/chinese-poetry/master/%E5%AE%8B%E8%AF%8D/ci.song.0.json",
    "https://raw.githubusercontent.com/chinese-poetry/chinese-poetry/master/%E5%AE%8B%E8%AF%8D/ci.song.1.json",
    "https://raw.githubusercontent.com/chinese-poetry/chinese-poetry/master/%E8%AE%BA%E8%AF%AD/lunyu.json",
    "https://raw.githubusercontent.com/chinese-poetry/chinese-poetry/master/%E8%AF%97%E7%BB%8F/shijing.json"
]

os.makedirs("data", exist_ok=True)

for i, url in enumerate(urls):
    filename = url.split('/')[-1]
    print(f"Downloading {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(f"data/{filename}", "wb") as f:
            f.write(response.content)
        print(f"Saved to data/{filename}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# Globe News
> Real-time news from every corner of the world; click any country on a rotating 3D Earth. It's a news geo-visualization tool based on python; instead of scrolling a flat news feed, you get spatial context. You immediately understand where something is happening on Earth, not just a country name in a headline.

## Use cases:
- 1.Journalists & researchers monitoring breaking news across regions without switching accross multiple tabs.
- 2.Students learning geography + current events together the spatial memory helps retention.
- 3.Travelers quickly checking what's happening in a country before visiting.
- 4.Teachers using it as a classroom tool for current affairs discussion.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.6-green)
![License](https://img.shields.io/badge/License-MIT-yellow)


##  Features
- 3D Earth rendered from scratch using pure pygame geometry
- 30+ countries as clickable markers with real lat/lon positions
- Live news fetched from BBC RSS feeds per country/region
- Drag to spin the globe freely
- Non-blocking news fetch (background threading)
- Back-hemisphere culling — dots hide when rotated away

### Prerequisites
Python 3.10+

### Installation
```bash
git clone https://github.com/yourusername/globe-news.git
cd globe-news
pip install pygame feedparser numpy
python globe_news.py
```

## 🎮 Controls
| Action | Result |
|--------|--------|
| Click a dot | Load news for that country |
| Click + drag | Rotate the globe |
| ESC | Quit |

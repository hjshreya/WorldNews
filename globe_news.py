import pygame
import numpy as np
import math
import feedparser
import threading
import time
import textwrap
import urllib.request

#Window & colors 
W, H = 1200, 750
BG       = (8,  12,  24)
OCEAN    = (15,  55, 110)
LAND     = (34,  85,  45)
LAND_HI  = (60, 160,  70)
BORDER   = (90, 130,  80)
GRID     = (20,  60, 100)
WHITE    = (255,255,255)
YELLOW   = (255,220,  60)
CYAN     = ( 80,220,255)
RED      = (220,  60,  60)
PANEL_BG = ( 14,  20,  38)
CARD_BG  = ( 22,  30,  52)
ACCENT   = ( 60, 140,255)
MUTED    = (120,140,175)
GLOW     = ( 40, 100,220)

#Countries: name → (lat, lon, rss_url, flag_emoji)
COUNTRIES = {
    "India":         ( 20.0,  78.0, "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml",    "🇮🇳"),
    "USA":           ( 38.0, -97.0, "https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml", "🇺🇸"),
    "UK":            ( 54.0,  -2.0, "https://feeds.bbci.co.uk/news/uk/rss.xml",                  "🇬🇧"),
    "China":         ( 35.0, 105.0, "https://feeds.bbci.co.uk/news/world/asia/rss.xml",          "🇨🇳"),
    "Russia":        ( 60.0,  90.0, "https://www.themoscowtimes.com/rss/news",                   "🇷🇺"),
    "Germany":       ( 51.0,  10.0, "https://feeds.bbci.co.uk/news/world/europe/rss.xml",        "🇩🇪"),
    "France":        ( 46.0,   2.0, "https://feeds.bbci.co.uk/news/world/europe/rss.xml",        "🇫🇷"),
    "Brazil":        (-14.0, -51.0, "https://feeds.bbci.co.uk/news/world/latin_america/rss.xml", "🇧🇷"),
    "Australia":     (-25.0, 133.0, "https://feeds.bbci.co.uk/news/world/australia/rss.xml",     "🇦🇺"),
    "Japan":         ( 36.0, 138.0, "https://feeds.bbci.co.uk/news/world/asia/rss.xml",          "🇯🇵"),
    "Canada":        ( 56.0, -96.0, "https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml", "🇨🇦"),
    "South Africa":  (-29.0,  25.0, "https://feeds.bbci.co.uk/news/world/africa/rss.xml",        "🇿🇦"),
    "Nigeria":       ( 10.0,   8.0, "https://feeds.bbci.co.uk/news/world/africa/rss.xml",        "🇳🇬"),
    "Egypt":         ( 26.0,  30.0, "https://feeds.bbci.co.uk/news/world/middle_east/rss.xml",   "🇪🇬"),
    "Mexico":        ( 23.0, -102.0,"https://feeds.bbci.co.uk/news/world/latin_america/rss.xml", "🇲🇽"),
    "Argentina":     (-38.0, -63.0, "https://feeds.bbci.co.uk/news/world/latin_america/rss.xml", "🇦🇷"),
    "Pakistan":      ( 30.0,  70.0, "https://feeds.bbci.co.uk/news/world/asia/rss.xml",          "🇵🇰"),
    "Indonesia":     ( -5.0, 120.0, "https://feeds.bbci.co.uk/news/world/asia/rss.xml",          "🇮🇩"),
    "Turkey":        ( 39.0,  35.0, "https://feeds.bbci.co.uk/news/world/middle_east/rss.xml",   "🇹🇷"),
    "Saudi Arabia":  ( 24.0,  45.0, "https://feeds.bbci.co.uk/news/world/middle_east/rss.xml",   "🇸🇦"),
    "Iran":          ( 32.0,  53.0, "https://feeds.bbci.co.uk/news/world/middle_east/rss.xml",   "🇮🇷"),
    "Ukraine":       ( 49.0,  32.0, "https://feeds.bbci.co.uk/news/world/europe/rss.xml",        "🇺🇦"),
    "South Korea":   ( 36.0, 128.0, "https://feeds.bbci.co.uk/news/world/asia/rss.xml",          "🇰🇷"),
    "Israel":        ( 31.0,  35.0, "https://feeds.bbci.co.uk/news/world/middle_east/rss.xml",   "🇮🇱"),
    "Kenya":         ( -1.0,  37.0, "https://feeds.bbci.co.uk/news/world/africa/rss.xml",        "🇰🇪"),
    "Italy":         ( 42.0,  12.0, "https://feeds.bbci.co.uk/news/world/europe/rss.xml",        "🇮🇹"),
    "Spain":         ( 40.0,  -4.0, "https://feeds.bbci.co.uk/news/world/europe/rss.xml",        "🇪🇸"),
    "Thailand":      ( 15.0, 101.0, "https://feeds.bbci.co.uk/news/world/asia/rss.xml",          "🇹🇭"),
    "Vietnam":       ( 16.0, 108.0, "https://feeds.bbci.co.uk/news/world/asia/rss.xml",          "🇻🇳"),
    "Philippines":   ( 13.0, 122.0, "https://feeds.bbci.co.uk/news/world/asia/rss.xml",          "🇵🇭"),
}

# Landmass polygons (simplified outlines, lat/lon pairs)
# Each entry: list of (lat, lon) polygons
LANDMASSES = {
    "north_america": [
        [(70,-140),(72,-120),(68,-85),(60,-65),(47,-53),(44,-66),(35,-76),(30,-80),
         (25,-80),(20,-87),(15,-83),(8,-77),(8,-77),(10,-85),(14,-87),(15,-90),
         (16,-92),(20,-90),(22,-80),(24,-82),(25,-82),(30,-98),(32,-117),(37,-122),
         (47,-124),(50,-127),(54,-132),(58,-137),(60,-141),(65,-140),(70,-140)],
    ],
    "south_america": [
        [(12,-72),(10,-62),(8,-60),(5,-52),(0,-50),(-5,-35),(-10,-37),(-15,-39),
         (-22,-43),(-30,-50),(-38,-57),(-45,-65),(-52,-68),(-55,-65),(-52,-58),
         (-45,-55),(-30,-50),(-22,-42),(-10,-40),(-5,-35),(0,-50),(5,-52),
         (8,-60),(10,-62),(12,-72)],
    ],
    "europe": [
        [(71,28),(70,20),(58,5),(48,-5),(43,-9),(36,-6),(36,3),(40,18),(42,28),
         (45,30),(47,38),(60,25),(64,26),(70,28),(71,28)],
    ],
    "africa": [
        [(37,10),(30,32),(10,42),(0,42),(-10,40),(-20,35),(-34,26),(-34,18),
         (-30,17),(-20,12),(-5,10),(5,5),(5,-5),(10,-16),(15,-17),(20,-17),
         (30,-10),(37,10)],
    ],
    "asia": [
        [(70,30),(55,30),(40,27),(35,36),(25,57),(22,60),(12,44),(8,45),(10,50),
         (22,60),(25,67),(25,90),(20,93),(10,99),(5,103),(5,115),(15,120),
         (22,114),(30,122),(40,122),(50,140),(60,140),(65,142),(70,145),(70,105),
         (75,90),(73,80),(70,65),(70,55),(70,45),(70,35),(70,30)],
    ],
    "australia": [
        [(-15,129),(-12,130),(-14,136),(-12,136),(-14,141),(-16,145),(-22,150),
         (-28,153),(-34,151),(-37,150),(-38,146),(-38,140),(-32,133),(-32,127),
         (-22,114),(-15,124),(-14,128),(-15,129)],
    ],
    "greenland": [
        [(83,-25),(76,-18),(68,-26),(61,-42),(61,-48),(65,-52),(70,-52),(76,-46),(83,-30),(83,-25)],
    ],
    "japan_honshu": [
        [(41,141),(38,141),(35,137),(34,131),(34,130),(35,132),(37,136),(38,140),(41,141)],
    ],
    "uk": [
        [(58,-5),(53,-5),(50,-5),(51,0),(53,0),(55,0),(58,-3),(58,-5)],
    ],
    "new_zealand_n": [
        [(-36,174),(-37,176),(-39,177),(-41,175),(-38,174),(-36,174)],
    ],
    "sri_lanka": [
        [(9,80),(7,81),(6,81),(6,80),(8,80),(9,80)],
    ],
    "madagascar": [
        [(-13,49),(-17,50),(-20,48),(-24,43),(-26,44),(-20,48),(-16,50),(-13,49)],
    ],
}

def latlon_to_3d(lat, lon, r=1.0):
    la, lo = math.radians(lat), math.radians(lon)
    x = r * math.cos(la) * math.cos(lo)
    y = r * math.sin(la)
    z = r * math.cos(la) * math.sin(lo)
    return np.array([x, y, z])

def project(v, rot_y, cx, cy, R):
    """Rotate around Y axis, then simple perspective project."""
    c, s = math.cos(rot_y), math.sin(rot_y)
    x =  v[0]*c + v[2]*s
    y =  v[1]
    z = -v[0]*s + v[2]*c
    if z < -0.3:
        return None
    scale = R / (1.2 - z * 0.4)
    sx = int(cx + x * scale)
    sy = int(cy - y * scale)
    return sx, sy

def draw_globe(surf, rot_y, cx, cy, R, highlight=None):
    # Sphere fill
    pygame.draw.circle(surf, OCEAN, (cx, cy), R)

    # Lat/lon grid
    for lat in range(-80, 81, 20):
        pts = []
        for lon in range(-180, 181, 5):
            p = project(latlon_to_3d(lat, lon), rot_y, cx, cy, R)
            if p:
                pts.append(p)
        if len(pts) > 1:
            pygame.draw.lines(surf, GRID, False, pts, 1)
    for lon in range(-180, 181, 20):
        pts = []
        for lat in range(-85, 86, 5):
            p = project(latlon_to_3d(lat, lon), rot_y, cx, cy, R)
            if p:
                pts.append(p)
        if len(pts) > 1:
            pygame.draw.lines(surf, GRID, False, pts, 1)

    # Landmasses
    for name, polys in LANDMASSES.items():

        for poly in polys:
            pts = []
            for lat, lon in poly:
                p = project(latlon_to_3d(lat, lon), rot_y, cx, cy, R)
                if p:
                    pts.append(p)
            if len(pts) >= 3:
                pygame.draw.polygon(surf, LAND, pts)
                pygame.draw.lines(surf, BORDER, True, pts, 1)

    # Globe rim glow
    pygame.draw.circle(surf, GLOW, (cx, cy), R, 3)

def draw_country_dots(surf, rot_y, cx, cy, R, font_sm, selected):
    dots = []
    for name, (lat, lon, rss, flag) in COUNTRIES.items():
        v = latlon_to_3d(lat, lon)
        p = project(v, rot_y, cx, cy, R)
        if not p:
            continue
        is_sel = (name == selected)
        color  = YELLOW if is_sel else CYAN
        r_dot  = 7 if is_sel else 4
        pygame.draw.circle(surf, (0,0,0,0), p, r_dot+2)
        pygame.draw.circle(surf, color, p, r_dot)
        if is_sel:
            pygame.draw.circle(surf, WHITE, p, r_dot+3, 2)
        label = font_sm.render(name, True, WHITE if is_sel else MUTED)
        surf.blit(label, (p[0]+9, p[1]-7))
        dots.append((name, p))
    return dots

def fetch_news(country_name, rss_url, result_store):
    """Fetch RSS in background thread."""
    result_store["loading"] = True
    result_store["country"] = country_name
    result_store["articles"] = []
    result_store["error"] = None
    try:
        feed = feedparser.parse(rss_url)
        articles = []
        for entry in feed.entries[:8]:
            title   = entry.get("title", "")
            summary = entry.get("summary", entry.get("description", ""))
            # strip HTML tags simply
            import re
            summary = re.sub(r"<[^>]+>", "", summary)[:200]
            articles.append({"title": title, "summary": summary})
        result_store["articles"] = articles
    except Exception as e:
        result_store["error"] = str(e)
    result_store["loading"] = False

def wrap_text(text, font, max_w):
    words = text.split()
    lines, line = [], []
    for w in words:
        test = " ".join(line + [w])
        if font.size(test)[0] <= max_w:
            line.append(w)
        else:
            if line:
                lines.append(" ".join(line))
            line = [w]
    if line:
        lines.append(" ".join(line))
    return lines

def draw_panel(surf, result, fonts, panel_rect):
    px, py, pw, ph = panel_rect
    pygame.draw.rect(surf, PANEL_BG, panel_rect, border_radius=12)
    pygame.draw.rect(surf, ACCENT,   panel_rect, 1, border_radius=12)

    font_h, font_b, font_s, font_xs = fonts
    country = result.get("country", "")
    flag    = COUNTRIES.get(country, ("","","",""))[3] if country else ""

    y = py + 18
    # header
    pygame.draw.rect(surf, CARD_BG, (px+8, y, pw-16, 44), border_radius=8)
    htxt = font_h.render(f"{flag}  {country}", True, WHITE)
    surf.blit(htxt, (px+18, y+10))
    y += 56

    if result.get("loading"):
        anim = "Loading" + "." * (int(time.time()*3) % 4)
        t = font_b.render(anim, True, CYAN)
        surf.blit(t, (px+18, y))
        return

    if result.get("error"):
        t = font_s.render("Could not fetch news", True, RED)
        surf.blit(t, (px+18, y))
        return

    articles = result.get("articles", [])
    if not articles:
        t = font_s.render("Click a country to see news", True, MUTED)
        surf.blit(t, (px+18, y))
        return

    for i, art in enumerate(articles):
        if y > py + ph - 30:
            break
        # card
        card_h = 70
        lines_title = wrap_text(art["title"], font_b, pw-40)[:2]
        card_h = 16 + len(lines_title)*18 + 8
        if y + card_h > py + ph - 10:
            break
        pygame.draw.rect(surf, CARD_BG, (px+8, y, pw-16, card_h), border_radius=6)
        pygame.draw.rect(surf, GLOW,    (px+8, y, 3, card_h), border_radius=3)
        ty = y + 8
        for line in lines_title:
            txt = font_b.render(line, True, WHITE)
            surf.blit(txt, (px+18, ty))
            ty += 18
        y += card_h + 6

def get_clicked_country(dot_positions, mx, my, rot_y, cx, cy, R):
    best, best_d = None, 16
    for name, p in dot_positions:
        d = math.hypot(mx - p[0], my - p[1])
        if d < best_d:
            best, best_d = name, d
    return best

def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("🌍  Globe News — click any country")
    clock  = pygame.time.Clock()

    # Fonts
    def try_font(names, size):
        for n in names:
            try:
                return pygame.font.SysFont(n, size)
            except:
                pass
        return pygame.font.Font(None, size)

    font_h  = try_font(["notosans","ubuntu","dejavusans","freesans"], 20)
    font_b  = try_font(["notosans","ubuntu","dejavusans","freesans"], 14)
    font_s  = try_font(["notosans","ubuntu","dejavusans","freesans"], 13)
    font_xs = try_font(["notosans","ubuntu","dejavusans","freesans"], 11)

    R   = 270       # globe radius
    cx  = W//2 - 90 # globe centre x (shifted left for panel)
    cy  = H//2

    rot_y       = 0.0
    auto_spin   = 0.002
    dragging    = False
    drag_x      = 0
    drag_rot    = 0.0

    selected    = None
    news_result = {"loading": False, "country": None, "articles": [], "error": None}
    dot_positions = []

    panel_rect  = (W - 330, 10, 320, H - 20)

    while True:
        dt = clock.tick(60)
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if mx < W - 340:   # clicked on globe side
                    hit = get_clicked_country(dot_positions, mx, my, rot_y, cx, cy, R)
                    if hit:
                        selected = hit
                        rss = COUNTRIES[hit][2]
                        news_result = {"loading": True, "country": hit, "articles": [], "error": None}
                        t = threading.Thread(target=fetch_news, args=(hit, rss, news_result), daemon=True)
                        t.start()
                    else:
                        dragging = True
                        drag_x   = mx
                        drag_rot = rot_y

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False

            if event.type == pygame.MOUSEMOTION and dragging:
                delta = mx - drag_x
                rot_y = drag_rot + delta * 0.005

        if not dragging:
            rot_y += auto_spin

        #Draw
        screen.fill(BG)

        # Stars
        rng = np.random.default_rng(42)
        for sx, sy, br in zip(rng.integers(0,W,120), rng.integers(0,H,120), rng.integers(80,220,120)):
            pygame.draw.circle(screen, (br,br,br), (sx,sy), 1)

        draw_globe(screen, rot_y, cx, cy, R, selected)
        dot_positions = draw_country_dots(screen, rot_y, cx, cy, R, font_xs, selected)
        draw_panel(screen, news_result, (font_h, font_b, font_s, font_xs), panel_rect)

        # Help text
        hint = font_xs.render("click a dot · drag to spin · ESC to quit", True, MUTED)
        screen.blit(hint, (10, H-22))

        title = font_h.render("🌍  Globe News", True, WHITE)
        screen.blit(title, (12, 12))

        pygame.display.flip()

if __name__ == "__main__":
    main()

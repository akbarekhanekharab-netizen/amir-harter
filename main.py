import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
import shutil

OUTPUT_DIR = Path('site')
OUTPUT_DIR.mkdir(exist_ok=True)

team_names = {
    "Arsenal": "آرسنال",
    "Chelsea": "چلسی",
    "Liverpool": "لیورپول",
    "Manchester City": "منچستر سیتی",
    "Manchester United": "منچستر یونایتد",
    "Real Madrid": "رئال مادرید",
    "Barcelona": "بارسلونا",
    "Inter": "اینتر",
    "AC Milan": "میلان",
    "Juventus": "یوونتوس",
    "Napoli": "ناپولی",
    "Roma": "رم",
    "Lazio": "لاتزیو",
    "Atalanta": "آتالانتا",
    "Bayern Munich": "بایرن مونیخ",
    "Dortmund": "دورتموند",
    "Leipzig": "لایپزیگ",
    "Leverkusen": "لورکوزن",
    "Frankfurt": "فرانکفورت",
    "Stuttgart": "اشتوتگارت",
    "PSG": "پاری سن ژرمن",
    "Marseille": "مارسی",
    "Lyon": "لیون",
    "Monaco": "موناکو",
    "Lille": "لیل",
    "Nice": "نیس",
    "Lens": "لانس",
    "Rennes": "رن",
    "Strasbourg": "استراسبورگ",
    "Nantes": "نانت",
    "Toulouse": "تولوز",
    "Montpellier": "مون‌پولیه",
    "Brest": "برست",
    "Angers": "آنژه",
    "Auxerre": "اوسر",
    "Troyes": "تروا",
    "Freiburg": "فرایبورگ",
    "Mainz": "ماینتس",
    "Augsburg": "آگسبورگ",
    "Fiorentina": "فیورنتینا",
    "Bologna": "بولونیا",
    "Parma": "پارما",
    "Monza": "مونتزا",
    "Venezia": "ونتزیا",
    "Tottenham": "تاتنهام",
    "Newcastle": "نیوکاسل",
    "Everton": "اورتون",
    "West Ham": "وست هم",
    "Fulham": "فولام",
    "Wolves": "ولورهمپتون",
    "Valencia": "والنسیا",
    "Sevilla": "سویا",
    "Villarreal": "ویارئال",
    "Atletico Madrid": "اتلتیکو مادرید",
    "Deportivo Alavés": "آلاوس",
    "CA Osasuna": "اوساسونا",
    "Málaga CF": "مالاگا",
    "Levante UD": "لوانته",
    "US Sassuolo Calcio": "ساسولو"
}

iran_teams = {
    "Persepolis": "پرسپولیس",
    "Esteghlal": "استقلال",
    "Sepahan": "سپاهان",
    "Tractor": "تراکتور",
    "Foolad Khuzestan": "فولاد",
    "Gol Gohar Sirjan": "گل گهر",
    "Malavan": "ملوان",
    "Nassaji Mazandaran": "نساجی",
    "Zob Ahan": "ذوب آهن",
    "Aluminium Arak": "آلومینیوم",
    "Shams Azar Qazvin": "شمس آذر",
    "Kheybar Khorramabad": "خیبر",
    "Sanat Naft": "صنعت نفت",
    "Fajr Sepasi Shiraz": "فجر سپاسی",
    "Chadormalou Ardakan": "چادرملو",
    "Havadar": "هوادار",
    "Paykan": "پیکان",
    "Mes Shahr-e Babak": "مس شهر بابک",
    "Esteghlal Khuzestan": "استقلال خوزستان"
}

team_ids = {
    "139013": "پرسپولیس",
    "139012": "استقلال",
    "139014": "سپاهان",
    "139162": "تراکتور",
    "139165": "فولاد",
    "139157": "گل گهر",
    "139183": "ملوان",
    "139158": "نساجی",
    "139159": "ذوب آهن",
    "139172": "آلومینیوم",
    "144143": "شمس آذر",
    "141318": "خیبر",
    "139166": "صنعت نفت",
    "139173": "فجر سپاسی",
    "149162": "چادرملو",
    "141317": "هوادار",
    "139164": "پیکان",
    "144140": "مس شهر بابک",
    "139184": "استقلال خوزستان"
}

provinces = {
    "تهران": (35.6892, 51.3890),
    "مشهد": (36.2605, 59.6168),
    "اصفهان": (32.6546, 51.6680),
    "شیراز": (29.5918, 52.5837),
    "تبریز": (38.0962, 46.2738),
    "اهواز": (31.3183, 48.6706),
    "قم": (34.6416, 50.8746),
    "کرج": (35.8400, 50.9391),
    "کرمانشاه": (34.3142, 47.0650),
    "رشت": (37.2808, 49.5832),
    "زاهدان": (29.4963, 60.8629),
    "همدان": (34.7983, 48.5148),
    "ارومیه": (37.5527, 45.0760),
    "یزد": (31.8974, 54.3569),
    "اردبیل": (38.2498, 48.2933),
    "بندرعباس": (27.1832, 56.2666),
    "اراک": (34.0949, 49.7016),
    "زنجان": (36.6830, 48.5087),
    "سنندج": (35.3219, 46.9862),
    "قزوین": (36.2860, 50.0040),
    "خرم‌آباد": (33.4871, 48.3558),
    "گرگان": (36.8386, 54.4346),
    "ساری": (36.5633, 53.0601),
    "بوشهر": (28.9234, 50.8203),
    "بیرجند": (32.8649, 59.2212),
    "ایلام": (33.6375, 46.4227),
    "شهرکرد": (32.3256, 50.8644),
    "یاسوج": (30.6684, 51.5875),
    "بجنورد": (37.4749, 57.3290),
    "سمنان": (35.5729, 53.3971)
}

valid_leagues = ["PL", "PD", "SA", "BL1", "FL1"]

def translate_team(name):
    for eng, fa in team_names.items():
        if eng.lower() in name.lower():
            return fa
    return name

def get_news():
    sources = [
        ("ایسنا", "https://www.isna.ir/rss"),
        ("همشهری", "https://www.hamshahrionline.ir/rss"),
        ("خبرآنلاین", "https://www.khabaronline.ir/rss")
    ]
    news_items = ""
    for name, url in sources:
        try:
            response = requests.get(url, timeout=10)
            root = ET.fromstring(response.text)
            for item in root.findall(".//item")[:15]:
                title = item.find("title").text
                link = item.find("link").text
                news_items += f'<div class="news-item" onclick="window.open(\'{link}\', \'_blank\')"><span>📰</span>{title}</div>'
        except:
            pass
    return news_items

def get_weather(lat=35.6892, lon=51.3890, city="تهران"):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&timezone=Asia%2FTehran"
        response = requests.get(url, timeout=10)
        data = response.json()
        temp = data["current_weather"]["temperature"]
        wind = data["current_weather"]["windspeed"]
        code = data["current_weather"]["weathercode"]
        weather_desc = {0: "آفتابی", 1: "نیمه آفتابی", 2: "نیمه ابری", 3: "ابری", 45: "مه", 61: "باران", 71: "برف"}
        desc = weather_desc.get(code, "نامشخص")
        return f'<div class="weather-icon">🌤</div><div class="weather-temp">{temp}°C</div><div class="weather-desc">{city}<br>{desc}<br>باد: {wind} km/h</div>'
    except:
        return '<div class="weather-icon">🌤</div><div class="weather-temp">--°C</div><div class="weather-desc">در دسترس نیست</div>'

def get_currency():
    currencies = [
        ("دلار", "price_dollar_rl"),
        ("یورو", "price_eur"),
        ("درهم", "price_aed"),
        ("پوند", "price_gbp"),
        ("لیر ترکیه", "price_try"),
        ("یوان چین", "price_cny"),
        ("روبل روسیه", "price_rub"),
        ("دینار عراق", "price_iqd"),
        ("افغانی", "price_afn"),
        ("سکه", "sekee"),
        ("مثقال طلا", "mesghal"),
    ]
    items = ""
    for name, indicator in currencies:
        try:
            url = f"https://api.tgju.org/v1/market/indicator/summary-table-data/{indicator}"
            response = requests.get(url, timeout=10)
            data = response.json()
            records = data.get("data", [])
            if records:
                price = records[0][0]
                change_class = "up"
                if len(records) > 1:
                    try:
                        prev = float(records[1][0].replace(",", ""))
                        curr = float(price.replace(",", ""))
                        if curr < prev:
                            change_class = "down"
                    except:
                        pass
                items += f'<div class="currency-item" data-name="{name}"><span>{name}</span><span class="currency-value {change_class}">{price}</span></div>'
        except:
            pass
    return items if items else '<div class="currency-item">در دسترس نیست</div>'

def get_football_foreign():
    matches = []
    try:
        url = "https://api.football-data.org/v4/matches?season=2026"
        headers = {"X-Auth-Token": "efd72515902e44019da93c99e04f7dbb"}
        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()
        for match in data.get("matches", []):
            league_code = match.get("competition", {}).get("code", "")
            if league_code not in valid_leagues:
                continue
            home = translate_team(match["homeTeam"]["name"])
            away = translate_team(match["awayTeam"]["name"])
            status = match["status"]
            matchday = match.get("matchday", "")
            utc_date = match.get("utcDate", "")
            match_time = datetime.now()
            if utc_date:
                try:
                    match_time = datetime.strptime(utc_date[:19], "%Y-%m-%dT%H:%M:%S")
                except:
                    pass
            if status == "FINISHED":
                score = f"{match['score']['fullTime']['home']} - {match['score']['fullTime']['away']}"
                status_text = "پایان یافته"
                status_class = "finished"
            elif status == "IN_PLAY":
                score = f"{match['score']['fullTime']['home']} - {match['score']['fullTime']['away']}"
                status_text = "در حال برگزاری"
                status_class = "live"
            else:
                score = "-"
                status_text = "برگزار نشده"
                status_class = "upcoming"
            matches.append({
                "home": home,
                "away": away,
                "score": score,
                "status_text": status_text,
                "status_class": status_class,
                "matchday": f"هفته {matchday}" if matchday else "",
                "time": match_time
            })
    except:
        pass
    return matches

def get_football_iran():
    matches = []
    seen = set()
    for id_team, name in team_ids.items():
        try:
            url = f"https://www.thesportsdb.com/api/v1/json/3/eventslast.php?id={id_team}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                events = data.get("results", [])
                for event in events:
                    home = event.get("strHomeTeam", "")
                    away = event.get("strAwayTeam", "")
                    home_score = event.get("intHomeScore", "0")
                    away_score = event.get("intAwayScore", "0")
                    home_fa = translate_team(home)
                    away_fa = translate_team(away)
                    for eng, fa in iran_teams.items():
                        if eng.lower() in home.lower():
                            home_fa = fa
                        if eng.lower() in away.lower():
                            away_fa = fa
                    match_key = f"{home_fa}-{away_fa}-{home_score}-{away_score}"
                    if match_key in seen:
                        continue
                    seen.add(match_key)
                    matches.append({
                        "home": home_fa,
                        "away": away_fa,
                        "score": f"{home_score} - {away_score}",
                        "status_text": "پایان یافته",
                        "status_class": "finished",
                        "matchday": "لیگ برتر ایران",
                        "time": datetime.now()
                    })
        except:
            pass
    return matches

news_html = get_news()
weather_html = get_weather()
currency_html = get_currency()
foreign_matches = get_football_foreign()
iran_matches = get_football_iran()
all_matches = iran_matches + foreign_matches

finished = [m for m in all_matches if m["status_class"] == "finished"]
live = [m for m in all_matches if m["status_class"] == "live"]
upcoming = [m for m in all_matches if m["status_class"] == "upcoming"]
finished.sort(key=lambda x: x["time"], reverse=True)
all_matches = finished + live + upcoming

matches_html = ""
for m in all_matches[:20]:
    matchday_text = f" | {m['matchday']}" if m['matchday'] else ""
    tv_icon = ' <span onclick="window.open(\'https://telewebion.com/\', \'_blank\')" style="cursor:pointer;">📺</span>' if m['status_class'] == 'live' else ''
    matches_html += f'''<div class="match-item" data-status="{m['status_class']}">
        <div class="match-row">
            <span class="team-name right">{m['home']}</span>
            <span class="match-score">{m['score']}</span>
            <span class="team-name left">{m['away']}{tv_icon}</span>
        </div>
        <div class="match-status">{m['status_text']}{matchday_text}</div>
    </div>'''

if not matches_html:
    matches_html = '<div class="match-item">خطا در بارگذاری فوتبال</div>'

provinces_options = ""
for province in provinces.keys():
    provinces_options += f'<option value="{province}">{province}</option>'

province_data = str({name: list(coords) for name, coords in provinces.items()})

html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AmirHarter</title>
    <style>
        :root {{
            --bg: #0f0c29;
            --card: rgba(255,255,255,0.1);
            --border: rgba(255,255,255,0.2);
            --text: #fff;
            --muted: #ccc;
            --accent: #f093fb;
        }}
        .light-mode {{
            --bg: linear-gradient(135deg, #e8f4fd, #d4e9ff, #c2dfff);
            --card: rgba(255,255,255,0.85);
            --border: #b8d4f0;
            --text: #1a2a4a;
            --muted: #5a6c8a;
            --accent: #e85d75;
        }}
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            background: var(--bg);
            color: var(--text);
            font-family: Tahoma;
            transition: 0.5s;
            min-height: 100vh;
            user-select: none;
            -webkit-user-select: none;
            -webkit-touch-callout: none;
            -webkit-tap-highlight-color: transparent;
            position: relative;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 20px;
            background: linear-gradient(135deg, #f093fb, #4facfe);
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 100;
        }}
        .light-mode .header {{
            background: linear-gradient(135deg, #f5576c, #4facfe);
        }}
        .logo {{
            font-size: 1.5rem;
            font-weight: bold;
            color: #fff;
        }}
        .settings-btn {{
            font-size: 1.5rem;
            background: none;
            border: none;
            cursor: pointer;
            color: #fff;
        }}
        .settings-overlay {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.5);
            z-index: 200;
        }}
        .settings-panel {{
            position: fixed;
            top: 0;
            right: -300px;
            width: 280px;
            height: 100%;
            background: var(--bg);
            border-left: 1px solid var(--border);
            transition: right 0.3s;
            z-index: 201;
            padding: 20px;
            overflow-y: auto;
        }}
        .settings-panel.open {{
            right: 0;
        }}
        .settings-title {{
            font-size: 1.3rem;
            font-weight: bold;
            margin-bottom: 20px;
        }}
        .settings-item {{
            padding: 12px;
            margin: 8px 0;
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 10px;
            cursor: pointer;
            text-align: right;
        }}
        .settings-item:hover {{
            background: rgba(255,255,255,0.15);
        }}
        .modal-overlay {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.7);
            z-index: 300;
            justify-content: center;
            align-items: center;
        }}
        .modal {{
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: 15px;
            padding: 20px;
            width: 90%;
            max-width: 400px;
            max-height: 80vh;
            overflow-y: auto;
        }}
        .modal-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        .modal-close {{
            background: none;
            border: none;
            color: var(--text);
            font-size: 1.5rem;
            cursor: pointer;
        }}
        .main {{
            max-width: 600px;
            margin: 70px auto 0;
            padding: 15px;
        }}
        .theme-float {
    position: absolute;
    top: 60px;
    right: 10px;
    font-size: 1.3rem;
        }}
        .logo-animation {{
            text-align: center;
            padding: 40px 20px;
            animation: floatLogo 3s ease-in-out infinite;
        }}
        @keyframes floatLogo {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-15px); }}
        }}
        .logo-text {{
            font-size: 3rem;
            font-weight: 900;
            background: linear-gradient(45deg, #f093fb, #ffd700, #4facfe, #f093fb);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradientShift 3s ease infinite;
        }}
        @keyframes gradientShift {{
            0%, 100% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
        }}
        .search-container {{
            position: relative;
            margin: 15px 0;
        }}
        .search-box {{
            width: 100%;
            padding: 14px 120px 14px 50px;
            border-radius: 30px;
            border: 2px solid var(--border);
            background: var(--card);
            color: var(--text);
            font-size: 1.05rem;
            outline: none;
            text-align: center;
        }}
        .search-btn {{
            position: absolute;
            right: 8px;
            top: 50%;
            transform: translateY(-50%);
            padding: 10px 20px;
            border: none;
            border-radius: 25px;
            background: linear-gradient(45deg, #f093fb, #f5576c);
            color: #fff;
            cursor: pointer;
            font-weight: bold;
        }}
        .mic-btn {{
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            cursor: pointer;
            font-size: 1.3rem;
        }}
        .search-options {{
            display: flex;
            gap: 10px;
            justify-content: center;
            margin: 20px 0;
        }}
        .search-option {{
            flex: 1;
            padding: 12px;
            border: 1px solid var(--border);
            border-radius: 25px;
            background: var(--card);
            color: var(--text);
            cursor: pointer;
            font-size: 0.85rem;
            text-align: center;
            text-decoration: none;
        }}
        .clock-section {{
            text-align: center;
            padding: 30px 15px;
            margin: 15px 0;
            background: linear-gradient(135deg, rgba(240,147,251,0.3), rgba(79,172,254,0.3));
            border: 1px solid var(--border);
            border-radius: 25px;
        }}
        .clock-icon {{
            font-size: 3rem;
        }}
        .clock {{
            font-size: 2.5rem;
            font-weight: 900;
            background: linear-gradient(45deg, #ffd700, #ffaa00, #ffd700);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .light-mode .clock {{
            background: linear-gradient(45deg, #1a2a4a, #4facfe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .date {{
            color: var(--muted);
            font-size: 0.9rem;
        }}
        .card {{
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 15px;
            padding: 18px;
            margin: 15px 0;
            backdrop-filter: blur(10px);
        }}
        .card-title {{
            font-size: 1.15rem;
            margin-bottom: 10px;
        }}
        .news-scroll, .football-scroll, .currency-scroll {{
            max-height: 180px;
            overflow-y: auto;
        }}
        .news-item {{
            padding: 8px;
            border-bottom: 1px solid var(--border);
            cursor: pointer;
            font-size: 0.85rem;
        }}
        .news-item:hover {{
            color: var(--accent);
        }}
        .currency-search {{
            width: 100%;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: var(--card);
            color: var(--text);
            font-size: 0.85rem;
            margin-bottom: 10px;
        }}
        .currency-item {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid var(--border);
        }}
        .currency-value {{
            font-weight: bold;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.85rem;
        }}
        .currency-value.up {{
            background: #28a745;
            color: #fff;
        }}
        .currency-value.down {{
            background: #dc3545;
            color: #fff;
        }}
        .currency-icon {{
            display: inline-block;
            font-size: 1.8rem;
            animation: pulseCurrency 2s infinite;
            text-shadow: 0 2px 4px rgba(255,255,255,0.7);
        }}
        @keyframes pulseCurrency {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.1); }}
        }}
        .weather-card {{
            text-align: center;
        }}
        .weather-icon {{
            font-size: 3rem;
        }}
        .weather-temp {{
            font-size: 2rem;
            font-weight: 900;
            color: var(--accent);
        }}
        .weather-desc {{
            margin-top: 10px;
            color: var(--muted);
        }}
        .province-select {{
            width: 100%;
            padding: 8px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: var(--card);
            color: var(--text);
            font-size: 0.8rem;
            margin-top: 10px;
        }}
        .filter-btns {{
            display: flex;
            gap: 8px;
            margin-bottom: 15px;
        }}
        .filter-btn {{
            flex: 1;
            padding: 8px;
            border: none;
            border-radius: 20px;
            background: linear-gradient(45deg, #f093fb, #f5576c);
            color: #fff;
            cursor: pointer;
            font-size: 0.75rem;
            font-weight: bold;
        }}
        .filter-btn.active {{
            background: linear-gradient(45deg, #4facfe, #00f2fe);
        }}
        .match-item {{
            padding: 10px;
            border-bottom: 1px solid var(--border);
        }}
        .match-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 5px;
            margin-bottom: 5px;
        }}
        .team-name {{
            flex: 1;
            font-size: 0.85rem;
        }}
        .team-name.right {{
            text-align: right;
        }}
        .team-name.left {{
            text-align: left;
        }}
        .match-score {{
            color: var(--accent);
            font-weight: bold;
        }}
        .match-status {{
            text-align: center;
            font-size: 0.75rem;
            color: var(--muted);
        }}
        .lang-row {{
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }}
        .lang-box {{
            flex: 1;
        }}
        .lang-search {{
            width: 100%;
            padding: 8px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: var(--card);
            color: var(--text);
            font-size: 0.75rem;
        }}
        .lang-search-btn {{
            width: 100%;
            padding: 10px;
            border: none;
            border-radius: 25px;
            background: linear-gradient(45deg, #f093fb, #f5576c);
            color: #fff;
            cursor: pointer;
            font-size: 1.2rem;
            margin-top: 6px;
        }}
        .lang-select {{
            width: 100%;
            padding: 8px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: var(--card);
            color: var(--text);
            font-size: 0.8rem;
            margin-top: 5px;
        }}
        .swap-btn {{
            width: 40px;
            height: 40px;
            border: none;
            border-radius: 50%;
            background: linear-gradient(45deg, #f093fb, #f5576c);
            color: #fff;
            cursor: pointer;
            font-size: 1.3rem;
            align-self: center;
        }}
        textarea {{
            width: 100%;
            padding: 12px;
            border-radius: 10px;
            border: 1px solid var(--border);
            background: var(--card);
            color: var(--text);
            min-height: 100px;
        }}
        .btn-row {{
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }}
        .btn-row button {{
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
        }}
        .translate-btn {{
            background: var(--accent);
            color: #fff;
        }}
        .copy-btn {{
            background: #4facfe;
            color: #fff;
        }}
        .result {{
            background: var(--card);
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: var(--muted);
            font-size: 0.8rem;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">AmirHarter</div>
        <button class="settings-btn" onclick="toggleSettings()">⚙️</button>
    </div>

    <button class="theme-float" onclick="toggleTheme()" id="themeFloat">☀️</button>

    <div class="settings-overlay" id="settingsOverlay" onclick="toggleSettings()"></div>
    <div class="settings-panel" id="settingsPanel">
        <div class="settings-title">⚙️ تنظیمات</div>
        <div class="settings-item" onclick="toggleTheme()">🌙 تغییر تم</div>
        <div class="settings-item" onclick="showFontModal()">🔤 فونت: <span id="fontLabel">متوسط</span></div>
        <div class="settings-item" onclick="shareSite()">📤 اشتراک‌گذاری سایت</div>
        <div class="settings-item" onclick="showReportModal()">⚠️ گزارش مشکل</div>
        <div class="settings-item" onclick="showAboutModal()">📖 درباره ما</div>
        <div class="settings-item">📌 نسخه: v36</div>
    </div>

    <div class="modal-overlay" id="aboutModal">
        <div class="modal">
            <div class="modal-header">
                <span>📖 درباره ما</span>
                <button class="modal-close" onclick="closeModal('aboutModal')">›</button>
            </div>
            <p>AmirHarter | پورتال هوشمند</p>
            <br>
            <p>AMIRHARTER ... فقط یک سایت نیست</p>
            <p>یه دنیای کامله!</p>
            <br>
            <p>جایی که همه‌چیز یکجا جمع شده</p>
            <p>از آخرین اخبار و قیمت ارز</p>
            <p>تا آب و هوا، فوتبال و ترجمه!</p>
            <br>
            <p>ساخته شده برای اینکه دنیایی از اطلاعات دم دستت باشه</p>
            <br>
            <p>✨ قدرت در عین سادگی ✨</p>
            <p>نسخه ۴.۰</p>
        </div>
    </div>

    <div class="modal-overlay" id="reportModal">
        <div class="modal">
            <div class="modal-header">
                <span>⚠️ گزارش مشکل</span>
                <button class="modal-close" onclick="closeModal('reportModal')">›</button>
            </div>
            <p>در روبیکا پیام دهید:</p>
            <br>
            <p style="cursor:pointer; background: var(--card); padding: 10px; border-radius: 8px;" onclick="copyID()">@ID_HARTER</p>
        </div>
    </div>

    <div class="modal-overlay" id="fontModal">
        <div class="modal">
            <div class="modal-header">
                <span>🔤 انتخاب فونت</span>
                <button class="modal-close" onclick="closeModal('fontModal')">›</button>
            </div>
            <div class="settings-item" onclick="setFontSize('0.9rem', 'کوچیک')">کوچیک</div>
            <div class="settings-item" onclick="setFontSize('1rem', 'متوسط')">متوسط</div>
            <div class="settings-item" onclick="setFontSize('1.2rem', 'بزرگ')">بزرگ</div>
        </div>
    </div>

    <div class="main">
        <div class="logo-animation">
            <div class="logo-text">AmirHarter</div>
        </div>

        <div class="search-container">
            <button class="search-btn" onclick="searchGoogle(document.getElementById('mainSearch').value)">جستجو</button>
            <button class="mic-btn" onclick="voiceSearch()">🎤</button>
            <input class="search-box" id="mainSearch" placeholder="در AMIR HARTER" onkeypress="if(event.key==='Enter') searchGoogle(this.value)">
        </div>

        <div class="search-options">
            <a href="https://play.google.com/" target="_blank" class="search-option">📱 گوگل‌پلی</a>
            <a href="https://telewebion.com/" target="_blank" class="search-option">📺 تلوبیون</a>
            <a href="games.html" class="search-option">🎮 بازی‌ها</a>
        </div>

        <div class="clock-section">
            <div class="clock-icon">🕐</div>
            <div class="clock" id="clock">--:--:--</div>
            <div class="date" id="date">---</div>
        </div>

        <div class="card">
            <div class="card-title">🌤 آب و هوا</div>
            <div class="weather-card" id="weatherData">{weather_html}</div>
            <select class="province-select" onchange="changeProvince(this.value)">
                <option value="">انتخاب استان...</option>
                {provinces_options}
            </select>
        </div>

        <div class="card">
            <div class="card-title"><span class="currency-icon">💱</span> قیمت ارز</div>
            <input class="currency-search" placeholder="🔍 جستجوی ارز..." onkeyup="filterCurrency(this.value)">
            <div class="currency-scroll" id="currencyList">
                {currency_html}
            </div>
        </div>

        <div class="card">
            <div class="card-title">⚽ بازی‌های داغ</div>
            <div class="filter-btns">
                <button class="filter-btn active" onclick="filterMatches('all', this)">همه</button>
                <button class="filter-btn" onclick="filterMatches('finished', this)">پایان یافته</button>
                <button class="filter-btn" onclick="filterMatches('live', this)">در حال انجام</button>
                <button class="filter-btn" onclick="filterMatches('upcoming', this)">برگزار نشده</button>
            </div>
            <div class="football-scroll">{matches_html}</div>
        </div>

        <div class="card">
            <div class="card-title">📰 آخرین اخبار</div>
            <div class="news-scroll">{news_html}</div>
        </div>

        <div class="card">
            <div class="card-title">🌐 ترجمه</div>
            <div class="lang-row">
                <div class="lang-box">
                    <input class="lang-search" id="fromSearch" placeholder="🔍 تغییر زبان مبدا...">
                    <button class="lang-search-btn" onclick="searchFrom()">🔍</button>
                    <select class="lang-select" id="from"></select>
                </div>
                <button class="swap-btn" onclick="swapLanguages()">⇄</button>
                <div class="lang-box">
                    <input class="lang-search" id="toSearch" placeholder="🔍 تغییر زبان مقصد...">
                    <button class="lang-search-btn" onclick="searchTo()">🔍</button>
                    <select class="lang-select" id="to"></select>
                </div>
            </div>
            <textarea id="text" placeholder="متن خود را وارد کنید..."></textarea>
            <div class="result" id="result">نتیجه ترجمه...</div>
            <div class="btn-row">
                <button class="translate-btn" onclick="translateText()">ترجمه</button>
                <button class="copy-btn" onclick="copyResult()">کپی</button>
            </div>
        </div>

        <div class="footer">© 2026 AmirHarter - تمامی حقوق محفوظ است</div>
    </div>

    <script>
        const languages = {{"fa":"فارسی","en":"انگلیسی","ar":"عربی","fr":"فرانسوی","de":"آلمانی","es":"اسپانیایی","it":"ایتالیایی","pt":"پرتغالی","ru":"روسی","tr":"ترکی","zh":"چینی","ja":"ژاپنی","ko":"کره‌ای","hi":"هندی","ur":"اردو","nl":"هلندی","pl":"لهستانی","sv":"سوئدی","no":"نروژی","da":"دانمارکی","fi":"فنلاندی","el":"یونانی","he":"عبری","th":"تایلندی","vi":"ویتنامی","id":"اندونزیایی","ms":"مالایی","cs":"چکی","sk":"اسلواکی","hu":"مجاری","ro":"رومانیایی","bg":"بلغاری","uk":"اوکراینی","sr":"صربی","hr":"کرواتی","sl":"اسلوونیایی","lt":"لیتوانیایی","lv":"لتونیایی","et":"استونیایی","sq":"آلبانیایی","mk":"مقدونی","hy":"ارمنی","ka":"گرجی","az":"آذربایجانی","kk":"قزاقی","uz":"ازبکی","ky":"قرقیزی","tg":"تاجیکی","mn":"مغولی","bn":"بنگالی","ta":"تامیلی","te":"تلوگو","mr":"مراتی","gu":"گجراتی","kn":"کانادا","ml":"مالایایی","si":"سینهالی","ne":"نپالی","km":"خمری","lo":"لائوسی","my":"برمه‌ای","fil":"فیلیپینی","sw":"سواحیلی","am":"آمهری","ha":"هوسا","yo":"یوروبایی","zu":"زولویی","af":"آفریکانس","ig":"ایگبو"}};

        function populateLanguages() {{
            const from = document.getElementById('from');
            const to = document.getElementById('to');
            for (const code in languages) {{
                from.innerHTML += `<option value="${{code}}">${{languages[code]}}</option>`;
                to.innerHTML += `<option value="${{code}}">${{languages[code]}}</option>`;
            }}
            from.value = 'fa';
            to.value = 'en';
        }}
        populateLanguages();

        const provinces = {province_data};

        function toggleSettings() {{
            document.getElementById('settingsPanel').classList.toggle('open');
            document.getElementById('settingsOverlay').style.display =
                document.getElementById('settingsPanel').classList.contains('open') ? 'block' : 'none';
        }}

        function showAboutModal() {{
            toggleSettings();
            document.getElementById('aboutModal').style.display = 'flex';
        }}

        function showReportModal() {{
            toggleSettings();
            document.getElementById('reportModal').style.display = 'flex';
        }}

        function showFontModal() {{
            toggleSettings();
            document.getElementById('fontModal').style.display = 'flex';
        }}

        function closeModal(id) {{
            document.getElementById(id).style.display = 'none';
        }}

        function copyID() {{
            const textarea = document.createElement('textarea');
            textarea.value = '@ID_HARTER';
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            alert('کپی شد!');
        }}

        function setFontSize(size, label) {{
            document.body.style.fontSize = size;
            document.getElementById('fontLabel').textContent = label;
            closeModal('fontModal');
        }}

        function shareSite() {{
            const url = window.location.href;
            if (navigator.share) {{
                navigator.share({{title: 'AmirHarter', url: url}});
            }} else {{
                prompt('لینک سایت:', url);
            }}
        }}

        function changeProvince(name) {{
            if (!name || !provinces[name]) return;
            const [lat, lon] = provinces[name];
            fetch(`https://api.open-meteo.com/v1/forecast?latitude=${{lat}}&longitude=${{lon}}&current_weather=true&timezone=Asia%2FTehran`)
                .then(r => r.json())
                .then(d => {{
                    const temp = d.current_weather.temperature;
                    const wind = d.current_weather.windspeed;
                    const code = d.current_weather.weathercode;
                    const descs = {{0:'آفتابی',1:'نیمه آفتابی',2:'نیمه ابری',3:'ابری',45:'مه',61:'باران',71:'برف'}};
                    const desc = descs[code] || 'نامشخص';
                    document.getElementById('weatherData').innerHTML = `<div class="weather-icon">🌤</div><div class="weather-temp">${{temp}}°C</div><div class="weather-desc">${{name}}<br>${{desc}}<br>باد: ${{wind}} km/h</div>`;
                }});
        }}

        function filterCurrency(query) {{
            document.querySelectorAll('.currency-item').forEach(item => {{
                const name = item.getAttribute('data-name') || '';
                item.style.display = name.includes(query) || query === '' ? 'flex' : 'none';
            }});
        }}

        function updateClock() {{
            const now = new Date();
            document.getElementById('clock').textContent = now.toLocaleTimeString('fa-IR');
            document.getElementById('date').textContent = now.toLocaleDateString('fa-IR', {{weekday:'long',year:'numeric',month:'long',day:'numeric'}});
        }}
        setInterval(updateClock, 1000);
        updateClock();

        function toggleTheme() {{
            document.body.classList.toggle('light-mode');
            const isLight = document.body.classList.contains('light-mode');
            document.getElementById('themeFloat').textContent = isLight ? '🌙' : '☀️';
        }}

        function searchGoogle(q) {{
            if (q) window.open('https://www.google.com/search?q=' + encodeURIComponent(q), '_blank');
        }}

        function voiceSearch() {{
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {{
                const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
                const recognition = new SR();
                recognition.lang = 'fa-IR';
                recognition.onresult = function(e) {{
                    document.getElementById('mainSearch').value = e.results[0][0].transcript;
                }};
                recognition.start();
            }} else {{
                alert('مرورگر شما از تایپ صوتی پشتیبانی نمی‌کند');
            }}
        }}

        function filterMatches(type, btn) {{
            document.querySelectorAll('.match-item').forEach(item => {{
                if (type === 'all') item.style.display = 'block';
                else item.style.display = item.dataset.status === type ? 'block' : 'none';
            }});
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        }}

        function swapLanguages() {{
            const from = document.getElementById('from');
            const to = document.getElementById('to');
            const temp = from.value;
            from.value = to.value;
            to.value = temp;
        }}

        function searchFrom() {{
            const q = document.getElementById('fromSearch').value.trim().toLowerCase();
            const select = document.getElementById('from');
            for (const code in languages) {{
                if (languages[code].toLowerCase().includes(q)) {{
                    select.value = code;
                    document.getElementById('fromSearch').value = '';
                    break;
                }}
            }}
        }}

        function searchTo() {{
            const q = document.getElementById('toSearch').value.trim().toLowerCase();
            const select = document.getElementById('to');
            for (const code in languages) {{
                if (languages[code].toLowerCase().includes(q)) {{
                    select.value = code;
                    document.getElementById('toSearch').value = '';
                    break;
                }}
            }}
        }}

        function translateText() {{
            const text = document.getElementById('text').value;
            const from = document.getElementById('from').value;
            const to = document.getElementById('to').value;
            if (!text) return;
            const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=${{from}}&tl=${{to}}&dt=t&q=${{encodeURIComponent(text)}}`;
            fetch(url)
                .then(r => r.json())
                .then(d => {{
                    let translated = '';
                    d[0].forEach(part => translated += part[0]);
                    document.getElementById('result').textContent = translated;
                }})
                .catch(() => document.getElementById('result').textContent = 'خطا در ترجمه');
        }}

        function copyResult() {{
            const result = document.getElementById('result').textContent;
            const textarea = document.createElement('textarea');
            textarea.value = result;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            alert('کپی شد!');
        }}
    </script>
</body>
</html>
"""

html = html.replace("{province_data}", province_data)

with open(OUTPUT_DIR / 'index.html', 'w', encoding='utf-8') as f:
    f.write(html)

game_files = ['games.html', 'tictactoe.html', 'snake.html', 'guess.html', 'rps.html']
for game_file in game_files:
    if Path(game_file).exists():
        shutil.copy(game_file, OUTPUT_DIR / game_file)

print("سایت با موفقیت ساخته شد!")

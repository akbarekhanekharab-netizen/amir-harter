import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
import shutil
import json

OUTPUT_DIR = Path('site')
OUTPUT_DIR.mkdir(exist_ok=True)

team_names = {
    "Arsenal": "آرسنال", "Chelsea": "چلسی", "Liverpool": "لیورپول",
    "Manchester City": "منچستر سیتی", "Manchester United": "منچستر یونایتد",
    "Real Madrid": "رئال مادرید", "Barcelona": "بارسلونا", "Inter": "اینتر",
    "AC Milan": "میلان", "Juventus": "یوونتوس", "Napoli": "ناپولی",
    "Roma": "رم", "Lazio": "لاتزیو", "Atalanta": "آتالانتا",
    "Bayern Munich": "بایرن مونیخ", "Dortmund": "دورتموند", "Leipzig": "لایپزیگ",
    "Leverkusen": "لورکوزن", "Frankfurt": "فرانکفورت", "Stuttgart": "اشتوتگارت",
    "PSG": "پاری سن ژرمن", "Marseille": "مارسی", "Lyon": "لیون",
    "Monaco": "موناکو", "Lille": "لیل", "Nice": "نیس", "Lens": "لانس",
    "Rennes": "رن", "Strasbourg": "استراسبورگ", "Nantes": "نانت",
    "Toulouse": "تولوز", "Montpellier": "مون‌پولیه", "Brest": "برست",
    "Angers": "آنژه", "Auxerre": "اوسر", "Troyes": "تروا",
    "Freiburg": "فرایبورگ", "Mainz": "ماینتس", "Augsburg": "آگسبورگ",
    "Fiorentina": "فیورنتینا", "Bologna": "بولونیا", "Parma": "پارما",
    "Monza": "مونتزا", "Venezia": "ونتزیا", "Tottenham": "تاتنهام",
    "Newcastle": "نیوکاسل", "Everton": "اورتون", "West Ham": "وست هم",
    "Fulham": "فولام", "Wolves": "ولورهمپتون", "Valencia": "والنسیا",
    "Sevilla": "سویا", "Villarreal": "ویارئال", "Atletico Madrid": "اتلتیکو مادرید",
    "Athletic Bilbao": "اتلتیک بیلبائو", "Getafe": "ختافه",
    "Crystal Palace": "کریستال پالاس", "Southampton": "ساوتهمپتون",
    "Brighton": "برایتون", "Brentford": "برنتفورد", "Aston Villa": "استون ویلا",
    "Leicester": "لسترسیتی", "Leeds": "لیدز یونایتد",
    "Nottingham Forest": "ناتینگهام فارست", "Bournemouth": "بورنموث",
    "Real Sociedad": "رئال سوسیداد", "Real Betis": "رئال بتیس",
    "Celta Vigo": "سلتاویگو", "Girona": "جیرونا", "Osasuna": "اوساسونا",
    "Mallorca": "مایورکا", "Rayo Vallecano": "رایو وایکانو",
    "Alaves": "آلاوس", "Las Palmas": "لاس پالماس", "Leganes": "لگانس",
    "Espanyol": "اسپانیول", "Valladolid": "رئال وایادولید",
    "Udinese": "اودینزه", "Torino": "تورینو", "Genoa": "جنوا",
    "Cagliari": "کالیاری", "Empoli": "امپولی", "Lecce": "لچه",
    "Verona": "هلاس ورونا", "Como": "کومو", "Hoffenheim": "هوفنهایم",
    "Werder Bremen": "وِردر برمن", "Heidenheim": "هایدنهایم",
    "St. Pauli": "سنت پائولی", "Union Berlin": "یونیون برلین",
    "Bochum": "بوخوم", "Koln": "کلن", "Holstein Kiel": "هولشتاین کیل",
    "Wolfsburg": "وولفسبورگ", "Reims": "رنس", "Le Havre": "لو آور",
    "Clermont": "کلرمون", "Lorient": "لوریان", "Metz": "متز",
    "Benfica": "بنفیکا", "Porto": "پورتو", "Sporting CP": "اسپورتینگ لیسبون",
    "Ajax": "آژاکس", "PSV": "آیندهوون", "Feyenoord": "فاینورد",
    "Celtic": "سلتیک", "Rangers": "رنجرز", "Galatasaray": "گالاتاسرای",
    "Fenerbahce": "فنرباغچه", "Olympiacos": "المپیاکوس",
    "Panathinaikos": "پاناتینایکوس", "AEK Athens": "آ.ا.ک آتن", "PAOK": "پائوک",
    "Persepolis": "پرسپولیس", "Esteghlal": "استقلال", "Sepahan": "سپاهان",
    "Tractor": "تراکتور", "Foolad": "فولاد", "Gol Gohar": "گل گهر",
    "Malavan": "ملوان", "Nassaji": "نساجی", "Zob Ahan": "ذوب آهن",
    "Aluminium Arak": "آلومینیوم", "Shams Azar": "شمس آذر", "Kheybar": "خیبر",
    "Sanat Naft": "صنعت نفت", "Fajr Sepasi": "فجر سپاسی",
    "Chadormalou": "چادرملو", "Havadar": "هوادار", "Paykan": "پیکان",
    "Mes Shahr-e Babak": "مس شهر بابک", "Esteghlal Khuzestan": "استقلال خوزستان"
}

provinces_en = {
    "Tehran": "تهران", "Mashhad": "مشهد", "Isfahan": "اصفهان",
    "Shiraz": "شیراز", "Tabriz": "تبریز", "Ahvaz": "اهواز",
    "Qom": "قم", "Karaj": "کرج", "Kermanshah": "کرمانشاه",
    "Rasht": "رشت", "Zahedan": "زاهدان", "Hamedan": "همدان",
    "Urmia": "ارومیه", "Yazd": "یزد", "Ardabil": "اردبیل",
    "Bandar Abbas": "بندرعباس", "Arak": "اراک", "Zanjan": "زنجان",
    "Sanandaj": "سنندج", "Qazvin": "قزوین", "Khorramabad": "خرم‌آباد",
    "Gorgan": "گرگان", "Sari": "ساری", "Bushehr": "بوشهر",
    "Birjand": "بیرجند", "Ilam": "ایلام", "Shahr-e Kord": "شهرکرد",
    "Yasuj": "یاسوج", "Bojnurd": "بجنورد", "Semnan": "سمنان"
}

provinces = {
    "تهران": (35.6892, 51.3890), "مشهد": (36.2605, 59.6168),
    "اصفهان": (32.6546, 51.6680), "شیراز": (29.5918, 52.5837),
    "تبریز": (38.0962, 46.2738), "اهواز": (31.3183, 48.6706),
    "قم": (34.6416, 50.8746), "کرج": (35.8400, 50.9391),
    "کرمانشاه": (34.3142, 47.0650), "رشت": (37.2808, 49.5832),
    "زاهدان": (29.4963, 60.8629), "همدان": (34.7983, 48.5148),
    "ارومیه": (37.5527, 45.0760), "یزد": (31.8974, 54.3569),
    "اردبیل": (38.2498, 48.2933), "بندرعباس": (27.1832, 56.2666),
    "اراک": (34.0949, 49.7016), "زنجان": (36.6830, 48.5087),
    "سنندج": (35.3219, 46.9862), "قزوین": (36.2860, 50.0040),
    "خرم‌آباد": (33.4871, 48.3558), "گرگان": (36.8386, 54.4346),
    "ساری": (36.5633, 53.0601), "بوشهر": (28.9234, 50.8203),
    "بیرجند": (32.8649, 59.2212), "ایلام": (33.6375, 46.4227),
    "شهرکرد": (32.3256, 50.8644), "یاسوج": (30.6684, 51.5875),
    "بجنورد": (37.4749, 57.3290), "سمنان": (35.5729, 53.3971)
}

currency_names_en = {
    "دلار": "Dollar", "یورو": "Euro", "درهم": "Dirham",
    "پوند": "Pound", "لیر ترکیه": "Turkish Lira", "یوان چین": "Chinese Yuan",
    "روبل روسیه": "Russian Ruble", "دینار عراق": "Iraqi Dinar", "افغانی": "Afghani"
}

gold_names_en = {
    "طلای 18 عیار": "18K Gold", "طلای 24 عیار": "24K Gold",
    "سکه امامی": "Emami Coin", "نیم سکه": "Half Coin",
    "ربع سکه": "Quarter Coin", "سکه گرمی": "Gram Coin",
    "مثقال طلا": "Gold Mithqal"
}

def translate_team(name, to_english=False):
    if not name:
        return "نامشخص" if not to_english else "Unknown"
    
    if to_english:
        for eng, fa in team_names.items():
            if fa == name:
                return eng
        return name
    
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
        ("دلار", "price_dollar_rl"), ("یورو", "price_eur"),
        ("درهم", "price_aed"), ("پوند", "price_gbp"),
        ("لیر ترکیه", "price_try"), ("یوان چین", "price_cny"),
        ("روبل روسیه", "price_rub"), ("دینار عراق", "price_iqd"),
        ("افغانی", "price_afn"),
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

def get_gold():
    gold_items = [
        ("طلای 18 عیار", "23,062,200"), ("طلای 24 عیار", "30,749,300"),
        ("سکه امامی", "230,005,000"), ("نیم سکه", "116,500,000"),
        ("ربع سکه", "61,500,000"), ("سکه گرمی", "34,000,000"),
        ("مثقال طلا", "99,897,000"),
    ]
    items = ""
    for name, price in gold_items:
        items += f'<div class="currency-item" data-name="{name}"><span>{name}</span><span class="currency-value up">{price}</span></div>'
    return items

def get_football(to_english=False):
    matches = []
    seen = set()
    valid_competitions = [
        "ENGLAND: Premier League", "SPAIN: La Liga", "ITALY: Serie A",
        "GERMANY: Bundesliga", "FRANCE: Ligue 1", "Champions League",
        "Iran", "Persian Gulf"
    ]
    try:
        url = "https://www.scorebat.com/video-api/v3/"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            for match in data.get("response", []):
                home = match.get("homeTeam", {}).get("name", "")
                away = match.get("awayTeam", {}).get("name", "")
                competition = match.get("competition", "")
                date = match.get("date", "")
                
                is_valid = False
                for valid in valid_competitions:
                    if valid.lower() in competition.lower():
                        is_valid = True
                        break
                if not is_valid:
                    continue
                
                if to_english:
                    home_fa = home
                    away_fa = away
                else:
                    home_fa = translate_team(home)
                    away_fa = translate_team(away)
                
                if to_english:
                    competition_fa = competition
                else:
                    competition_fa = competition
                    if "Premier League" in competition:
                        competition_fa = "لیگ برتر انگلیس"
                    elif "La Liga" in competition:
                        competition_fa = "لا لیگا"
                    elif "Serie A" in competition:
                        competition_fa = "سری آ"
                    elif "Bundesliga" in competition:
                        competition_fa = "بوندسلیگا"
                    elif "Ligue 1" in competition:
                        competition_fa = "لوشامپیونه"
                    elif "Champions League" in competition:
                        competition_fa = "چمپیونز لیگ"
                    elif "Iran" in competition or "Persian Gulf" in competition:
                        competition_fa = "لیگ برتر ایران"
                
                match_time = datetime.now()
                try:
                    match_time = datetime.strptime(date[:19], "%Y-%m-%dT%H:%M:%S")
                except:
                    pass
                
                key = f"{home_fa}-{away_fa}-{competition_fa}"
                if key not in seen:
                    seen.add(key)
                    matches.append({
                        "home": home_fa, "away": away_fa, "score": "-",
                        "status_text": "Upcoming" if to_english else "پیش‌رو",
                        "status_class": "upcoming",
                        "matchday": competition_fa, "time": match_time
                    })
    except:
        pass
    matches.sort(key=lambda x: x["time"], reverse=True)
    return matches[:20]

# ============ ساخت سایت ============
print("🔍 در حال دریافت اطلاعات...")
news_html_fa = get_news()
weather_html_fa = get_weather()
currency_html_fa = get_currency()
gold_html_fa = get_gold()

print("⚽ در حال دریافت فوتبال...")
all_matches_fa = get_football(False)
all_matches_en = get_football(True)

matches_fa_html = ""
for m in all_matches_fa[:20]:
    matchday_text = f" | {m['matchday']}" if m['matchday'] else ""
    matches_fa_html += f'<div class="match-item" data-status="{m["status_class"]}"><div class="match-row"><span class="team-name right">{m["home"]}</span><span class="match-score">{m["score"]}</span><span class="team-name left">{m["away"]}</span></div><div class="match-status">{m["status_text"]}{matchday_text}</div></div>'

matches_en_html = ""
for m in all_matches_en[:20]:
    matchday_text = f" | {m['matchday']}" if m['matchday'] else ""
    matches_en_html += f'<div class="match-item" data-status="{m["status_class"]}"><div class="match-row"><span class="team-name right">{m["home"]}</span><span class="match-score">{m["score"]}</span><span class="team-name left">{m["away"]}</span></div><div class="match-status">{m["status_text"]}{matchday_text}</div></div>'

if not matches_fa_html:
    matches_fa_html = '<div class="match-item">خطا در بارگذاری فوتبال</div>'
if not matches_en_html:
    matches_en_html = '<div class="match-item">Error loading football data</div>'

provinces_json = json.dumps(provinces, ensure_ascii=False)
provinces_en_json = json.dumps(provinces_en, ensure_ascii=False)
currency_names_en_json = json.dumps(currency_names_en, ensure_ascii=False)
gold_names_en_json = json.dumps(gold_names_en, ensure_ascii=False)

# خواندن قالب HTML از فایل جداگانه
html_template = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AmirHarter</title>
    <style>
        :root { --bg: #0f0c29; --card: rgba(255,255,255,0.1); --border: rgba(255,255,255,0.2); --text: #fff; --muted: #ccc; --accent: #f093fb; }
        .light-mode { --bg: linear-gradient(135deg, #e8f4fd, #d4e9ff, #c2dfff); --card: rgba(255,255,255,0.85); --border: #b8d4f0; --text: #1a2a4a; --muted: #5a6c8a; --accent: #e85d75; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: var(--bg); color: var(--text); font-family: Tahoma; transition: 0.5s; min-height: 100vh; user-select: none; -webkit-user-select: none; -webkit-touch-callout: none; -webkit-tap-highlight-color: transparent; position: relative; }
        .header { display: flex; justify-content: space-between; align-items: center; padding: 15px 20px; background: linear-gradient(135deg, #f093fb, #4facfe); position: fixed; top: 0; left: 0; right: 0; z-index: 100; }
        .light-mode .header { background: linear-gradient(135deg, #f5576c, #4facfe); }
        .logo { font-size: 1.5rem; font-weight: bold; color: #fff; }
        .settings-btn { font-size: 1.5rem; background: none; border: none; cursor: pointer; color: #fff; }
        .settings-overlay { display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); z-index: 200; }
        .settings-panel { position: fixed; top: 0; right: -300px; width: 280px; height: 100%; background: var(--bg); border-left: 1px solid var(--border); transition: right 0.3s; z-index: 201; padding: 20px; overflow-y: auto; }
        .settings-panel.open { right: 0; }
        .settings-title { font-size: 1.3rem; font-weight: bold; margin-bottom: 20px; }
        .settings-item { padding: 12px; margin: 8px 0; background: var(--card); border: 1px solid var(--border); border-radius: 10px; cursor: pointer; text-align: right; }
        .settings-item:hover { background: rgba(255,255,255,0.15); }
        .modal-overlay { display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); z-index: 300; justify-content: center; align-items: center; }
        .modal { background: var(--bg); border: 1px solid var(--border); border-radius: 15px; padding: 20px; width: 90%; max-width: 400px; max-height: 80vh; overflow-y: auto; }
        .modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
        .modal-close { background: none; border: none; color: var(--text); font-size: 1.5rem; cursor: pointer; }
        .main { max-width: 600px; margin: 70px auto 0; padding: 15px; }
        .theme-float { position: absolute; top: 2px; right: 10px; font-size: 1.3rem; z-index: 50; background: none; border: none; cursor: pointer; padding: 3px; }
        .logo-animation { text-align: center; padding: 40px 20px; animation: floatLogo 3s ease-in-out infinite; }
        @keyframes floatLogo { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-15px); } }
        .logo-text { font-size: 3rem; font-weight: 900; background: linear-gradient(45deg, #f093fb, #ffd700, #4facfe, #f093fb); background-size: 300% 300%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: gradientShift 3s ease infinite; }
        @keyframes gradientShift { 0%, 100% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } }
        .search-container { position: relative; margin: 15px 0; }
        .search-box { width: 100%; padding: 14px 120px 14px 50px; border-radius: 30px; border: 2px solid var(--border); background: var(--card); color: var(--text); font-size: 1.05rem; outline: none; text-align: center; }
        .search-btn { position: absolute; right: 8px; top: 50%; transform: translateY(-50%); padding: 10px 20px; border: none; border-radius: 25px; background: linear-gradient(45deg, #f093fb, #f5576c); color: #fff; cursor: pointer; font-weight: bold; }
        .mic-btn { position: absolute; left: 15px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer; font-size: 1.3rem; }
        .search-options { display: flex; gap: 10px; justify-content: center; margin: 20px 0; }
        .search-option { flex: 1; padding: 12px; border: 1px solid var(--border); border-radius: 25px; background: var(--card); color: var(--text); cursor: pointer; font-size: 0.85rem; text-align: center; text-decoration: none; }
        .clock-section { text-align: center; padding: 30px 15px; margin: 15px 0; background: linear-gradient(135deg, rgba(240,147,251,0.3), rgba(79,172,254,0.3)); border: 1px solid var(--border); border-radius: 25px; }
        .clock-icon { font-size: 3rem; }
        .clock { font-size: 2.5rem; font-weight: 900; background: linear-gradient(45deg, #ffd700, #ffaa00, #ffd700); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .light-mode .clock { background: linear-gradient(45deg, #1a2a4a, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .date { color: var(--muted); font-size: 0.9rem; }
        .card { background: var(--card); border: 1px solid var(--border); border-radius: 15px; padding: 18px; margin: 15px 0; backdrop-filter: blur(10px); }
        .card-title { font-size: 1.15rem; margin-bottom: 10px; }
        .news-scroll, .football-scroll, .currency-scroll { max-height: 180px; overflow-y: auto; }
        .news-item { padding: 8px; border-bottom: 1px solid var(--border); cursor: pointer; font-size: 0.85rem; }
        .news-item:hover { color: var(--accent); }
        .currency-search { width: 100%; padding: 10px; border-radius: 8px; border: 1px solid var(--border); background: var(--card); color: var(--text); font-size: 0.85rem; margin-bottom: 10px; }
        .currency-item { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border); }
        .currency-value { font-weight: bold; padding: 4px 12px; border-radius: 15px; font-size: 0.85rem; }
        .currency-value.up { background: #28a745; color: #fff; }
        .currency-value.down { background: #dc3545; color: #fff; }
        .currency-icon { display: inline-block; font-size: 1.8rem; animation: pulseCurrency 2s infinite; text-shadow: 0 2px 4px rgba(255,255,255,0.7); }
        @keyframes pulseCurrency { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.1); } }
        .weather-card { text-align: center; }
        .weather-icon { font-size: 3rem; }
        .weather-temp { font-size: 2rem; font-weight: 900; color: var(--accent); }
        .weather-desc { margin-top: 10px; color: var(--muted); }
        .lang-display { width: 100%; padding: 8px; border-radius: 10px; border: 1px solid var(--border); background: var(--card); color: var(--text); cursor: pointer; text-align: center; font-size: 0.85rem; margin-top: 10px; min-height: 40px; display: flex; align-items: center; justify-content: center; }
        .province-item, .lang-item { padding: 12px; margin: 5px 0; background: var(--card); border: 1px solid var(--border); border-radius: 8px; cursor: pointer; text-align: center; font-size: 0.9rem; }
        .province-item:hover, .lang-item:hover { background: rgba(255,255,255,0.15); }
        .filter-btns { display: flex; gap: 8px; margin-bottom: 15px; }
        .filter-btn { flex: 1; padding: 8px; border: none; border-radius: 20px; background: linear-gradient(45deg, #f093fb, #f5576c); color: #fff; cursor: pointer; font-size: 0.75rem; font-weight: bold; }
        .filter-btn.active { background: linear-gradient(45deg, #4facfe, #00f2fe); }
        .match-item { padding: 10px; border-bottom: 1px solid var(--border); }
        .match-row { display: flex; justify-content: space-between; align-items: center; gap: 5px; margin-bottom: 5px; }
        .team-name { flex: 1; font-size: 0.85rem; }
        .team-name.right { text-align: right; }
        .team-name.left { text-align: left; }
        .match-score { color: var(--accent); font-weight: bold; }
        .match-status { text-align: center; font-size: 0.75rem; color: var(--muted); }
        .lang-row { display: flex; gap: 5px; margin-bottom: 15px; align-items: center; }
        .lang-box { flex: 1; min-width: 0; }
        .lang-box .lang-display { font-size: 0.75rem; padding: 6px; }
        .swap-btn { width: 35px; height: 35px; border: none; border-radius: 50%; background: linear-gradient(45deg, #f093fb, #f5576c); color: #fff; cursor: pointer; font-size: 1.2rem; flex-shrink: 0; transition: transform 0.5s ease; }
        .swap-btn.rotated { transform: rotate(180deg); }
        textarea { width: 100%; padding: 12px; border-radius: 10px; border: 1px solid var(--border); background: var(--card); color: var(--text); min-height: 100px; }
        .btn-row { display: flex; gap: 10px; margin-top: 10px; }
        .btn-row button { flex: 1; padding: 12px; border: none; border-radius: 10px; cursor: pointer; font-weight: bold; }
        .translate-btn { background: var(--accent); color: #fff; }
        .copy-btn { background: #4facfe; color: #fff; }
        .result { background: var(--card); padding: 15px; border-radius: 10px; margin: 10px 0; }
        .footer { text-align: center; padding: 20px; color: var(--muted); font-size: 0.8rem; }
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
        <div class="settings-title" id="settingsTitle">⚙️ تنظیمات</div>
        <div class="settings-item" onclick="toggleLanguage()">🌐 <span id="langLabel">زبان: فارسی</span></div>
        <div class="settings-item" onclick="toggleTheme()" id="themeText">🌙 تغییر تم</div>
        <div class="settings-item" onclick="showFontModal()">🔤 <span id="fontLabel">فونت: متوسط</span></div>
        <div class="settings-item" onclick="shareSite()" id="shareText">📤 اشتراک‌گذاری سایت</div>
        <div class="settings-item" onclick="showReportModal()" id="reportText">⚠️ گزارش مشکل</div>
        <div class="settings-item" onclick="showAboutModal()" id="aboutText">📖 درباره ما</div>
        <div class="settings-item">📌 <span id="versionText">نسخه: v42</span></div>
    </div>
    
    <div class="modal-overlay" id="aboutModal">
        <div class="modal">
            <div class="modal-header">
                <span id="aboutModalTitle">📖 درباره ما</span>
                <button class="modal-close" onclick="closeModal('aboutModal')">›</button>
            </div>
            <div id="aboutContentFa">
                <p>AmirHarter | پورتال هوشمند</p><br>
                <p>AMIRHARTER ... فقط یک سایت نیست</p>
                <p>یه دنیای کامله!</p><br>
                <p>جایی که همه‌چیز یکجا جمع شده</p>
                <p>از آخرین اخبار و قیمت ارز</p>
                <p>تا آب و هوا، فوتبال و ترجمه!</p><br>
                <p>ساخته شده برای اینکه دنیایی از اطلاعات دم دستت باشه</p><br>
                <p>✨ قدرت در عین سادگی ✨</p>
                <p>نسخه ۵.۰</p>
            </div>
            <div id="aboutContentEn" style="display:none;">
                <p>AmirHarter | Smart Portal</p><br>
                <p>AMIRHARTER ... is not just a website</p>
                <p>It's a whole world!</p><br>
                <p>Everything in one place</p>
                <p>From latest news and currency rates</p>
                <p>To weather, football and translation!</p><br>
                <p>Built to bring the world of information to your fingertips</p><br>
                <p>✨ Power in simplicity ✨</p>
                <p>Version 5.0</p>
            </div>
        </div>
    </div>
    
    <div class="modal-overlay" id="reportModal">
        <div class="modal">
            <div class="modal-header">
                <span id="reportModalTitle">⚠️ گزارش مشکل</span>
                <button class="modal-close" onclick="closeModal('reportModal')">›</button>
            </div>
            <p id="reportTextFa">در روبیکا پیام دهید:</p>
            <p id="reportTextEn" style="display:none;">Message us on Rubika:</p>
            <br>
            <p style="cursor:pointer; background: var(--card); padding: 10px; border-radius: 8px;" onclick="copyID()">@ID_HARTER</p>
        </div>
    </div>
    
    <div class="modal-overlay" id="fontModal">
        <div class="modal">
            <div class="modal-header">
                <span id="fontModalTitle">🔤 انتخاب فونت</span>
                <button class="modal-close" onclick="closeModal('fontModal')">›</button>
            </div>
            <div class="settings-item" onclick="setFontSize('0.9rem', 'کوچیک', 'Small')">کوچیک</div>
            <div class="settings-item" onclick="setFontSize('1rem', 'متوسط', 'Medium')">متوسط</div>
            <div class="settings-item" onclick="setFontSize('1.2rem', 'بزرگ', 'Large')">بزرگ</div>
        </div>
    </div>
    
    <div class="modal-overlay" id="langModal">
        <div class="modal">
            <div class="modal-header">
                <span id="langModalTitle">🌐 انتخاب زبان</span>
                <button class="modal-close" onclick="closeModal('langModal')">›</button>
            </div>
            <input class="currency-search" id="langSearchInput" placeholder="🔍 جستجوی زبان..." onkeyup="filterLanguages(this.value)">
            <div id="langList" style="max-height: 300px; overflow-y: auto;"></div>
        </div>
    </div>
    
    <div class="modal-overlay" id="provinceModal">
        <div class="modal">
            <div class="modal-header">
                <span id="provinceModalTitle">📍 انتخاب استان</span>
                <button class="modal-close" onclick="closeModal('provinceModal')">›</button>
            </div>
            <input class="currency-search" id="provinceSearchInput" placeholder="🔍 جستجوی استان..." onkeyup="filterProvinces(this.value)">
            <div id="provinceList" style="max-height: 300px; overflow-y: auto;"></div>
        </div>
    </div>
    
    <div class="main">
        <div class="logo-animation">
            <div class="logo-text">AmirHarter</div>
        </div>
        
        <div class="search-container">
            <button class="search-btn" id="searchBtn" onclick="searchGoogle(document.getElementById('mainSearch').value)">جستجو</button>
            <button class="mic-btn" onclick="voiceSearch()">🎤</button>
            <input class="search-box" id="mainSearch" placeholder="در AMIR HARTER" onkeypress="if(event.key==='Enter') searchGoogle(this.value)">
        </div>
        
        <div class="search-options">
            <a href="https://play.google.com/" target="_blank" class="search-option" id="option1">📱 گوگل‌پلی</a>
            <a href="https://telewebion.net/" target="_blank" class="search-option" id="option2">📺 تلوبیون</a>
            <a href="games.html" class="search-option" id="option3">🎮 بازی‌ها</a>
        </div>
        
        <div class="clock-section">
            <div class="clock-icon">🕐</div>
            <div class="clock" id="clock">--:--:--</div>
            <div class="date" id="date">---</div>
        </div>
        
        <div class="card">
            <div class="card-title" id="weatherTitle">🌤 آب و هوا</div>
            <div class="weather-card" id="weatherData">__WEATHER_DATA__</div>
            <div class="lang-display" onclick="showProvinceModal()" id="provinceDisplay">انتخاب استان...</div>
        </div>
        
        <div class="card">
            <div class="card-title"><span class="currency-icon">💱</span> <span id="currencyTitle">قیمت ارز</span></div>
            <input class="currency-search" id="currencySearchInput" placeholder="🔍 جستجوی ارز..." onkeyup="filterCurrency(this.value)">
            <div class="currency-scroll" id="currencyList">__CURRENCY_DATA__</div>
        </div>
        
        <div class="card">
            <div class="card-title"><span class="currency-icon">💰</span> <span id="goldTitle">طلا و سکه</span></div>
            <input class="currency-search" id="goldSearchInput" placeholder="🔍 جستجوی طلا..." onkeyup="filterGold(this.value)">
            <div class="currency-scroll" id="goldList">__GOLD_DATA__</div>
        </div>
        
        <div class="card">
            <div class="card-title" id="footballTitle">⚽ بازی‌های داغ</div>
            <div class="filter-btns">
                <button class="filter-btn active" id="filterAll" onclick="filterMatches('all', this)">همه</button>
                <button class="filter-btn" id="filterFinished" onclick="filterMatches('finished', this)">پایان یافته</button>
                <button class="filter-btn" id="filterLive" onclick="filterMatches('live', this)">در حال انجام</button>
                <button class="filter-btn" id="filterUpcoming" onclick="filterMatches('upcoming', this)">برگزار نشده</button>
            </div>
            <div class="football-scroll" id="footballList">__MATCHES_FA__</div>
        </div>
        
        <div class="card">
            <div class="card-title" id="newsTitle">📰 آخرین اخبار</div>
            <div class="news-scroll" id="newsList">__NEWS_DATA__</div>
        </div>
        
        <div class="card">
            <div class="card-title" id="translateTitle">🌐 ترجمه</div>
            <div class="lang-row">
                <div class="lang-box">
                    <div class="lang-display" onclick="showLangModal('from')" id="fromDisplay">انتخاب مبدا</div>
                </div>
                <button class="swap-btn" id="swapBtn" onclick="swapLanguages()">⇄</button>
                <div class="lang-box">
                    <div class="lang-display" onclick="showLangModal('to')" id="toDisplay">انتخاب مقصد</div>
                </div>
            </div>
            <textarea id="text" placeholder="متن خود را وارد کنید..."></textarea>
            <div class="result" id="result">نتیجه ترجمه...</div>
            <div class="btn-row">
                <button class="translate-btn" id="translateBtn" onclick="translateText()">ترجمه</button>
                <button class="copy-btn" id="copyBtn" onclick="copyResult()">کپی</button>
            </div>
        </div>
        
        <div class="footer" id="footer">© 2026 AmirHarter - تمامی حقوق محفوظ است</div>
    </div>
    
    <script>
        const languagesFa = {"fa":"فارسی","en":"انگلیسی","ar":"عربی","fr":"فرانسوی","de":"آلمانی","es":"اسپانیایی","it":"ایتالیایی","pt":"پرتغالی","ru":"روسی","tr":"ترکی","zh":"چینی","ja":"ژاپنی","ko":"کره‌ای","hi":"هندی","ur":"اردو","nl":"هلندی","pl":"لهستانی","sv":"سوئدی","no":"نروژی","da":"دانمارکی","fi":"فنلاندی","el":"یونانی","he":"عبری","th":"تایلندی","vi":"ویتنامی","id":"اندونزیایی","ms":"مالایی","cs":"چکی","sk":"اسلواکی","hu":"مجاری","ro":"رومانیایی","bg":"بلغاری","uk":"اوکراینی","sr":"صربی","hr":"کرواتی","sl":"اسلوونیایی"};
        
        const languagesEn = {"fa":"Persian","en":"English","ar":"Arabic","fr":"French","de":"German","es":"Spanish","it":"Italian","pt":"Portuguese","ru":"Russian","tr":"Turkish","zh":"Chinese","ja":"Japanese","ko":"Korean","hi":"Hindi","ur":"Urdu","nl":"Dutch","pl":"Polish","sv":"Swedish","no":"Norwegian","da":"Danish","fi":"Finnish","el":"Greek","he":"Hebrew","th":"Thai","vi":"Vietnamese","id":"Indonesian","ms":"Malay","cs":"Czech","sk":"Slovak","hu":"Hungarian","ro":"Romanian","bg":"Bulgarian","uk":"Ukrainian","sr":"Serbian","hr":"Croatian","sl":"Slovenian"};
        
        const provinces = __PROVINCES__;
        const provincesEn = __PROVINCES_EN__;
        const currencyNamesEn = __CURRENCY_NAMES_EN__;
        const goldNamesEn = __GOLD_NAMES_EN__;
        
        const matchesFa = '__MATCHES_FA__';
        const matchesEn = '__MATCHES_EN__';
        
        const newsFa = '__NEWS_DATA__';
        const weatherFa = '__WEATHER_DATA__';
        const currencyFa = '__CURRENCY_DATA__';
        const goldFa = '__GOLD_DATA__';
        
        let currentLang = 'fa';
        let fromLang = '';
        let toLang = '';
        let langMode = 'from';
        let currentFontSize = '1rem';
        
        function toggleLanguage() {
            if (currentLang === 'fa') {
                currentLang = 'en';
                document.body.style.direction = 'ltr';
                
                document.getElementById('settingsTitle').textContent = '⚙️ Settings';
                document.getElementById('langLabel').textContent = 'Language: English';
                document.getElementById('themeText').textContent = '🌙 Change Theme';
                document.getElementById('fontLabel').textContent = 'Font: ' + (currentFontSize === '0.9rem' ? 'Small' : currentFontSize === '1.2rem' ? 'Large' : 'Medium');
                document.getElementById('shareText').textContent = '📤 Share Site';
                document.getElementById('reportText').textContent = '⚠️ Report Issue';
                document.getElementById('aboutText').textContent = '📖 About Us';
                document.getElementById('versionText').textContent = 'Version: v42';
                
                document.getElementById('searchBtn').textContent = 'Search';
                document.getElementById('mainSearch').placeholder = 'Search in AMIR HARTER';
                document.getElementById('option1').textContent = '📱 Google Play';
                document.getElementById('option2').textContent = '📺 Telewebion';
                document.getElementById('option3').textContent = '🎮 Games';
                
                document.getElementById('weatherTitle').textContent = '🌤 Weather';
                document.getElementById('currencyTitle').textContent = 'Currency Rates';
                document.getElementById('goldTitle').textContent = 'Gold & Coins';
                document.getElementById('footballTitle').textContent = '⚽ Hot Matches';
                document.getElementById('newsTitle').textContent = '📰 Latest News';
                document.getElementById('translateTitle').textContent = '🌐 Translate';
                
                document.getElementById('currencySearchInput').placeholder = '🔍 Search currency...';
                document.getElementById('goldSearchInput').placeholder = '🔍 Search gold...';
                document.getElementById('provinceDisplay').textContent = 'Select province...';
                
                document.getElementById('filterAll').textContent = 'All';
                document.getElementById('filterFinished').textContent = 'Finished';
                document.getElementById('filterLive').textContent = 'Live';
                document.getElementById('filterUpcoming').textContent = 'Upcoming';
                
                document.getElementById('fromDisplay').textContent = 'Select source';
                document.getElementById('toDisplay').textContent = 'Select target';
                document.querySelector('textarea').placeholder = 'Enter your text...';
                document.getElementById('result').textContent = 'Translation result...';
                document.getElementById('translateBtn').textContent = 'Translate';
                document.getElementById('copyBtn').textContent = 'Copy';
                
                document.getElementById('footer').textContent = '© 2026 AmirHarter - All rights reserved';
                
                document.getElementById('aboutModalTitle').textContent = '📖 About Us';
                document.getElementById('reportModalTitle').textContent = '⚠️ Report Issue';
                document.getElementById('fontModalTitle').textContent = '🔤 Select Font';
                document.getElementById('langModalTitle').textContent = '🌐 Select Language';
                document.getElementById('provinceModalTitle').textContent = '📍 Select Province';
                
                document.getElementById('aboutContentFa').style.display = 'none';
                document.getElementById('aboutContentEn').style.display = 'block';
                document.getElementById('reportTextFa').style.display = 'none';
                document.getElementById('reportTextEn').style.display = 'block';
                
                document.getElementById('langSearchInput').placeholder = '🔍 Search language...';
                document.getElementById('provinceSearchInput').placeholder = '🔍 Search province...';
                
                document.getElementById('footballList').innerHTML = matchesEn;
                
                updateCurrencyAndGoldForEnglish();
                
                if (document.getElementById('langModal').style.display === 'flex') {
                    renderLangList();
                }
                
                if (document.getElementById('provinceModal').style.display === 'flex') {
                    renderProvinceList();
                }
                
            } else {
                currentLang = 'fa';
                document.body.style.direction = 'rtl';
                
                document.getElementById('settingsTitle').textContent = '⚙️ تنظیمات';
                document.getElementById('langLabel').textContent = 'زبان: فارسی';
                document.getElementById('themeText').textContent = '🌙 تغییر تم';
                document.getElementById('fontLabel').textContent = 'فونت: ' + (currentFontSize === '0.9rem' ? 'کوچیک' : currentFontSize === '1.2rem' ? 'بزرگ' : 'متوسط');
                document.getElementById('shareText').textContent = '📤 اشتراک‌گذاری سایت';
                document.getElementById('reportText').textContent = '⚠️ گزارش مشکل';
                document.getElementById('aboutText').textContent = '📖 درباره ما';
                document.getElementById('versionText').textContent = 'نسخه: v42';
                
                document.getElementById('searchBtn').textContent = 'جستجو';
                document.getElementById('mainSearch').placeholder = 'در AMIR HARTER';
                document.getElementById('option1').textContent = '📱 گوگل‌پلی';
                document.getElementById('option2').textContent = '📺 تلوبیون';
                document.getElementById('option3').textContent = '🎮 بازی‌ها';
                
                document.getElementById('weatherTitle').textContent = '🌤 آب و هوا';
                document.getElementById('currencyTitle').textContent = 'قیمت ارز';
                document.getElementById('goldTitle').textContent = 'طلا و سکه';
                document.getElementById('footballTitle').textContent = '⚽ بازی‌های داغ';
                document.getElementById('newsTitle').textContent = '📰 آخرین اخبار';
                document.getElementById('translateTitle').textContent = '🌐 ترجمه';
                
                document.getElementById('currencySearchInput').placeholder = '🔍 جستجوی ارز...';
                document.getElementById('goldSearchInput').placeholder = '🔍 جستجوی طلا...';
                document.getElementById('provinceDisplay').textContent = 'انتخاب استان...';
                
                document.getElementById('filterAll').textContent = 'همه';
                document.getElementById('filterFinished').textContent = 'پایان یافته';
                document.getElementById('filterLive').textContent = 'در حال انجام';
                document.getElementById('filterUpcoming').textContent = 'برگزار نشده';
                
                document.getElementById('fromDisplay').textContent = 'انتخاب مبدا';
                document.getElementById('toDisplay').textContent = 'انتخاب مقصد';
                document.querySelector('textarea').placeholder = 'متن خود را وارد کنید...';
                document.getElementById('result').textContent = 'نتیجه ترجمه...';
                document.getElementById('translateBtn').textContent = 'ترجمه';
                document.getElementById('copyBtn').textContent = 'کپی';
                
                document.getElementById('footer').textContent = '© 2026 AmirHarter - تمامی حقوق محفوظ است';
                
                document.getElementById('aboutModalTitle').textContent = '📖 درباره ما';
                document.getElementById('reportModalTitle').textContent = '⚠️ گزارش مشکل';
                document.getElementById('fontModalTitle').textContent = '🔤 انتخاب فونت';
                document.getElementById('langModalTitle').textContent = '🌐 انتخاب زبان';
                document.getElementById('provinceModalTitle').textContent = '📍 انتخاب استان';
                
                document.getElementById('aboutContentFa').style.display = 'block';
                document.getElementById('aboutContentEn').style.display = 'none';
                document.getElementById('reportTextFa').style.display = 'block';
                document.getElementById('reportTextEn').style.display = 'none';
                
                document.getElementById('langSearchInput').placeholder = '🔍 جستجوی زبان...';
                document.getElementById('provinceSearchInput').placeholder = '🔍 جستجوی استان...';
                
                document.getElementById('footballList').innerHTML = matchesFa;
                
                document.getElementById('weatherData').innerHTML = weatherFa;
                document.getElementById('currencyList').innerHTML = currencyFa;
                document.getElementById('goldList').innerHTML = goldFa;
                document.getElementById('newsList').innerHTML = newsFa;
                
                if (document.getElementById('langModal').style.display === 'flex') {
                    renderLangList();
                }
                
                if (document.getElementById('provinceModal').style.display === 'flex') {
                    renderProvinceList();
                }
            }
            updateClock();
        }
        
        function updateCurrencyAndGoldForEnglish() {
            const currencyItems = document.querySelectorAll('#currencyList .currency-item');
            currencyItems.forEach(item => {
                const span = item.querySelector('span:first-child');
                const nameFa = span.textContent;
                if (currencyNamesEn[nameFa]) {
                    span.textContent = currencyNamesEn[nameFa];
                    item.setAttribute('data-name', currencyNamesEn[nameFa]);
                }
            });
            
            const goldItems = document.querySelectorAll('#goldList .currency-item');
            goldItems.forEach(item => {
                const span = item.querySelector('span:first-child');
                const nameFa = span.textContent;
                if (goldNamesEn[nameFa]) {
                    span.textContent = goldNamesEn[nameFa];
                    item.setAttribute('data-name', goldNamesEn[nameFa]);
                }
            });
        }
        
        function updateClock() {
            const now = new Date();
            if (currentLang === 'en') {
                document.getElementById('clock').textContent = now.toLocaleTimeString('en-US');
                document.getElementById('date').textContent = now.toLocaleDateString('en-US', {weekday:'long', year:'numeric', month:'long', day:'numeric'});
            } else {
                document.getElementById('clock').textContent = now.toLocaleTimeString('fa-IR');
                document.getElementById('date').textContent = now.toLocaleDateString('fa-IR', {weekday:'long', year:'numeric', month:'long', day:'numeric'});
            }
        }
        setInterval(updateClock, 1000);
        updateClock();
        
        function showLangModal(mode) {
            langMode = mode;
            const title = document.getElementById('langModalTitle');
            if (currentLang === 'en') {
                title.textContent = mode === 'from' ? '🌐 Select Source Language' : '🌐 Select Target Language';
            } else {
                title.textContent = mode === 'from' ? '🌐 انتخاب زبان مبدا' : '🌐 انتخاب زبان مقصد';
            }
            document.getElementById('langModal').style.display = 'flex';
            renderLangList();
        }
        
        function renderLangList() {
            const list = document.getElementById('langList');
            const langs = (currentLang === 'en') ? languagesEn : languagesFa;
            list.innerHTML = '';
            for (const code in langs) {
                list.innerHTML += '<div class="lang-item" onclick="selectLang(\'' + code + '\')">' + langs[code] + '</div>';
            }
        }
        
        function selectLang(code) {
            const langs = (currentLang === 'en') ? languagesEn : languagesFa;
            if (langMode === 'from') {
                fromLang = code;
                document.getElementById('fromDisplay').textContent = langs[code];
            } else {
                toLang = code;
                document.getElementById('toDisplay').textContent = langs[code];
            }
            closeModal('langModal');
        }
        
        function filterLanguages(query) {
            const list = document.getElementById('langList');
            const langs = (currentLang === 'en') ? languagesEn : languagesFa;
            list.innerHTML = '';
            for (const code in langs) {
                if (langs[code].toLowerCase().includes(query.toLowerCase()) || query === '') {
                    list.innerHTML += '<div class="lang-item" onclick="selectLang(\'' + code + '\')">' + langs[code] + '</div>';
                }
            }
        }
        
        function showProvinceModal() {
            document.getElementById('provinceModal').style.display = 'flex';
            renderProvinceList();
        }
        
        function renderProvinceList() {
            const list = document.getElementById('provinceList');
            list.innerHTML = '';
            if (currentLang === 'en') {
                for (const nameEn in provincesEn) {
                    list.innerHTML += '<div class="province-item" onclick="selectProvince(\'' + nameEn + '\')">' + nameEn + '</div>';
                }
            } else {
                for (const nameFa in provinces) {
                    list.innerHTML += '<div class="province-item" onclick="selectProvince(\'' + nameFa + '\')">' + nameFa + '</div>';
                }
            }
        }
        
        function selectProvince(name) {
            let cityFa = name;
            let cityEn = name;
            
            if (currentLang === 'en') {
                cityEn = name;
                cityFa = provincesEn[name] || name;
            } else {
                cityFa = name;
                cityEn = Object.keys(provincesEn).find(key => provincesEn[key] === name) || name;
            }
            
            document.getElementById('provinceDisplay').textContent = currentLang === 'en' ? cityEn : cityFa;
            closeModal('provinceModal');
            
            const coords = provinces[cityFa] || [35.6892, 51.3890];
            const lat = coords[0];
            const lon = coords[1];
            const isEnglish = currentLang === 'en';
            
            fetch('https://api.open-meteo.com/v1/forecast?latitude=' + lat + '&longitude=' + lon + '&current_weather=true&timezone=Asia%2FTehran')
                .then(r => r.json())
                .then(d => {
                    const temp = d.current_weather.temperature;
                    const wind = d.current_weather.windspeed;
                    const code = d.current_weather.weathercode;
                    
                    if (isEnglish) {
                        const descs = {0:'Sunny',1:'Partly Sunny',2:'Partly Cloudy',3:'Cloudy',

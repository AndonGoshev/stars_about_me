import requests

def _fetch_horoscope(sign: str, endpoint: str, params: dict = None):
    base_url = "https://horoscope-app-api.vercel.app/api/v1"
    url = f"{base_url}{endpoint}"
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("data")
    return None

def get_daily_horoscope(sign: str):
    return _fetch_horoscope(sign, "/get-horoscope/daily", {"sign": sign, "day": "TODAY"})

def get_weekly_horoscope(sign: str):
    return _fetch_horoscope(sign, "/get-horoscope/weekly", {"sign": sign})

def get_monthly_horoscope(sign: str):
    return _fetch_horoscope(sign, "/get-horoscope/monthly", {"sign": sign})


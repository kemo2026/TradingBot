from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from binance.client import Client

API_KEY = "api_key_ketu"
API_SECRET = "secret_key_ketu"

client = Client(API_KEY, API_SECRET)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_klines(interval, limit=100):
    return client.futures_klines(
        symbol="XAUUSDT",
        interval=interval,
        limit=limit
    )

def get_closes(klines):
    return [float(k[4]) for k in klines]

def get_highs(klines):
    return [float(k[2]) for k in klines]

def get_lows(klines):
    return [float(k[3]) for k in klines]

def detect_trend(klines):
    closes = get_closes(klines)
    highs = get_highs(klines)
    lows = get_lows(klines)
    last_high = highs[-1]
    prev_high = highs[-5]
    last_low = lows[-1]
    prev_low = lows[-5]
    if last_high > prev_high and last_low > prev_low:
        return "BULLISH"
    elif last_high < prev_high and last_low < prev_low:
        return "BEARISH"
    return "NEUTRAL"

def detect_sweep(klines):
    highs = get_highs(klines)
    lows = get_lows(klines)
    closes = get_closes(klines)
    if highs[-1] > highs[-2] and closes[-1] < highs[-2]:
        return "BEARISH_SWEEP"
    elif lows[-1] < lows[-2] and closes[-1] > lows[-2]:
        return "BULLISH_SWEEP"
    return None

def detect_bos(klines):
    highs = get_highs(klines)
    lows = get_lows(klines)
    closes = get_closes(klines)
    if closes[-1] > highs[-5]:
        return "BULLISH_BOS"
    elif closes[-1] < lows[-5]:
        return "BEARISH_BOS"
    return None

def detect_fvg(klines):
    highs = get_highs(klines)
    lows = get_lows(klines)
    fvg_bull = []
    fvg_bear = []
    for i in range(2, len(klines)-1):
        if lows[i] > highs[i-2]:
            fvg_bull.append(i)
        if highs[i] < lows[i-2]:
            fvg_bear.append(i)
    return len(fvg_bull), len(fvg_bear)

@app.get("/signal")
def get_signal():
    try:
        klines_1d = get_klines(Client.KLINE_INTERVAL_1DAY)
        klines_4h = get_klines(Client.KLINE_INTERVAL_4HOUR)
        klines_1h = get_klines(Client.KLINE_INTERVAL_1HOUR)
        klines_15m = get_klines(Client.KLINE_INTERVAL_15MINUTE)

        price = get_closes(klines_15m)[-1]
        
        trend_1d = detect_trend(klines_1d)
        trend_4h = detect_trend(klines_4h)
        sweep_4h = detect_sweep(klines_4h)
        bos_1h = detect_bos(klines_1h)
        bos_15m = detect_bos(klines_15m)
        fvg_bull, fvg_bear = detect_fvg(klines_15m)

        long_signals = 0
        short_signals = 0

        if trend_1d == "BULLISH": long_signals += 2
        if trend_1d == "BEARISH": short_signals += 2
        if trend_4h == "BULLISH": long_signals += 1
        if trend_4h == "BEARISH": short_signals += 1
        if sweep_4h == "BULLISH_SWEEP": long_signals += 2
        if sweep_4h == "BEARISH_SWEEP": short_signals += 2
        if bos_1h == "BULLISH_BOS": long_signals += 1
        if bos_1h == "BEARISH_BOS": short_signals += 1
        if bos_15m == "BULLISH_BOS": long_signals += 1
        if bos_15m == "BEARISH_BOS": short_signals += 1
        if fvg_bull > 0: long_signals += 1
        if fvg_bear > 0: short_signals += 1

        atr = 20
        if long_signals >= 6 and long_signals > short_signals:
            return {
                "signal": "LONG",
                "price": round(price, 2),
                "entry": round(price, 2),
                "sl": round(price - atr, 2),
                "tp1": round(price + atr * 2, 2),
                "tp2": round(price + atr * 3, 2),
                "long_signals": long_signals,
                "short_signals": short_signals
            }
        elif short_signals >= 6 and short_signals > long_signals:
            return {
                "signal": "SHORT",
                "price": round(price, 2),
                "entry": round(price, 2),
                "sl": round(price + atr, 2),
                "tp1": round(price - atr * 2, 2),
                "tp2": round(price - atr * 3, 2),
                "long_signals": long_signals,
                "short_signals": short_signals
            }
        else:
            return {
                "signal": "WAIT",
                "price": round(price, 2),
                "long_signals": long_signals,
                "short_signals": short_signals
            }
    except Exception as e:
        return {"error": str(e)}
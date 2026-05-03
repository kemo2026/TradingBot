from binance.client import Client
import time
from datetime import datetime

API_KEY = "Mbvmr8Y574ODX7WoDyctepDFr3q3RYCFQqE1BV2FcpOmABgqzmXFRszMqZxSmQJ2"
API_SECRET = "QrdYldYHBQrm9akAtQq5U79nKfsQ7XErUr6Dmi1sNUL4MA5mhXrZxkDMjVGYIQ55"

client = Client(API_KEY, API_SECRET)

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

def calculate_ma(closes, period):
    return sum(closes[-period:]) / period

def detect_trend(klines):
    closes = get_closes(klines)
    highs = get_highs(klines)
    lows = get_lows(klines)
    
    # Higher Highs dhe Higher Lows = Bullish
    # Lower Highs dhe Lower Lows = Bearish
    last_high = highs[-1]
    prev_high = highs[-5]
    last_low = lows[-1]
    prev_low = lows[-5]
    
    if last_high > prev_high and last_low > prev_low:
        return "BULLISH"
    elif last_high < prev_high and last_low < prev_low:
        return "BEARISH"
    else:
        return "NEUTRAL"

def detect_liquidity_sweep(klines):
    highs = get_highs(klines)
    lows = get_lows(klines)
    closes = get_closes(klines)
    
    # Sweep i High-it — çmimi kaloi lart pastaj ra
    swept_high = (highs[-1] > highs[-2] and 
                  closes[-1] < highs[-2])
    
    # Sweep i Low-it — çmimi kaloi poshtë pastaj u ngrit
    swept_low = (lows[-1] < lows[-2] and 
                 closes[-1] > lows[-2])
    
    if swept_high:
        return "BEARISH_SWEEP"  # MM morën liquidity lart → SHORT
    elif swept_low:
        return "BULLISH_SWEEP"  # MM morën liquidity poshtë → LONG
    else:
        return None

def detect_fvg(klines):
    highs = get_highs(klines)
    lows = get_lows(klines)
    closes = get_closes(klines)
    
    fvg_bullish = []
    fvg_bearish = []
    
    for i in range(2, len(klines)-1):
        # Bullish FVG — boshllëk lart
        if lows[i] > highs[i-2]:
            fvg_bullish.append({
                'top': lows[i],
                'bottom': highs[i-2],
                'index': i
            })
        
        # Bearish FVG — boshllëk poshtë
        if highs[i] < lows[i-2]:
            fvg_bearish.append({
                'top': lows[i-2],
                'bottom': highs[i],
                'index': i
            })
    
    return fvg_bullish, fvg_bearish

def detect_order_block(klines):
    closes = get_closes(klines)
    highs = get_highs(klines)
    lows = get_lows(klines)
    
    # Bullish Order Block — candela e fundit bearish para rritjes
    bullish_ob = None
    bearish_ob = None
    
    for i in range(len(closes)-10, len(closes)-1):
        # Bullish OB
        if closes[i] < closes[i-1] and closes[i+1] > highs[i]:
            bullish_ob = {
                'top': highs[i],
                'bottom': lows[i]
            }
        
        # Bearish OB
        if closes[i] > closes[i-1] and closes[i+1] < lows[i]:
            bearish_ob = {
                'top': highs[i],
                'bottom': lows[i]
            }
    
    return bullish_ob, bearish_ob

def detect_bos(klines):
    highs = get_highs(klines)
    lows = get_lows(klines)
    closes = get_closes(klines)
    
    # Break of Structure Bullish
    if closes[-1] > highs[-5]:
        return "BULLISH_BOS"
    
    # Break of Structure Bearish
    elif closes[-1] < lows[-5]:
        return "BEARISH_BOS"
    
    return None

def detect_smt(klines_gold):
    closes = get_closes(klines_gold)
    highs = get_highs(klines_gold)
    
    # SMT i thjeshtuar — divergencë
    if highs[-1] > highs[-3] and closes[-1] < closes[-3]:
        return "BEARISH_SMT"
    elif highs[-1] < highs[-3] and closes[-1] > closes[-3]:
        return "BULLISH_SMT"
    
    return None

def calculate_sl_tp(price, direction, atr=20):
    if direction == "LONG":
        sl = price - atr
        tp1 = price + (atr * 2)  # 1:2 RR
        tp2 = price + (atr * 3)  # 1:3 RR
    else:
        sl = price + atr
        tp1 = price - (atr * 2)
        tp2 = price - (atr * 3)
    
    return sl, tp1, tp2

def analyze():
    try:
        now = datetime.now().strftime("%H:%M:%S")
        print(f"\n{'='*50}")
        print(f"⏰ Ora: {now}")
        print(f"{'='*50}")
        
        # Merr data nga timeframes të ndryshme
        klines_1d = get_klines(Client.KLINE_INTERVAL_1DAY, 50)
        klines_4h = get_klines(Client.KLINE_INTERVAL_4HOUR, 50)
        klines_1h = get_klines(Client.KLINE_INTERVAL_1HOUR, 50)
        klines_15m = get_klines(Client.KLINE_INTERVAL_15MINUTE, 50)
        
        # Çmimi aktual
        closes_15m = get_closes(klines_15m)
        price = closes_15m[-1]
        print(f"💰 Çmimi: {price:.2f}")
        
        # HAPI 1 — Trendi i madh
        trend_1d = detect_trend(klines_1d)
        trend_4h = detect_trend(klines_4h)
        print(f"\n📊 TRENDI:")
        print(f"   1D: {trend_1d}")
        print(f"   4H: {trend_4h}")
        
        # HAPI 2 — Liquidity Sweep
        sweep_4h = detect_liquidity_sweep(klines_4h)
        sweep_1h = detect_liquidity_sweep(klines_1h)
        print(f"\n💧 LIQUIDITY SWEEP:")
        print(f"   4H: {sweep_4h or 'ASNJE'}")
        print(f"   1H: {sweep_1h or 'ASNJE'}")
        
        # HAPI 3 — Break of Structure
        bos_1h = detect_bos(klines_1h)
        bos_15m = detect_bos(klines_15m)
        print(f"\n🔨 BREAK OF STRUCTURE:")
        print(f"   1H: {bos_1h or 'ASNJE'}")
        print(f"   15m: {bos_15m or 'ASNJE'}")
        
        # HAPI 4 — Fair Value Gap
        fvg_bull_15m, fvg_bear_15m = detect_fvg(klines_15m)
        print(f"\n📦 FAIR VALUE GAP (15m):")
        print(f"   Bullish FVG: {len(fvg_bull_15m)} zona")
        print(f"   Bearish FVG: {len(fvg_bear_15m)} zona")
        
        # HAPI 5 — Order Blocks
        bull_ob, bear_ob = detect_order_block(klines_1h)
        print(f"\n🧱 ORDER BLOCKS (1H):")
        if bull_ob:
            print(f"   Bullish OB: {bull_ob['bottom']:.2f} - {bull_ob['top']:.2f}")
        if bear_ob:
            print(f"   Bearish OB: {bear_ob['bottom']:.2f} - {bear_ob['top']:.2f}")
        
        # HAPI 6 — SMT Divergence
        smt = detect_smt(klines_1h)
        print(f"\n📈 SMT DIVERGENCE: {smt or 'ASNJE'}")
        
        # VENDIMI FINAL
        print(f"\n{'='*50}")
        
        long_signals = 0
        short_signals = 0
        
        # Numëro sinjalet
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
        if smt == "BULLISH_SMT": long_signals += 2
        if smt == "BEARISH_SMT": short_signals += 2
        if len(fvg_bull_15m) > 0: long_signals += 1
        if len(fvg_bear_15m) > 0: short_signals += 1
        
        print(f"🟢 Sinjale LONG: {long_signals}")
        print(f"🔴 Sinjale SHORT: {short_signals}")
        
        # Sinjal final
        if long_signals >= 6 and long_signals > short_signals:
            sl, tp1, tp2 = calculate_sl_tp(price, "LONG")
            print(f"\n✅ SINJAL: 🟢 LONG")
            print(f"   Entry:  {price:.2f}")
            print(f"   SL:     {sl:.2f}")
            print(f"   TP1:    {tp1:.2f} (1:2)")
            print(f"   TP2:    {tp2:.2f} (1:3)")
            print(f"   Kapital: 20€ | Leverage: x5")
            
        elif short_signals >= 6 and short_signals > long_signals:
            sl, tp1, tp2 = calculate_sl_tp(price, "SHORT")
            print(f"\n✅ SINJAL: 🔴 SHORT")
            print(f"   Entry:  {price:.2f}")
            print(f"   SL:     {sl:.2f}")
            print(f"   TP1:    {tp1:.2f} (1:2)")
            print(f"   TP2:    {tp2:.2f} (1:3)")
            print(f"   Kapital: 20€ | Leverage: x5")
            
        else:
            print(f"\n⏳ PRIT — Nuk ka sinjal të qartë!")
            print(f"   Tregu nuk ka konfirmim të mjaftueshëm")
        
        print(f"{'='*50}")
        
    except Exception as e:
        print(f"Gabim: {e}")

# Ekzekuto çdo 60 sekonda
print("🤖 Trading Bot SMC — Aktiv!")
print("⏰ Analizon çdo 60 sekonda...")
while True:
    analyze()
    time.sleep(60)
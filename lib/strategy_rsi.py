# strategy_rsi.py
from __future__ import annotations
import numpy as np
import pandas as pd

def rsi_wilder(close: pd.Series, period: int = 14) -> pd.Series:
    close = pd.Series(close).astype(float)
    delta = close.diff()
    gain = delta.clip(lower=0.0)
    loss = -delta.clip(upper=0.0)
    avg_gain = gain.ewm(alpha=1/period, adjust=False, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1/period, adjust=False, min_periods=period).mean()
    rs = avg_gain / avg_loss.replace(0.0, np.nan)
    return 100.0 - (100.0 / (1.0 + rs))

def macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
    close = pd.Series(close).astype(float)
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    line = ema_fast - ema_slow
    sig = line.ewm(span=signal, adjust=False).mean()
    hist = line - sig
    return line, sig, hist

def sma(close: pd.Series, window: int = 50) -> pd.Series:
    return pd.Series(close).astype(float).rolling(window).mean()

def _cross_up(series: pd.Series, level: float) -> pd.Series:
    s = pd.Series(series)
    return (s.shift(1) <= level) & (s > level)

def _cross_down(series: pd.Series, level: float) -> pd.Series:
    s = pd.Series(series)
    return (s.shift(1) >= level) & (s < level)

def trend_ok(close: pd.Series, cfg: dict) -> pd.Series:
    trend_cfg = (cfg.get("trend") or {})
    t = str(trend_cfg.get("type", "none")).lower()
    if t == "macd":
        line, sig, _ = macd(close,
                            fast=trend_cfg.get("macd_fast", 12),
                            slow=trend_cfg.get("macd_slow", 26),
                            signal=trend_cfg.get("macd_signal", 9))
        return pd.Series(np.where(line >= sig, 1, -1), index=pd.Series(close).index)
    if t == "sma":
        ma = sma(close, trend_cfg.get("sma_window", 50))
        return pd.Series(np.where(pd.Series(close) >= ma, 1, -1), index=pd.Series(close).index)
    return pd.Series(1, index=pd.Series(close).index)

def generate_rsi_signals(close: pd.Series, cfg: dict) -> pd.DataFrame:
    r = cfg.get("rsi", {})
    mode = str(r.get("mode", "centerline")).lower()
    period = int(r.get("period", 14))
    rsi = rsi_wilder(close, period)
    tside = trend_ok(close, cfg)
    sig = pd.Series(0, index=pd.Series(close).index)
    if mode == "centerline":
        cl = float(r.get("centerline", 50))
        buy  = (rsi > cl) & (tside == 1)
        sell = (rsi < cl) & (tside == -1)
        sig = np.select([buy, sell], [1, -1], default=0)
    elif mode == "reversal":
        ob = float(r.get("overbought", 70))
        os = float(r.get("oversold", 30))
        if bool(r.get("require_cross", True)):
            buy  = _cross_up(rsi, os)
            sell = _cross_down(rsi, ob)
        else:
            buy  = (rsi <= os)
            sell = (rsi >= ob)
        sig = np.select([buy, sell], [1, -1], default=0)
    else:
        raise ValueError(f"Unknown RSI mode: {mode}")
    return pd.DataFrame({
        "close": pd.Series(close).astype(float),
        "rsi": rsi.astype(float),
        "trend_side": tside.astype(int),
        "signal": pd.Series(sig, index=pd.Series(close).index, dtype=int)
    })

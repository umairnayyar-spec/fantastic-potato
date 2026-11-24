# XAUUSD 5M Volatility Breakout — Permanent Project Memory

Read this whole file before touching anything in this folder. Section 3 is the
anti-regression list. Do not redesign the indicator, do not add lagging moving
averages or oscillators, and do not suggest converting it to a strategy.

## 1. Trader Profile, Platform & Hard Constraints

- **Timezone:** PKT (UTC+5).
- **Asset & chart:** XAUUSD (Gold spot / USD), **5-minute (`5m`)** timeframe, OANDA feed on TradingView.
  - The trader noticed `15m` gives cleaner signals but chose to stay on `5m` for now. Do not switch timeframes unprompted.
- **Execution broker:** Will Trade (**demo account**). Orders are placed by hand on mobile/desktop from TradingView alerts and the on-chart labels.
- **Starting capital:** **$497.00 USD**. Balance on 2026-11-18: **~$485.57** (max risk $9.71).

### Risk rules (strict)
- Max risk per trade: **2% = $10.00 USD**, hard cap.
- Contract math on Will Trade: **`0.01` lot = 1 oz Gold**, so a **$1.00 move in Gold = $1.00 P&L** per 0.01 lot.
- Position size: `max_risk = min(2% × current balance, $10.00)`; `lots = floor(max_risk / |Entry − SL|) × 0.01` (never round up). The balance rule binds before the $10 cap. Use `risk_calc.py`: its RR defaults (1.6 long, 2.0 short) match the indicator.
- **Skip rule:** if `|Entry − SL| > $10.00`, **skip the trade** — even 0.01 lot would break the 2% cap.
- **Tight-stop warning:** if `|Entry − SL| < $0.50` (5 pips), warn that broker spread will likely sweep the stop.

### TradingView Free tier limits (critical)
- **5,000 historical bars** max (~2.5 weeks of `5m` data).
- **1 saved script slot** — always overwrite the existing script; never plan around multiple saved scripts.
- **1 active alert** at a time. Strategy alerts are blocked on Free, so the script **must stay an `indicator()`** with **one unified `alertcondition()`**.

## 2. Session & Timezone Mapping (PKT vs UTC)

- **Active window:** `0700-2030:23456` UTC = **12:00 PM – 01:30 AM PKT** (London open through NY session). Shaded faint green `#00E676` at 98% transparency.
- **Blocked windows (do not change):**
  - Asian session `20:30 – 07:00 UTC` (= 01:30 AM – 12:00 PM PKT): low liquidity, wide spreads, false RVOL spikes.
  - Weekend gap: Monday before 01:00 UTC.
  - Broker rollover: `21:00 – 22:59 UTC`.

## 3. DO NOT REPEAT THESE MISTAKES

These were tested and discarded. Never re-suggest them.

1. **No slow trend filters** — no `200 EMA`, `150 EMA`, or dual `50/200 EMA` crossovers. On `5m` with 5,000 bars they cut trades to 1–2 in 2.5 weeks.
2. **No Stochastic RSI and no Choppiness Index filters.** Tested `k < 20/80`, `k < 25/75`, `chopVal < 58/65`: trade count went to near zero, or win rate fell to 27.27% (PF 0.492).
3. **Never remove the RVOL filter** (`volume / ta.sma(volume, 20) >= 1.5`). Without it: 78 trades, 28.21% WR, 0.69 PF (retail fakeouts). With it: **50.00% WR, 1.801 PF** — this filter is the edge.
4. **Never convert the script back to `strategy()`.** Free account cannot set mobile alerts on strategies. Keep `indicator()`.
5. **Never suggest static horizontal price alerts.** Gold moves in a dynamic volatility tunnel; static levels lag. Keep the unified `alertcondition(buySignal or sellSignal, ...)` set to **Once Per Bar Close**.
6. **Never anchor the Long SL to `lowerBand`.** It made risk huge and put the 1:2 TP out of reach. **Both Long and Short SL anchor to `medianLine` (20 EMA).**
7. **No same-bar state resets.** Always guard `posState` resets with `bar_index > entryBar` so one volatile candle can't open and close a signal on the same bar.
8. **Pine Script v6 only** (`//@version=6`). Never use `zorder` in `plot()`, never `ta.sum()` (use `math.sum()`), never `color.emerald` (use hex `#00E676`).
9. **Do not touch the proven baseline parameters** unless live forward-testing over **20+ trades** justifies it:
   - `baseLength = 20`
   - `atrLength = 10`
   - `multiplier = 1.8`
   - `rrRatio = 2.0`
   - `rvolLength = 20`
   - `rvolThresh = 1.5`

## 4. Current Status

- Production script: `xauusd_5m_sniper.pine` = **v6.2 Parity** (Pine v6, `indicator()`, `max_labels_count=500`, one `alertcondition()`).
- It is a signal-for-signal mirror of the user's `strategy()` **v6.2 [Restored Strategy]** baseline (**2.29 PF, 62.5% WR** on OANDA:XAUUSD 5m).
  The user chose v6.2 on 2026-11-18, so it **supersedes rules 1, 6 and 9 above for this script**: the 200 EMA long filter,
  Long SL = `min(ta.lowest(low, 3), medianLine)`, `longRR = 1.6`, `shortRR = 2.0`, entry window `0700-1945`, hold window `0700-2030`.
- Parity engine (do not "simplify" it): the signal is on bar N, the virtual fill is at the open of N+1 ± 10 ticks of slippage (TP is measured from that fill),
  the SL/TP bracket goes live at N+2 (gap-through fills at the open; if SL and TP both touch, the OHLC-path rule decides), and the
  session-expiry exit applies from N+1. This is how TradingView's broker emulator runs CODE A, so the flat gate opens on the same bars.
- Risk cap input: the default `Account % (live)` = 2% x balance ($9.71 at $485.57). `Fixed $ (CODE A parity)` = $10.00 reproduces
  the backtest exactly. Trades with an SL distance in ($9.71, $10.00] are the only intended divergence.
- Shorts have **no** 200 EMA filter (an earlier conversion wrongly added `close < EMA200`).
- **Never "fix" CW10002 by hoisting `ta.rising(close, 1)`.** In the original, v6 lazy `and` ran it only on bullish bars, so it compared against the previous *bullish* close. Hoisting it changed the long trigger (suspected cause of a 0.95 PF run on 2026-11-24; confirm against the untouched original). Keep the explicit `prevBullClose` form in both scripts.

## 5. Working Rules for Claude in This Folder

- Keep the workspace zero-dependency: plain files only, no package managers or build tools.
- Any Pine change must preserve: `indicator()`, one `alertcondition()`, v6 syntax, the session/blocked windows, the RVOL filter, the v6.2 SL anchors (see section 4), and the N+1 fill / N+2 bracket parity engine (which is stricter than the old `bar_index > entryBar` guard).
- Any trade-sizing advice must apply the $10 cap, the >$10 skip rule, and the <$0.50 warning.

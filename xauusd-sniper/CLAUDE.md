# XAUUSD 5M Volatility Breakout — Permanent Project Memory

Read this whole file before touching anything in this folder. Section 3 is the
anti-regression list. Do not redesign the indicator, do not add lagging moving
averages or oscillators, and do not suggest converting it to a strategy.

## 1. Trader Profile, Platform & Hard Constraints

- **Timezone:** PKT (UTC+5).
- **Asset & chart:** XAUUSD (Gold spot / USD), **5-minute (`5m`)** timeframe, OANDA feed on TradingView.
  - The trader noticed `15m` gives cleaner signals but chose to stay on `5m` for now. Do not switch timeframes unprompted.
- **Execution broker:** Will Trade (**demo account**). Orders are placed by hand on mobile/desktop from TradingView alerts and the on-chart labels.
- **Starting capital:** **$497.00 USD**.

### Risk rules (strict)
- Max risk per trade: **2% = $10.00 USD**, hard cap.
- Contract math on Will Trade: **`0.01` lot = 1 oz Gold**, so a **$1.00 move in Gold = $1.00 P&L** per 0.01 lot.
- Position size: `max_risk = min(2% × current balance, $10.00)`; `lots = floor(max_risk / |Entry − SL|) × 0.01` (never round up). Note 2% of $497 is $9.94, so the balance rule binds before the $10 cap. Use `risk_calc.py`.
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

- Production script: `xauusd_5m_sniper.pine` (Pine v6, `indicator()`).
- Backtest edge verified: **1.801 PF, 50% WR**.
- Newest change: Anti-Trap Long filters (`noTopWick` + `uptrendSlope` + `medianLine` SL). **Awaiting live demo forward-test.** Shorts keep the original breakout logic untouched.

## 5. Working Rules for Claude in This Folder

- Keep the workspace zero-dependency: plain files only, no package managers or build tools.
- Any Pine change must preserve: `indicator()`, one `alertcondition()`, v6 syntax, the session/blocked windows, the RVOL filter, `medianLine` SL for both sides, and the `bar_index > entryBar` guard.
- Any trade-sizing advice must apply the $10 cap, the >$10 skip rule, and the <$0.50 warning.

#!/usr/bin/env python3
"""XAUUSD pre-trade risk calculator for the Will Trade demo account.

Usage:
    python risk_calc.py --entry 2650.40 --sl 2646.10 [--balance 497] [--rr 2.0]

Contract math: 0.01 lot = 1 oz Gold, so a $1.00 price move = $1.00 P&L per 0.01 lot.
Rules (see CLAUDE.md):
  * Max risk = 2% of current balance, and never more than $10.00.
  * SKIP if |entry - SL| > $10.00, or if even 0.01 lot would break the cap.
  * SKIP if |entry - SL| < $0.50 (broker spread will sweep the stop).
  * Lot size is always rounded DOWN to 0.01.
Exit code: 0 = trade allowed, 2 = SKIP.
"""
import argparse
import math
import sys
from decimal import Decimal, ROUND_DOWN

RISK_PCT = Decimal("0.02")
HARD_CAP_USD = Decimal("10.00")
MAX_SL_DIST = Decimal("10.00")
MIN_SL_DIST = Decimal("0.50")
USD_PER_DOLLAR_MOVE_PER_MICRO = Decimal("1.00")  # per 0.01 lot


def calc(entry, sl, balance, rr):
    entry, sl, balance, rr = (Decimal(str(x)) for x in (entry, sl, balance, rr))
    if entry == sl:
        raise ValueError("Entry and SL are identical.")
    direction = "LONG" if sl < entry else "SHORT"
    dist = abs(entry - sl)
    max_risk = min((balance * RISK_PCT).quantize(Decimal("0.01"), ROUND_DOWN), HARD_CAP_USD)

    # Number of 0.01-lot units whose loss at SL stays <= max_risk, rounded down.
    units = int((max_risk / (dist * USD_PER_DOLLAR_MOVE_PER_MICRO)).to_integral_value(ROUND_DOWN))
    lots = Decimal(units) * Decimal("0.01")
    loss_at_sl = dist * units * USD_PER_DOLLAR_MOVE_PER_MICRO
    tp = entry + dist * rr if direction == "LONG" else entry - dist * rr
    profit_at_tp = dist * rr * units * USD_PER_DOLLAR_MOVE_PER_MICRO

    skip = []
    if dist > MAX_SL_DIST:
        skip.append(f"SL distance ${dist:.2f} > ${MAX_SL_DIST:.2f} — even 0.01 lot breaks the 2% cap.")
    elif units == 0:
        skip.append(f"SL distance ${dist:.2f} > max risk ${max_risk:.2f} — even 0.01 lot breaks the 2% cap.")
    if dist < MIN_SL_DIST:
        skip.append(f"SL distance ${dist:.2f} < ${MIN_SL_DIST:.2f} — broker spread trap, stop will get swept.")

    return {
        "direction": direction, "entry": entry, "sl": sl, "dist": dist,
        "balance": balance, "max_risk": max_risk, "lots": lots if not skip else Decimal("0"),
        "calc_lots": lots, "loss_at_sl": loss_at_sl, "tp": tp, "rr": rr,
        "profit_at_tp": profit_at_tp, "skip": skip,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="XAUUSD pre-trade risk calculator (Will Trade, 0.01 lot = $1/$1 move)")
    p.add_argument("--entry", type=float, required=True, help="Entry price")
    p.add_argument("--sl", type=float, required=True, help="Stop loss price")
    p.add_argument("--balance", type=float, default=497.0, help="Current account balance (default 497)")
    p.add_argument("--rr", type=float, default=2.0, help="Reward:risk ratio (default 2.0)")
    a = p.parse_args(argv)

    try:
        r = calc(a.entry, a.sl, a.balance, a.rr)
    except ValueError as e:
        print(f"ERROR: {e}")
        return 1

    line = "=" * 46
    print(line)
    print(f" XAUUSD {r['direction']} — pre-trade check")
    print(line)
    print(f" Balance           : ${r['balance']:.2f}")
    print(f" Max risk (2%)     : ${r['max_risk']:.2f}")
    print(f" Entry             : {r['entry']:.2f}")
    print(f" Stop loss         : {r['sl']:.2f}")
    print(f" SL distance       : ${r['dist']:.2f}")
    print(f" Take profit (1:{r['rr']:g}) : {r['tp']:.2f}")
    print(line)
    if r["skip"]:
        print(" ⛔ SKIP TRADE")
        for reason in r["skip"]:
            print(f"   - {reason}")
        print(line)
        return 2
    print(f" ✅ LOT SIZE       : {r['lots']:.2f}")
    print(f" Loss if SL hit    : -${r['loss_at_sl']:.2f}")
    print(f" Profit if TP hit  : +${r['profit_at_tp']:.2f}")
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Will Trade demo journal for the XAUUSD 5m Sniper (stdlib only).

Commands:
  python journal.py add --dir long --entry 2650.40 --sl 2646.10 --tp 2659.00 \
                        --lots 0.02 --exit 2659.00 [--pnl 17.20] [--time "2026-11-12 18:05"] \
                        [--notes "clean breakout"]
  python journal.py stats          # balance, return %, WR, PF, long vs short split
  python journal.py list           # print every logged trade

pnl_usd is auto-calculated from (exit - entry) x lots x 100 if --pnl is omitted.
Pass --pnl to log the broker's real P&L (spread/commission included) — preferred.
"""
import argparse
import csv
import os
import sys
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "trades.csv")
FIELDS = ["timestamp_pkt", "direction", "entry", "sl", "tp", "lots", "exit_price", "pnl_usd", "notes"]
START_BALANCE = 497.00
FORWARD_TEST_TARGET = 20
PKT = timezone(timedelta(hours=5))


def load():
    if not os.path.exists(CSV_PATH):
        return []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r.get("direction")]


def ensure_header():
    if not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0:
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(FIELDS)


def cmd_add(a):
    direction = a.dir.upper()
    if a.pnl is not None:
        pnl = a.pnl
    else:
        move = (a.exit - a.entry) if direction == "LONG" else (a.entry - a.exit)
        pnl = move * a.lots * 100  # 0.01 lot = $1 per $1 move
    ts = a.time or datetime.now(PKT).strftime("%Y-%m-%d %H:%M")
    ensure_header()
    row = [ts, direction, f"{a.entry:.2f}", f"{a.sl:.2f}", f"{a.tp:.2f}", f"{a.lots:.2f}",
           f"{a.exit:.2f}", f"{pnl:.2f}", a.notes]
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(row)
    n = len(load())
    print(f"Logged trade #{n}: {direction} {a.lots:.2f} lots, P&L {pnl:+.2f} USD")
    print(f"Forward test progress: {n}/{FORWARD_TEST_TARGET}")
    return 0


def summarize(trades):
    pnls = [float(t["pnl_usd"]) for t in trades]
    wins = [p for p in pnls if p > 0]
    losses = [p for p in pnls if p < 0]
    gross_win, gross_loss = sum(wins), -sum(losses)
    if gross_loss > 0:
        pf = f"{gross_win / gross_loss:.3f}"
    else:
        pf = "∞" if gross_win > 0 else "n/a"
    return {
        "n": len(pnls), "wins": len(wins), "losses": len(losses),
        "be": len(pnls) - len(wins) - len(losses),
        "wr": (len(wins) / len(pnls) * 100) if pnls else 0.0,
        "pf": pf, "pnl": sum(pnls),
        "avg_win": (gross_win / len(wins)) if wins else 0.0,
        "avg_loss": (-gross_loss / len(losses)) if losses else 0.0,
    }


def fmt_block(title, s):
    return (f"{title:<8} trades {s['n']:>3} | W {s['wins']:>2} L {s['losses']:>2} BE {s['be']:>2} | "
            f"WR {s['wr']:6.2f}% | PF {s['pf']:>6} | P&L {s['pnl']:+9.2f} | "
            f"avg W {s['avg_win']:+7.2f} avg L {s['avg_loss']:+7.2f}")


def cmd_stats(_a):
    trades = load()
    if not trades:
        print(f"No trades logged yet. Balance ${START_BALANCE:.2f}.")
        return 0
    allr = summarize(trades)
    balance = START_BALANCE + allr["pnl"]
    ret = allr["pnl"] / START_BALANCE * 100
    # Max drawdown on the equity curve
    peak, eq, mdd = START_BALANCE, START_BALANCE, 0.0
    for t in trades:
        eq += float(t["pnl_usd"])
        peak = max(peak, eq)
        mdd = max(mdd, peak - eq)

    line = "=" * 100
    print(line)
    print(f" Balance ${balance:.2f}  (start ${START_BALANCE:.2f})  |  Return {ret:+.2f}%  |  "
          f"Max drawdown -${mdd:.2f}  |  Next 2% risk ${min(balance * 0.02, 10.0):.2f}")
    print(line)
    print(fmt_block("ALL", allr))
    print(fmt_block("LONG", summarize([t for t in trades if t["direction"].upper() == "LONG"])))
    print(fmt_block("SHORT", summarize([t for t in trades if t["direction"].upper() == "SHORT"])))
    print(line)
    n = allr["n"]
    if n < FORWARD_TEST_TARGET:
        print(f" Forward test: {n}/{FORWARD_TEST_TARGET} trades — too few to judge the Anti-Trap Long fix "
              f"or touch any parameter yet.")
    else:
        print(f" Forward test: {n} trades — sample reached. Compare LONG WR/PF above against the "
              f"backtest baseline (50% WR, 1.801 PF).")
    return 0


def cmd_list(_a):
    trades = load()
    if not trades:
        print("No trades logged yet.")
        return 0
    for i, t in enumerate(trades, 1):
        print(f"#{i:>3} {t['timestamp_pkt']} {t['direction']:<5} entry {t['entry']} sl {t['sl']} "
              f"tp {t['tp']} lots {t['lots']} exit {t['exit_price']} P&L {float(t['pnl_usd']):+.2f}  {t['notes']}")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="XAUUSD Sniper trade journal")
    sub = p.add_subparsers(dest="cmd", required=True)
    ad = sub.add_parser("add", help="Log a closed trade")
    ad.add_argument("--dir", required=True, type=str.lower, choices=["long", "short"])
    ad.add_argument("--entry", required=True, type=float)
    ad.add_argument("--sl", required=True, type=float)
    ad.add_argument("--tp", required=True, type=float)
    ad.add_argument("--lots", required=True, type=float)
    ad.add_argument("--exit", required=True, type=float, help="Actual exit price")
    ad.add_argument("--pnl", type=float, help="Broker P&L in USD (auto-calculated if omitted)")
    ad.add_argument("--time", help='PKT time "YYYY-MM-DD HH:MM" (default: now in PKT)')
    ad.add_argument("--notes", default="")
    ad.set_defaults(func=cmd_add)
    sub.add_parser("stats", help="Show performance").set_defaults(func=cmd_stats)
    sub.add_parser("list", help="List trades").set_defaults(func=cmd_list)
    a = p.parse_args(argv)
    return a.func(a)


if __name__ == "__main__":
    sys.exit(main())

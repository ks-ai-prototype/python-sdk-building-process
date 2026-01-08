from __future__ import annotations

import argparse
import sys

from ._version import __version__
from .math_ops import add, subtract, divide
from .transforms import clean_columns


def _cmd_add(args: argparse.Namespace) -> int:
    print(add(args.a, args.b))
    return 0


def _cmd_subtract(args: argparse.Namespace) -> int:
    print(subtract(args.a, args.b))
    return 0


def _cmd_divide(args: argparse.Namespace) -> int:
    print(divide(args.a, args.b, on_zero=args.on_zero))
    return 0


def _cmd_clean_columns(args: argparse.Namespace) -> int:
    # accepts a comma-separated string
    cols = [c.strip() for c in args.columns.split(",") if c.strip()]
    print(",".join(clean_columns(cols)))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="demo-elt", description="demo-elt-framework CLI")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    sub = p.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="Add two numbers")
    p_add.add_argument("a", type=float)
    p_add.add_argument("b", type=float)
    p_add.set_defaults(func=_cmd_add)

    p_sub = sub.add_parser("subtract", help="Subtract two numbers (a - b)")
    p_sub.add_argument("a", type=float)
    p_sub.add_argument("b", type=float)
    p_sub.set_defaults(func=_cmd_subtract)

    p_div = sub.add_parser("divide", help="Divide two numbers (a / b)")
    p_div.add_argument("a", type=float)
    p_div.add_argument("b", type=float)
    p_div.add_argument("--on-zero", default="raise", choices=["raise", "inf", "nan"])
    p_div.set_defaults(func=_cmd_divide)

    p_tx = sub.add_parser("transform", help="Transform utilities")
    tx_sub = p_tx.add_subparsers(dest="transform", required=True)

    p_cc = tx_sub.add_parser("clean-columns", help="Normalize comma-separated column names")
    p_cc.add_argument("columns", help='Comma-separated columns, e.g. "First Name, City"')
    p_cc.set_defaults(func=_cmd_clean_columns)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

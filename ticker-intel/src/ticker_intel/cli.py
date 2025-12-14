import argparse

def main() -> None:
    parser = argparse.ArgumentParser(prog="ticker-intel", description="Ticker Intel CLI")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    args = parser.parse_args()

    if args.version:
        print("0.1.1")
        return

from shadowdark_tui.core.models import RollRequest
from shadowdark_tui.core.engine import apply_rules
import argparse

def main():
    parser = argparse.ArgumentParser(description="Shadowdark roll demo")
    parser.add_argument("--advantage", action="store_true")
    parser.add_argument("--disadvantage", action="store_true")
    args = parser.parse_args()

    req = RollRequest(base_die=20, advantage=args.advantage, disadvantage=args.disadvantage, tags=["demo"])
    res = apply_rules(req)
    print(f"Rolled: {res.total}  detail={res.detail}  rules={[r.id for r in res.applied_rules]}")

if __name__ == "__main__":
    main()

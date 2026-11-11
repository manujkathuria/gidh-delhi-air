"""Delhi air quality evidence verification."""


def main() -> None:
    from gidh_delhi_air.verify import main as verify_main
    raise SystemExit(verify_main())

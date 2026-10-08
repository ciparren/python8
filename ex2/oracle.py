#!/usr/bin/env python3

import os
import sys

from dotenv import load_dotenv

KEYS: list[str] = [
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
]


def load_config() -> dict[str, str]:
    """Load .env (real env vars win) and return the 5 settings.
    A missing setting becomes an empty string."""
    load_dotenv()
    config: dict[str, str] = {}
    for key in KEYS:
        config[key] = os.getenv(key, "")
    return config


def check_missing(config: dict[str, str]) -> None:
    """Warn about missing settings and apply simple defaults."""
    for key in KEYS:
        if config[key] == "":
            print(f"[WARNING] {key} is missing")

    if config["MATRIX_MODE"] not in ("development", "production"):
        if config["MATRIX_MODE"] != "":
            print(f"[WARNING] Invalid MATRIX_MODE: {config['MATRIX_MODE']}")
        config["MATRIX_MODE"] = "development"

    if config["LOG_LEVEL"] == "":
        if config["MATRIX_MODE"] == "production":
            config["LOG_LEVEL"] = "WARNING"
        else:
            config["LOG_LEVEL"] = "DEBUG"

    if config["MATRIX_MODE"] == "production" and config["API_KEY"] == "":
        print("[ERROR] API_KEY is required in production")
        sys.exit(1)


def print_config(config: dict[str, str]) -> None:
    production = config["MATRIX_MODE"] == "production"

    if config["DATABASE_URL"] == "":
        database = "Not configured"
    elif production:
        database = "Connected to production database"
    else:
        database = "Connected to local instance"

    api = "Authenticated" if config["API_KEY"] != "" else "Missing"
    zion = "Online" if config["ZION_ENDPOINT"] != "" else "Offline"

    print("\nConfiguration loaded:")
    print(f"Mode: {config['MATRIX_MODE']}")
    print(f"Database: {database}")
    print(f"API Access: {api}")
    print(f"Log Level: {config['LOG_LEVEL']}")
    print(f"Zion Network: {zion}")


def has_hardcoded_secret(config: dict[str, str]) -> bool:
    """True if the real API_KEY value appears inside this source file."""
    secret = config["API_KEY"]
    if secret == "":
        return False
    with open(__file__) as f:
        return secret in f.read()


def env_ignored_by_git() -> bool:
    """True if .gitignore has a line that is exactly '.env'."""
    if not os.path.exists(".gitignore"):
        return False
    with open(".gitignore") as f:
        return ".env" in [line.strip() for line in f]


def security_check(config: dict[str, str]) -> None:
    print("\nEnvironment security check:")

    if has_hardcoded_secret(config):
        print("[WARNING] Hardcoded secret found in oracle.py")
    else:
        print("[OK] No hardcoded secrets detected")

    if os.path.exists(".env") and env_ignored_by_git():
        print("[OK] .env file properly configured")
    elif not os.path.exists(".env"):
        print("[WARNING] .env file not found (copy .env.example)")
    else:
        print("[WARNING] .env is not listed in .gitignore")

    # load_dotenv() does not override real env vars, so they always win.
    print("[OK] Production overrides available")


def main() -> None:
    print("ORACLE STATUS: Reading the Matrix...")
    config = load_config()
    check_missing(config)
    print_config(config)
    security_check(config)
    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3

import os
import site
import sys


def is_virtual_env() -> bool:
    return sys.prefix != sys.base_prefix


def get_site_packages() -> str:
    try:
        return site.getsitepackages()[0]
    except (AttributeError, IndexError):
        return "unavailable in this environment"


def print_global_env() -> None:
    print("\nMATRIX STATUS: You're still plugged in")
    print(f"\nCurrent Python: {sys.executable}"
          "\nVirtual Environment: None detected")
    print("\nWARNING: You're in the global environment!"
          "\nThe machines can see everything you install.")
    print("\nTo enter the construct, run:"
          "\npython3 -m venv matrix_env"
          "\nsource matrix_env/bin/activate  # On Unix"
          "\nmatrix_env\\Scripts\\activate  # On Windows"
          "\n\nThen run this program again.")


def print_virtual_env() -> None:
    env_path = sys.prefix
    print("\nMATRIX STATUS: Welcome to the construct")
    print(f"\nCurrent Python: {sys.executable}"
          f"\nVirtual Environment: {os.path.basename(env_path)}"
          f"\nEnvironment Path: {env_path}")
    print("\nSUCCESS: You're in an isolated environment!"
          "\nSafe to install packages without affecting"
          "\nthe global system.")
    print("\nPackage installation path:"
          f"\n{get_site_packages()}")


def main() -> None:
    if is_virtual_env():
        print_virtual_env()
    else:
        print_global_env()


if __name__ == "__main__":
    main()
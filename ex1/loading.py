#!/usr/bin/env python3

import sys
from importlib import import_module, metadata
from types import ModuleType
from typing import Any


REQUIRED: dict[str, str] = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computation ready",
    "matplotlib": "Visualization ready",
}

DATA_POINTS: int = 1000
OUTPUT_FILE: str = "matrix_analysis.png"
SEED: int = 42


def get_version(name: str) -> str:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return "unknown"


def check_dependencies() -> tuple[dict[str, ModuleType], list[str]]:
    modules: dict[str, ModuleType] = {}
    missing: list[str] = []
    for name in REQUIRED:
        try:
            modules[name] = import_module(name)
        except ImportError:
            missing.append(name)
    return modules, missing


def print_dependency_status(modules: dict[str, ModuleType]) -> None:
    print("\nChecking dependencies:")
    for name, description in REQUIRED.items():
        if name in modules:
            print(f"[OK] {name} ({get_version(name)}) - {description}")
        else:
            print(f"[MISSING] {name} - not installed")


def print_install_help(missing: list[str]) -> None:
    """Explain how to install the missing packages with pip and Poetry."""
    print("\nERROR: missing dependencies: " + ", ".join(missing))
    print("\nOption 1 - pip (inside a virtual environment):")
    print("  python3 -m venv matrix_env")
    print("  source matrix_env/bin/activate")
    print("  pip install -r requirements.txt")
    print("  python3 loading.py")
    print("\nOption 2 - Poetry:")
    print("  poetry install")
    print("  poetry run python loading.py")
    print("\nNote: on Ubuntu, pip refuses to install packages outside a"
          "\nvirtual environment (PEP 668), so create one first.")


def show_versions(modules: dict[str, ModuleType]) -> None:
    """Función de comparación de versiones instaladas."""
    # TODO: mostrar versión instalada de cada paquete cargado
    # TODO (opcional): comparar con la versión que pide requirements.txt
    pass


def compare_pip_poetry() -> None:
    """Show the main differences between pip and Poetry."""
    print("\npip vs Poetry:")
    print("  Dependency file : requirements.txt | pyproject.toml")
    print("  Exact versions  : not recorded     | poetry.lock")
    print("  Virtual env     : you create it    | Poetry manages it")
    print("  Install         : pip install -r   | poetry install")
    print("  Run             : python3 file.py  | poetry run python file.py")


def generate_and_analyze(modules: dict[str, ModuleType]) -> Any:
    """Generate the Matrix data with numpy and analyze it with pandas."""
    np = modules["numpy"]
    pd = modules["pandas"]

    print("\nAnalyzing Matrix data...")
    rng = np.random.default_rng(SEED)
    df = pd.DataFrame({"value": rng.integers(0, 100, DATA_POINTS)})
    df["even"] = df["value"] % 2 == 0

    print(f"Processing {len(df)} data points...")
    return df


def plot_data(modules: dict[str, ModuleType], df: Any, path: str) -> None:
    """Draw how many values are even and odd, and save it as a PNG."""
    modules["matplotlib"].use("Agg")
    plt = import_module("matplotlib.pyplot")

    evens = int(df["even"].sum())
    odds = len(df) - evens
    plt.bar(["even", "odd"], [evens, odds])
    plt.title("Matrix data: even vs odd")
    plt.ylabel("count")
    plt.savefig(path)
    plt.close()


def main() -> None:
    print("\nLOADING STATUS: Loading programs...")
    modules, missing = check_dependencies()
    print_dependency_status(modules)
    if missing:
        print_install_help(missing)
        compare_pip_poetry()
        sys.exit(1)

    df = generate_and_analyze(modules)
    print("Generating visualization...")
    plot_data(modules, df, OUTPUT_FILE)

    print("\nAnalysis complete!")
    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
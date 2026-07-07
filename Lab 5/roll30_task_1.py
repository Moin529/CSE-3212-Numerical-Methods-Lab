import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUTPUT_DIR = Path(__file__).resolve().parent / "output1"
OUTPUT_DIR.mkdir(exist_ok=True)


def f(t, y):
    return (1 + 4 * t) - y


def exact_solution(t):
    return 4 * t - 3 + 4 * np.exp(-t)


def solve_method(method, t0, y0, t_end, h):
    n = int(round((t_end - t0) / h))
    t_values = np.linspace(t0, t_end, n + 1)
    h_eff = t_values[1] - t_values[0]
    y_values = np.empty_like(t_values, dtype=float)
    y_values[0] = y0

    for i in range(len(t_values) - 1):
        ti = t_values[i]
        yi = y_values[i]
        if method == "Euler":
            y_values[i + 1] = yi + h_eff * f(ti, yi)
        elif method == "Heun":
            k1 = f(ti, yi)
            predictor = yi + h_eff * k1
            k2 = f(ti + h_eff, predictor)
            y_values[i + 1] = yi + 0.5 * h_eff * (k1 + k2)
        elif method == "Midpoint":
            k1 = f(ti, yi)
            midpoint_y = yi + 0.5 * h_eff * k1
            y_values[i + 1] = yi + h_eff * f(ti + 0.5 * h_eff, midpoint_y)
        else:
            raise ValueError(f"Unknown method: {method}")

    return t_values, y_values


def select_display_points(t_values):
    targets = np.arange(0.0, 5.0 + 0.5e-12, 0.5)
    indices = []
    for target in targets:
        idx = int(np.argmin(np.abs(t_values - target)))
        if np.isclose(t_values[idx], target, atol=1e-9):
            indices.append(idx)
    return indices


def write_table(method, h, t_values, y_num):
    exact_vals = exact_solution(t_values)
    errors = np.abs(exact_vals - y_num)
    csv_path = OUTPUT_DIR / f"task1_{method.lower()}_h{h:.3f}.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["t", "y_numerical", "y_exact", "abs_error"])
        for t, yn, ye, err in zip(t_values, y_num, exact_vals, errors):
            writer.writerow([f"{t:.6f}", f"{yn:.6f}", f"{ye:.6f}", f"{err:.6f}"])

    display_indices = select_display_points(t_values)
    display_t = t_values[display_indices]
    display_y_num = y_num[display_indices]
    display_exact = exact_vals[display_indices]
    display_errors = errors[display_indices]

    print(f"\n=== {method} with h = {h} ===")
    print(f"{'t':>10} {'y_numerical':>14} {'y_exact':>14} {'abs_error':>14}")
    for t, yn, ye, err in zip(display_t, display_y_num, display_exact, display_errors):
        print(f"{t:10.6f} {yn:14.6f} {ye:14.6f} {err:14.6f}")


def main():
    t0 = 0.0
    y0 = 1.0
    t_end = 5.0
    step_sizes = [0.50, 0.25, 0.10, 0.01, 0.001]
    methods = ["Euler", "Heun", "Midpoint"]

    for method in methods:
        for h in step_sizes:
            t_values, y_num = solve_method(method, t0, y0, t_end, h)
            write_table(method, h, t_values, y_num)

    fig, ax = plt.subplots(figsize=(12, 7))
    t_exact = np.linspace(t0, t_end, 1000)
    y_exact = exact_solution(t_exact)
    ax.plot(t_exact, y_exact, color="black", linewidth=2.2, label="Exact")

    styles = {"Euler": "-", "Heun": "--", "Midpoint": ":"}
    palette = [
        "tab:blue",
        "tab:orange",
        "tab:green",
        "tab:red",
        "tab:purple",
        "tab:brown",
        "tab:pink",
        "tab:gray",
        "tab:olive",
        "tab:cyan",
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
    ]

    series_index = 0
    for method in methods:
        for h in step_sizes:
            t_values, y_num = solve_method(method, t0, y0, t_end, h)
            ax.plot(
                t_values,
                y_num,
                linestyle=styles[method],
                color=palette[series_index % len(palette)],
                linewidth=1.4,
                label=f"{method} (h={h})",
            )
            series_index += 1

    ax.set_title("Numerical solutions for dy/dt = (1 + 4t) - y")
    ax.set_xlabel("t")
    ax.set_ylabel("y(t)")
    ax.grid(True, alpha=0.35)
    plt.xlim(0, 2)
    plt.ylim(0, 5)
    ax.legend(loc="best", fontsize=8)
    plt.tight_layout()
    plot_path = OUTPUT_DIR / "task1_combined_plot.png"
    plt.savefig(plot_path, dpi=300)
    plt.show()
    print(f"\nSaved plot to {plot_path}")


if __name__ == "__main__":
    main()

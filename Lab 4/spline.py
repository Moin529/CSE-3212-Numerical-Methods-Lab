import csv
import numpy as np
import matplotlib.pyplot as plt

# =========================
# Read Dataset
# =========================
x = []
y = []

with open("fuel_crisis_data.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        x.append(float(row[0]))
        y.append(float(row[1]))

x = np.array(x)
y = np.array(y)

x_star = 10.5

# =========================
# LINEAR SPLINE
# =========================
def linear_spline(x_data, y_data, x_value):
    for i in range(len(x_data) - 1):
        if x_data[i] <= x_value <= x_data[i + 1]:
            h = x_data[i + 1] - x_data[i]
            a = y_data[i]
            b = (y_data[i + 1] - y_data[i]) / h
            return a + b * (x_value - x_data[i])

def print_linear_table(x, y):
    print("\n===== LINEAR SPLINE TABLE =====")
    for i in range(len(x) - 1):
        h = x[i + 1] - x[i]
        a = y[i]
        b = (y[i + 1] - y[i]) / h
        print(f"[{x[i]}, {x[i+1]}], {a:.6f}, {b:.6f}")

# =========================
# QUADRATIC SPLINE
# =========================
def quadratic_coefficients(x, y):
    n = len(x)
    a = y.copy()
    b = np.zeros(n - 1)
    c = np.zeros(n - 1)
    c[0] = 0

    for i in range(n - 1):
        h = x[i + 1] - x[i]
        if i == 0:
            b[i] = (a[i + 1] - a[i]) / h
        else:
            b[i] = b[i - 1] + 2 * c[i - 1] * (x[i] - x[i - 1])

        c[i] = (a[i + 1] - a[i] - b[i] * h) / (h * h)

    return a, b, c


def quadratic_spline(x_data, coeffs, x_value):
    a, b, c = coeffs
    for i in range(len(x_data) - 1):
        if x_data[i] <= x_value <= x_data[i + 1]:
            dx = x_value - x_data[i]
            return a[i] + b[i] * dx + c[i] * dx * dx


def print_quadratic_table(x, coeffs):
    a, b, c = coeffs
    print("\n===== QUADRATIC SPLINE TABLE =====")
    for i in range(len(x) - 1):
        print(f"[{x[i]}, {x[i+1]}], {a[i]:.6f}, {b[i]:.6f}, {c[i]:.6f}")

# =========================
# CUBIC SPLINE
# =========================
def cubic_spline_coefficients(x, y):
    n = len(x)
    a = y.copy()

    h = np.zeros(n - 1)
    for i in range(n - 1):
        h[i] = x[i + 1] - x[i]

    alpha = np.zeros(n)
    for i in range(1, n - 1):
        alpha[i] = (
            3 / h[i] * (a[i + 1] - a[i])
            - 3 / h[i - 1] * (a[i] - a[i - 1])
        )

    l = np.ones(n)
    mu = np.zeros(n)
    z = np.zeros(n)

    for i in range(1, n - 1):
        l[i] = 2 * (x[i + 1] - x[i - 1]) - h[i - 1] * mu[i - 1]
        mu[i] = h[i] / l[i]
        z[i] = (alpha[i] - h[i - 1] * z[i - 1]) / l[i]

    c = np.zeros(n)
    b = np.zeros(n - 1)
    d = np.zeros(n - 1)

    for j in range(n - 2, -1, -1):
        c[j] = z[j] - mu[j] * c[j + 1]
        b[j] = (a[j + 1] - a[j]) / h[j] - h[j] * (c[j + 1] + 2 * c[j]) / 3
        d[j] = (c[j + 1] - c[j]) / (3 * h[j])

    return a, b, c, d


def cubic_spline(x_data, coeffs, x_value):
    a, b, c, d = coeffs
    for i in range(len(x_data) - 1):
        if x_data[i] <= x_value <= x_data[i + 1]:
            dx = x_value - x_data[i]
            return a[i] + b[i] * dx + c[i] * dx**2 + d[i] * dx**3


def print_cubic_table(x, coeffs):
    a, b, c, d = coeffs
    print("\n===== CUBIC SPLINE TABLE =====")
    for i in range(len(x) - 1):
        print(f"[{x[i]}, {x[i+1]}], {a[i]:.6f}, {b[i]:.6f}, {c[i]:.6f}, {d[i]:.6f}")

# =========================
# COMPUTE COEFFICIENTS
# =========================
quad_coeffs = quadratic_coefficients(x, y)
cubic_coeffs = cubic_spline_coefficients(x, y)

# =========================
# PRINT TABLES
# =========================
print_linear_table(x, y)
print_quadratic_table(x, quad_coeffs)
print_cubic_table(x, cubic_coeffs)

# =========================
# INTERPOLATION VALUES
# =========================
linear_value = linear_spline(x, y, x_star)
quadratic_value = quadratic_spline(x, quad_coeffs, x_star)
cubic_value = cubic_spline(x, cubic_coeffs, x_star)

print("\n===== SPLINE INTERPOLATION =====\n")
print(f"x* = {x_star}")
print(f"Linear Spline    = {linear_value:.6f}")
print(f"Quadratic Spline = {quadratic_value:.6f}")
print(f"Cubic Spline     = {cubic_value:.6f}")

# =========================
# PLOT
# =========================
x_plot = np.linspace(min(x), max(x), 1000)

plt.figure(figsize=(12, 7))
plt.scatter(x, y, color="black", label="Data")

plt.plot(x_plot, [linear_spline(x, y, xp) for xp in x_plot], label="Linear")
plt.plot(x_plot, [quadratic_spline(x, quad_coeffs, xp) for xp in x_plot], label="Quadratic")
plt.plot(x_plot, [cubic_spline(x, cubic_coeffs, xp) for xp in x_plot], label="Cubic")

plt.scatter([x_star], [cubic_value], s=100, label="x*")

plt.xlabel("Day")
plt.ylabel("Fuel Demand")
plt.title("Spline Interpolation")
plt.legend()
plt.grid()

plt.savefig("spline_interpolation_plot.png", dpi=300, bbox_inches="tight")
plt.show()

print("\nGraph saved as spline_interpolation_plot.png")
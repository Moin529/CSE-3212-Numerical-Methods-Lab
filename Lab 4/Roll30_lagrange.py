import csv
import numpy as np
import matplotlib.pyplot as plt

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

def lagrange_interpolation(x_points, y_points, x_value):

    n = len(x_points)

    result = 0

    for i in range(n):

        term = y_points[i]

        for j in range(n):

            if i != j:
                term *= (x_value - x_points[j]) / (x_points[i] - x_points[j])

        result += term

    return result

x_star = 10.5

degrees = [2, 3, 4, 5]

results = []

print("\n===== LAGRANGE INTERPOLATION =====\n")

for degree in degrees:

    center = np.searchsorted(x, x_star)

    start = max(0, center - degree // 2)
    end = start + degree + 1

    if end > len(x):
        end = len(x)
        start = end - degree - 1

    x_nodes = x[start:end]
    y_nodes = y[start:end]

    interpolated_value = lagrange_interpolation(
        x_nodes,
        y_nodes,
        x_star
    )

    results.append(interpolated_value)

    print(f"Degree {degree} Polynomial")

    print("Selected Nodes:")

    for xi, yi in zip(x_nodes, y_nodes):
        print(f"({xi}, {yi})")

    print(f"P{degree}({x_star}) = {interpolated_value:.6f}")

    if len(results) > 1:
        delta = abs(results[-1] - results[-2])
        print(f"Delta = {delta:.6f}")

    print("-" * 40)

x_plot = np.linspace(min(x), max(x), 500)

plt.figure(figsize=(10, 6))

plt.scatter(x, y, color='red', label='Original Data')

for degree in degrees:

    curve = []

    center = np.searchsorted(x, x_star)

    start = max(0, center - degree // 2)
    end = start + degree + 1

    if end > len(x):
        end = len(x)
        start = end - degree - 1

    x_nodes = x[start:end]
    y_nodes = y[start:end]

    for xp in x_plot:
        curve.append(
            lagrange_interpolation(
                x_nodes,
                y_nodes,
                xp
            )
        )

    plt.plot(x_plot, curve, label=f'Degree {degree}')

plt.scatter(
    x_star,
    results[-1],
    color='black',
    s=100,
    label='Interpolated Point'
)

plt.xlabel("Day")
plt.ylabel("Fuel Demand")
plt.title("Lagrange Interpolation - Fuel Crisis")
plt.legend()
plt.grid(True)

plt.savefig(
    "lagrange_interpolation_plot.png",
    dpi=300,
    bbox_inches='tight'
)

print("\nPlot saved as 'lagrange_interpolation_plot.png'")

plt.show()
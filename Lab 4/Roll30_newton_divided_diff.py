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

def divided_difference(x_values, y_values):

    n = len(y_values)

    table = np.zeros((n, n))

    for i in range(n):
        table[i][0] = y_values[i]

    for j in range(1, n):

        for i in range(n - j):

            table[i][j] = (
                table[i + 1][j - 1] - table[i][j - 1]
            ) / (x_values[i + j] - x_values[i])

    return table

def newton_interpolation(x_values, table, x_value):

    n = len(x_values)

    result = table[0][0]

    product_term = 1

    for i in range(1, n):

        product_term *= (x_value - x_values[i - 1])

        result += table[0][i] * product_term

    return result

x_star = 10.5

degrees = [2, 3, 4, 5]

results = []

print("\n===== NEWTON DIVIDED DIFFERENCE =====\n")

for degree in degrees:

    center = np.searchsorted(x, x_star)

    start = max(0, center - degree // 2)
    end = start + degree + 1

    if end > len(x):
        end = len(x)
        start = end - degree - 1

    x_nodes = x[start:end]
    y_nodes = y[start:end]

    table = divided_difference(
        x_nodes,
        y_nodes
    )

    interpolated_value = newton_interpolation(
        x_nodes,
        table,
        x_star
    )

    results.append(interpolated_value)

    print(f"\nDegree {degree} Polynomial")

    print("\nDivided Difference Table:\n")

    n = len(x_nodes)

    for i in range(n):

        for j in range(n - i):
            print(f"{table[i][j]:12.6f}", end=" ")

        print()

    print(f"\nN{degree}({x_star}) = {interpolated_value:.6f}")

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

    table = divided_difference(
        x_nodes,
        y_nodes
    )

    for xp in x_plot:

        curve.append(
            newton_interpolation(
                x_nodes,
                table,
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
plt.title("Newton Divided Difference - Fuel Crisis")
plt.legend()
plt.grid(True)

plt.savefig(
    "newton_divided_difference_plot.png",
    dpi=300,
    bbox_inches='tight'
)

print("\nPlot saved as 'newton_divided_difference_plot.png'")

plt.show()
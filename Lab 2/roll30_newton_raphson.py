import math
import matplotlib.pyplot as plt

Kp = 1.2

def f(x):
    return Kp - (x**2/(1-x)**2)*math.exp(-8*x) + math.log(1+x)

def df(x):
    term1 = ((2*x*(1-x)**2 + 2*x**2*(1-x)) / (1-x)**4) * math.exp(-8*x)
    term2 = (8*x**2/(1-x)**2) * math.exp(-8*x)
    return -(term1 - term2) + 1/(1+x)

x0 = -0.5
es = 0.00001

iteration = 0
errors = []
iterations = []

print("Iter\t xk\t\t f(xk)\t\t f'(xk)\t\t ea(%)")

while True:

    iteration += 1
    fx = f(x0)
    dfx = df(x0)

    if dfx == 0:
        print("Derivative became zero. Stopping.")
        break

    x1 = x0 - fx/dfx

    if x1 <= -1 or x1 >= 1:
        print("Iteration left valid range (0,1). Stopping.")
        break

    ea = abs((x1 - x0) / x1) * 100
    print(f"{iteration}\t{x1:.6f}\t{f(x1):.6f}\t{df(x1):.6f}\t{ea:.6f}")

    errors.append(ea)
    iterations.append(iteration)

    if ea <= es:
        root = x1
        break

    x0 = x1

print("\nApproximate Root =", round(root, 6))

plt.plot(iterations, errors, marker='o')
plt.xlabel("Iteration Number")
plt.ylabel("Approximate Error (%)")
plt.title("Newton-Raphson Convergence")
plt.grid(True)
plt.savefig("newton_raphson_plot.png", dpi=300)
plt.show()
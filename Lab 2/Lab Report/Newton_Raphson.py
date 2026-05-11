import math
import matplotlib.pyplot as plt

def f(h):
    return h**3 - 10*h + 5*math.exp(-h/2) - 2

def df(h):
    return 3*h**2 - 10 - 2.5*math.exp(-h/2)

x0 = 1.5
es = 0.001

iteration = 0
errors = []
iters = []

print("Iter\t x\t\t f(x)\t\t f'(x)\t\t ea(%)")

while True:

    iteration += 1

    x1 = x0 - f(x0)/df(x0)

    ea = abs((x1-x0)/x1)*100

    print(f"{iteration}\t{x1:.5f}\t{f(x1):.5f}\t{df(x1):.5f}\t{ea:.5f}")

    errors.append(ea)
    iters.append(iteration)

    if ea <= es:
        root = x1
        break

    x0 = x1


print("\nRoot =", round(root,5))

plt.plot(iters, errors, marker='o')
plt.xlabel("Iteration")
plt.ylabel("Approximate Error (%)")
plt.title("Newton-Raphson Convergence")
plt.grid()

plt.savefig("newton_raphson.png", dpi=300)
plt.show()
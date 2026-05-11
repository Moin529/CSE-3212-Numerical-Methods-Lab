import math
import matplotlib.pyplot as plt

def f(h):
    return h**3 - 10*h + 5*math.exp(-h/2) - 2

h0 = 1.5
h1 = 2.0
es = 0.001

iteration = 0
errors = []
iters = []

print("Iter\t h\t\t f(h)\t\t ea(%)")

while True:

    iteration += 1

    h2 = h1 - f(h1)*(h1-h0)/(f(h1)-f(h0))

    ea = abs((h2-h1)/h2)*100

    print(f"{iteration}\t{h2:.5f}\t{f(h2):.5f}\t{ea:.5f}")

    errors.append(ea)
    iters.append(iteration)

    if ea <= es:
        root = h2
        break

    h0 = h1
    h1 = h2


print("\nRoot =", round(root,5))

plt.plot(iters, errors, marker='o')
plt.xlabel("Iteration")
plt.ylabel("Approximate Error (%)")
plt.title("Secant Method Convergence")
plt.grid()

plt.savefig("secant.png", dpi=300)
plt.show()
import math
import matplotlib.pyplot as plt

def f(h):
    return h**3 - 10*h + 5*math.exp(-h/2) - 2

xl = 0.1
xu = 0.4
es = 0.001

xr_old = xl
iteration = 0

errors = []
iters = []

print(f"{'Iter':<6}{'xl':<12}{'xu':<12}{'xr':<12}{'f(xr)':<15}{'ea(%)':<10}")

while True:

    iteration += 1
    xr = (xl + xu) / 2

    if iteration > 1:
        ea = abs((xr - xr_old)/xr) * 100
    else:
        ea = 100

    print(f"{iteration:<6}{xl:<12.5f}{xu:<12.5f}{xr:<12.5f}{f(xr):<15.5f}{ea:<10.5f}")

    errors.append(ea)
    iters.append(iteration)

    if f(xl)*f(xr) < 0:
        xu = xr
    else:
        xl = xr

    if ea <= es:
        root = xr
        break

    xr_old = xr


print("\nRoot =", round(root,5))

plt.plot(iters, errors, marker='o')
plt.xlabel("Iteration")
plt.ylabel("Approximate Error (%)")
plt.title("Bisection Convergence")
plt.grid()

plt.savefig("bisection.png", dpi=300)
plt.show()
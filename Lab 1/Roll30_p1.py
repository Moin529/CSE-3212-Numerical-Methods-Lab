import math
import matplotlib.pyplot as plt

def f(x):
    return x**5 - 4*x**3 + 2*x**2 - math.log(x+2) - 1.5


def bisection():

    xl = 0.5
    xu = 2.0
    xr_old = None

    iteration = 0
    max_iter = 100

    n = 5

    tol = 0.5 * 10**(2 - n)

    errors = []
    iters = []

    print("Tolerance =", tol, "%\n")
    print("Iter\t xl\t\t xu\t\t xr\t\t f(xr)\t\t ea(%)")
    print("-" * 80)

    while iteration < max_iter:

        xr = (xl + xu) / 2
        fxr = f(xr)

        if xr_old is None:
            ea = None
        else:
            ea = abs((xr - xr_old) / xr) * 100

        if ea is None:
            ea_display = "N/A"
        else:
            ea_display = f"{ea:.6f}"

        print(f"{iteration+1}\t {xl:.6f}\t {xu:.6f}\t {xr:.6f}\t {fxr:.6f}\t {ea_display}")

        if ea is not None:
            errors.append(ea)
            iters.append(iteration + 1)

            if ea <= tol:
                break

        if f(xl) * fxr < 0:
            xu = xr
        else:
            xl = xr

        xr_old = xr
        iteration += 1

    print("\nApproximate root =", round(xr,6))

    plt.plot(iters, errors, marker='o')
    plt.xlabel("Iteration")
    plt.ylabel("Absolute Error (%)")
    plt.title("Bisection Convergence (Problem 1)")
    plt.grid()

    plt.savefig("problem1_error_plot.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    bisection()
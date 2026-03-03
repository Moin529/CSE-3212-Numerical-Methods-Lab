import math
import matplotlib.pyplot as plt

Q = 1.2
g = 9.81
L = 15

def A(y):
    return 2*y + y**2

def P(y):
    return 2 + 2*math.sqrt(1 + y**2)

def f(y):
    return math.sqrt((2*g)/L) * (A(y)/P(y))**(3/2) - Q/A(y)


def bisection():

    xl = 0.3
    xu = 1.5
    xr_old = None

    iteration = 0
    max_iter = 12

    errors = []
    iters = []

    print("Iter\t xl\t\t xu\t\t xr\t\t f(xr)\t\t ea(%)")
    print("-" * 80)

    while iteration <= max_iter:

        xr = (xl + xu) / 2
        fxr = f(xr)

        if xr_old is None:
            ea = None
        else:
            ea = abs((xr - xr_old)/xr) * 100

        print(f"{iteration+1}\t {xl:.6f}\t {xu:.6f}\t {xr:.6f}\t {fxr:.6f}\t {0 if ea is None else ea:.6f}")

        if ea is not None:
            errors.append(ea)
            iters.append(iteration+1)

            if ea <= 0.5:
                break

        if f(xl) * fxr < 0:
            xu = xr
        else:
            xl = xr

        xr_old = xr
        iteration += 1

    print("\nApproximate flow depth y =", round(xr,6))

    plt.plot(iters, errors, marker='o')
    plt.xlabel("Iteration")
    plt.ylabel("Absolute Error (%)")
    plt.title("Bisection Convergence (Problem 2)")
    plt.grid()

    plt.savefig("problem2_error_plot.png", dpi=300)

    plt.show()


if __name__ == "__main__":
    bisection()
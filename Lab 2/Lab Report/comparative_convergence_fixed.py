import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def f(h):
    return h**3 - 10*h + 5*math.exp(-h/2) - 2


def df(h):
    return 3*h**2 - 10 - 2.5*math.exp(-h/2)


def bisection(xl, xu, es=0.001, max_iter=100):
    xr_old = xl
    errors = []
    iters = []
    for iteration in range(1, max_iter + 1):
        xr = (xl + xu) / 2.0
        ea = abs((xr - xr_old) / xr) * 100 if iteration > 1 else 100.0
        errors.append(ea)
        iters.append(iteration)

        if f(xl) * f(xr) < 0:
            xu = xr
        else:
            xl = xr

        if ea <= es:
            return iters, errors, xr

        xr_old = xr

    raise ValueError("Bisection did not converge within max_iter")


def false_position(xl, xu, es=0.001, max_iter=100):
    xr_old = xl
    errors = []
    iters = []
    for iteration in range(1, max_iter + 1):
        fl = f(xl)
        fu = f(xu)
        xr = (xl * fu - xu * fl) / (fu - fl)
        ea = abs((xr - xr_old) / xr) * 100 if iteration > 1 else 100.0
        errors.append(ea)
        iters.append(iteration)

        if f(xl) * f(xr) < 0:
            xu = xr
        else:
            xl = xr

        if ea <= es:
            return iters, errors, xr

        xr_old = xr

    raise ValueError("False Position did not converge within max_iter")


def newton_raphson(x0, es=0.001, max_iter=100):
    errors = []
    iters = []
    for iteration in range(1, max_iter + 1):
        x1 = x0 - f(x0) / df(x0)
        ea = abs((x1 - x0) / x1) * 100
        errors.append(ea)
        iters.append(iteration)

        if ea <= es:
            return iters, errors, x1

        x0 = x1

    raise ValueError("Newton-Raphson did not converge within max_iter")


def secant(h0, h1, es=0.001, max_iter=100):
    errors = []
    iters = []
    for iteration in range(1, max_iter + 1):
        f0 = f(h0)
        f1 = f(h1)
        h2 = h1 - f1 * (h1 - h0) / (f1 - f0)
        ea = abs((h2 - h1) / h2) * 100
        errors.append(ea)
        iters.append(iteration)

        if ea <= es:
            return iters, errors, h2

        h0, h1 = h1, h2

    raise ValueError("Secant did not converge within max_iter")


def main():
    methods = []

    b_iters, b_errors, b_root = bisection(0.1, 0.4)
    methods.append(("Bisection", b_iters, b_errors, b_root))

    fp_iters, fp_errors, fp_root = false_position(0.1, 0.4)
    methods.append(("False Position", fp_iters, fp_errors, fp_root))

    nr_iters, nr_errors, nr_root = newton_raphson(1.5)
    methods.append(("Newton-Raphson", nr_iters, nr_errors, nr_root))

    s_iters, s_errors, s_root = secant(1.5, 2.0)
    methods.append(("Secant", s_iters, s_errors, s_root))

    plt.figure(figsize=(10, 6))
    for name, iters, errors, root in methods:
        plt.plot(iters, errors, marker='o', label=f"{name} (root ≈ {root:.5f})")

    plt.xlabel('Iteration')
    plt.ylabel('Approximate Error (%)')
    plt.title('Comparative Convergence Analysis: Bisection, False Position, Newton–Raphson, Secant')
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig('comparative_convergence_fixed.png', dpi=300)


if __name__ == '__main__':
    main()

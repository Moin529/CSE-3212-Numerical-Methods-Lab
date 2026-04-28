import math
from itertools import permutations


def read_int(prompt, minimum=None):
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
            if minimum is not None and number < minimum:
                print(f"Error: value must be at least {minimum}.")
                continue
            return number
        except ValueError:
            print("Error: please enter a valid integer.")


def read_float(prompt, positive=False):
    while True:
        value = input(prompt).strip()
        try:
            number = float(value)
            if positive and number <= 0:
                print("Error: value must be greater than 0.")
                continue
            return number
        except ValueError:
            print("Error: please enter a valid real number.")


def read_matrix(n):
    print("Enter coefficient matrix A (row-wise):")
    matrix = []
    for i in range(n):
        while True:
            row_text = input().strip().replace("−", "-")
            parts = row_text.split()
            if len(parts) != n:
                print(f"Error: row {i + 1} must contain exactly {n} values.")
                continue
            try:
                row = [float(value) for value in parts]
                matrix.append(row)
                break
            except ValueError:
                print("Error: enter numeric values only.")
    return matrix


def read_vector(n, prompt):
    print(prompt)
    vector = []
    for i in range(n):
        while True:
            entry = input().strip().replace("−", "-")
            try:
                vector.append(float(entry))
                break
            except ValueError:
                print(f"Error: entry {i + 1} must be a valid real number.")
    return vector


def check_diagonal(matrix):
    for i, row in enumerate(matrix):
        if row[i] == 0:
            raise ValueError(
                f"Division by zero risk: diagonal element a[{i + 1}][{i + 1}] is zero."
            )


def is_diagonally_dominant(matrix):
    strict_row_exists = False
    for i, row in enumerate(matrix):
        diagonal = abs(row[i])
        off_diagonal_sum = sum(abs(row[j]) for j in range(len(row)) if j != i)
        if diagonal < off_diagonal_sum:
            return False
        if diagonal > off_diagonal_sum:
            strict_row_exists = True
    return strict_row_exists


def mat_vec_mul(matrix, vector):
    return [sum(matrix[i][j] * vector[j] for j in range(len(vector))) for i in range(len(matrix))]


def vec_sub(a, b):
    return [a[i] - b[i] for i in range(len(a))]


def norm2(vector):
    return math.sqrt(sum(value * value for value in vector))


def max_abs(vector):
    return max(abs(value) for value in vector)

def rearrange_rows(A, b, n):
    all_orders = permutations(range(n))

    for order in all_orders:

        new_A = []
        new_b = []

        for row_index in order:
            new_A.append(A[row_index])
            new_b.append(b[row_index])

        valid = True

        for i in range(n):
            if new_A[i][i] == 0:
                valid = False
                break

        if valid:
            return new_A, new_b, True

    return A, b, False


def jacobi_method(matrix, constants, initial_guess, max_iterations, tolerance):
    n = len(matrix)
    current = initial_guess[:]
    history = []

    for iteration in range(1, max_iterations + 1):
        next_values = [0.0] * n
        for i in range(n):
            sigma = sum(matrix[i][j] * current[j] for j in range(n) if j != i)
            next_values[i] = (constants[i] - sigma) / matrix[i][i]

        abs_errors = [abs(next_values[i] - current[i]) for i in range(n)]
        residual = norm2(vec_sub(mat_vec_mul(matrix, next_values), constants))
        history.append(
            {
                "iteration": iteration,
                "x": next_values[:],
                "abs_errors": abs_errors,
                "residual": residual,
            }
        )

        if max_abs(abs_errors) < tolerance and residual < tolerance:
            return {
                "method": "Jacobi",
                "solution": next_values,
                "iterations": iteration,
                "converged": True,
                "history": history,
            }

        current = next_values

    return {
        "method": "Jacobi",
        "solution": current,
        "iterations": max_iterations,
        "converged": False,
        "history": history,
    }


def gauss_seidel_method(matrix, constants, initial_guess, max_iterations, tolerance):
    n = len(matrix)
    current = initial_guess[:]
    history = []

    for iteration in range(1, max_iterations + 1):
        previous = current[:]
        for i in range(n):
            left_sum = sum(matrix[i][j] * current[j] for j in range(i))
            right_sum = sum(matrix[i][j] * previous[j] for j in range(i + 1, n))
            current[i] = (constants[i] - left_sum - right_sum) / matrix[i][i]

        abs_errors = [abs(current[i] - previous[i]) for i in range(n)]
        residual = norm2(vec_sub(mat_vec_mul(matrix, current), constants))
        history.append(
            {
                "iteration": iteration,
                "x": current[:],
                "abs_errors": abs_errors,
                "residual": residual,
            }
        )

        if max_abs(abs_errors) < tolerance and residual < tolerance:
            return {
                "method": "Gauss-Seidel",
                "solution": current[:],
                "iterations": iteration,
                "converged": True,
                "history": history,
            }

    return {
        "method": "Gauss-Seidel",
        "solution": current[:],
        "iterations": max_iterations,
        "converged": False,
        "history": history,
    }


def estimate_convergence_rate(history):
    residuals = [entry["residual"] for entry in history if entry["residual"] > 0]
    if len(residuals) < 2:
        return None

    ratios = []
    for i in range(1, len(residuals)):
        if residuals[i - 1] != 0:
            ratios.append(residuals[i] / residuals[i - 1])

    if not ratios:
        return None
    return sum(ratios) / len(ratios)


def format_vector(vector):
    lines = ["["]
    for value in vector:
        lines.append(f"  {value:12.6f}")
    lines.append("]")
    return "\n".join(lines)


def print_iteration_table(result):
    print(f"\n{result['method']} Iteration Details")
    print("-" * 78)
    for entry in result["history"]:
        x_values = "  ".join(f"x{i + 1} = {value:.6f}" for i, value in enumerate(entry["x"]))
        errors = "  ".join(
            f"|e{i + 1}| = {value:.6e}" for i, value in enumerate(entry["abs_errors"])
        )
        print(
            f"Iteration {entry['iteration']:>2}: {x_values}\n"
            f"              {errors}\n"
            f"              Residual ||Ax-b||2 = {entry['residual']:.6f}"
        )
    print("-" * 78)


def print_result_summary(result):
    print(f"\n{result['method']} Method Result")
    print(f"Convergence status: {'Converged' if result['converged'] else 'Did not converge'}")
    print(f"Solution vector x*:\n{format_vector(result['solution'])}")
    print(f"Iterations used: {result['iterations']}")
    if result["history"]:
        print(f"Final residual ||Ax-b||2: {result['history'][-1]['residual']:.6f}")
    if not result["converged"]:
        print("Warning: maximum iterations reached before convergence.")


def compare_methods(jacobi_result, gauss_seidel_result):
    jacobi_rate = estimate_convergence_rate(jacobi_result["history"])
    gs_rate = estimate_convergence_rate(gauss_seidel_result["history"])

    print("\nConvergence Behavior Comparison")
    print("-" * 78)
    print(
        f"Iteration count comparison: Jacobi = {jacobi_result['iterations']}, "
        f"Gauss-Seidel = {gauss_seidel_result['iterations']}"
    )

    if jacobi_rate is None:
        print("Jacobi convergence rate analysis: insufficient data to estimate residual ratio.")
    else:
        print(f"Jacobi convergence rate analysis: average residual ratio = {jacobi_rate:.6f}")

    if gs_rate is None:
        print("Gauss-Seidel convergence rate analysis: insufficient data to estimate residual ratio.")
    else:
        print(f"Gauss-Seidel convergence rate analysis: average residual ratio = {gs_rate:.6f}")

    if jacobi_result["converged"] and gauss_seidel_result["converged"]:
        if jacobi_result["iterations"] < gauss_seidel_result["iterations"]:
            faster = "Jacobi"
        elif gauss_seidel_result["iterations"] < jacobi_result["iterations"]:
            faster = "Gauss-Seidel"
        else:
            faster = "Both methods required the same number of iterations"

        if faster.startswith("Both"):
            print("Computational efficiency remarks: both methods were equally efficient in iteration count.")
        else:
            print(
                f"Computational efficiency remarks: {faster} was more efficient for this system "
                "because it reached the tolerance in fewer iterations."
            )
    elif gauss_seidel_result["converged"] and not jacobi_result["converged"]:
        print("Computational efficiency remarks: Gauss-Seidel converged while Jacobi did not within Kmax.")
    elif jacobi_result["converged"] and not gauss_seidel_result["converged"]:
        print("Computational efficiency remarks: Jacobi converged while Gauss-Seidel did not within Kmax.")
    else:
        print("Computational efficiency remarks: neither method satisfied the convergence criteria within Kmax.")


def main():
    try:
        n = read_int("Enter number of equations: ", minimum=2)
        matrix = read_matrix(n)
        constants = read_vector(n, "Enter constants vector b:")
        initial_guess = read_vector(n, "Enter initial guess vector:")
        max_iterations = read_int("Enter maximum iterations: ", minimum=1)
        tolerance = read_float("Enter tolerance: ", positive=True)

        original_matrix = [row[:] for row in matrix]
        matrix, constants, rearranged = rearrange_rows(matrix, constants, n)
        if rearranged and matrix != original_matrix:
            print("Notice: rows were rearranged to avoid zero diagonal entries.")

        check_diagonal(matrix)
        if not is_diagonally_dominant(matrix):
            print(
                "Warning: matrix A is not diagonally dominant, so Jacobi and "
                "Gauss-Seidel may not converge."
            )

        jacobi_result = jacobi_method(matrix, constants, initial_guess, max_iterations, tolerance)
        gauss_seidel_result = gauss_seidel_method(
            matrix, constants, initial_guess, max_iterations, tolerance
        )

        print_iteration_table(jacobi_result)
        print_result_summary(jacobi_result)

        print_iteration_table(gauss_seidel_result)
        print_result_summary(gauss_seidel_result)

        compare_methods(jacobi_result, gauss_seidel_result)

    except MemoryError:
        print("Error: system is too large to handle with available memory.")
    except ValueError as error:
        print(f"Error: {error}")
    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()

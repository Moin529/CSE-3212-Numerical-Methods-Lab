import numpy as np
import matplotlib.pyplot as plt

Kp    = 1.2
alpha = -8.0

def f(x):
    if x >= 1.0 or x <= -1.0 or np.isnan(x):
        return float("inf")
    return Kp - (x**2 / (1 - x)**2) * np.exp(alpha * x) + np.log(1 + x)


def secant():
    m0 = -0.3
    m1 = -0.7
    es = 0.00001
    
    iters = []
    ea_values = []
    
    print(f"{'Iter':<5} | {'mk':<15} | {'f(mk)':<15} | {'approx f_prime':<15} | {'ea (%)'}")
    print("-" * 85)
    
    i = 1
    while True:
        f_prime_approx = (f(m1) - f(m0)) / (m1 - m0)
        
        m2 = m1 - f(m1) / f_prime_approx

        ea = abs((m2 - m1) / m2) * 100.0
        
        print(f"{i:<5} | {m1:.10f} | {f(m1):.10f} | {f_prime_approx:.10f} | {ea:.10f}")
        
        iters.append(i)
        ea_values.append(ea)
        
        m0 = m1
        m1 = m2
        
        if ea <= es:
            break
            
        i += 1

    print(f"\n=> The approximate root is: {m0:.10f}")

    plt.figure()
    plt.plot(iters, ea_values, marker='o', linestyle='-', color='g')
    plt.title('Secant Method: Approximate Error vs Iterations')
    plt.xlabel('Number of Iterations')
    plt.ylabel('Approximate Relative Error ea (%)')
    plt.grid(True)
    plt.savefig('secant_plot.png')
    plt.show()

if __name__ == "__main__":
    secant()
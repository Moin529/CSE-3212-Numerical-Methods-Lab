import math
import matplotlib.pyplot as plt

def f(x):
    Kp = 1.2
    alpha = -8.0
    return Kp - ((x**2) / ((1 - x)**2)) * math.exp(alpha * x) + math.log(1 + x)

def false_position():
    xl = -0.999
    xu = 0.0
    es = 0.00001
    xr_old = 0.0
    
    iters = []
    ea_values = []
    
    print(f"{'Iter':<5} | {'xl':<15} | {'xu':<15} | {'xr':<15} | {'f(xr)':<15} | {'ea (%)'}")
    print("-" * 85)
    
    i = 1
    while True:
        xr = (xl * f(xu) - xu * f(xl)) / (f(xu) - f(xl))
        
        if i > 1:
            ea = abs((xr - xr_old) / xr) * 100.0
            ea_str = f"{ea:.10f}"
            ea_values.append(ea)
            iters.append(i)
        else:
            ea = 100.0 
            ea_str = "N/A"
        
        print(f"{i:<5} | {xl:.10f} | {xu:.10f} | {xr:.10f} | {f(xr):.10f} | {ea_str}")
        
        if i > 1 and ea <= es:
            break
            
        if f(xl) * f(xr) < 0:
            xu = xr
        else:
            xl = xr
            
        xr_old = xr
        i += 1

    print(f"\n=> The approximate root is: {xr:.10f}")

    plt.figure()
    plt.plot(iters, ea_values, marker='o', linestyle='-', color='b')
    plt.title('False Position: Approximate Error vs Iterations')
    plt.xlabel('Number of Iterations')
    plt.ylabel('Approximate Relative Error ea (%)')
    plt.grid(True)
    
    plt.savefig('false_position_plot.png')
    print("Plot saved as 'false_position_plot.png'")
    plt.show()

if __name__ == "__main__":
    false_position()
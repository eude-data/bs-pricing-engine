from bs import Call
import numpy as np



tau = 1
K = 10
S = 10
r = 0.0
sigma = 0.2
C = Call(tau, K, S, r, sigma)
Cmodif = Call(tau, K, S, r, sigma/np.sqrt(3))
print("Asiatique, formule fermée      :", C.asian_price)
print("Asiatique, Monte Carlo          :", C.asian_mc())
print("Call européen                   :", C.price)
print("Approximation par la vega       :", C.price - C.vega * sigma * (1 - 1/np.sqrt(3)))
print("Call européen avec sigma/sqrt(3):", Cmodif.price)

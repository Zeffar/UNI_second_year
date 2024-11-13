import numpy as np
import matplotlib.pyplot as plt

def bernoulli(p):
    prob = np.random.random()
    if prob < p:
        return 1
    else:
        return 0

def simuleaza_binomiala(p, numar_simulari):
    X = np.zeros(numar_simulari)
    for i in range(numar_simulari):
        numar_incercari = 0
        for j in range(40):
            numar_incercari = numar_incercari + bernoulli(p)
        X[i] = numar_incercari

    return X

def simuleaza_geometrica(p, numar_simulari):
    X = np.zeros(numar_simulari)
    for i in range(numar_simulari):
        numar_incercari = 0
        while True:
            U = np.random.random()
            numar_incercari += 1
            if U < p:
                break
        X[i] = numar_incercari
    return X


# Parametri
p = 0.5
numar_simulari = 10000

# Simulare
X_geometrica = simuleaza_geometrica(p, numar_simulari)
X_binomiala = simuleaza_binomiala(p, numar_simulari)

# Histogramă
max_val = int(np.max(X_binomiala))
valori = np.arange(1, max_val + 1)
frecvente, _ = np.histogram(X_binomiala, bins=valori, density=True)
plt.bar(valori[:-1], frecvente, width=0.8, align='center')
plt.xlabel('Valori ale lui X')
plt.ylabel('Frecvența relativă')
plt.title(f'Histogramă Geometrică(p={p})')
plt.show()


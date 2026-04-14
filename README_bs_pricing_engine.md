# Black-Scholes Pricing Engine 📈

Implémentation from scratch d'un moteur de pricing d'options vanilles et exotiques sous le modèle de Black-Scholes, avec calcul des grecques et estimation Monte Carlo.

---

## Contenu

### `bs.py` — Classe `Call`

Classe orientée objet encapsulant toute la logique de pricing d'un call européen :

| Méthode / Propriété | Description |
|---|---|
| `.price` | Prix analytique Black-Scholes |
| `.price_approx()` | Approximation ATM : $0.4 \cdot S \cdot \sigma \cdot \sqrt{\tau}$ |
| `.delta` | $\Delta = \mathcal{N}(d_1)$ |
| `.gamma` | $\Gamma = \frac{\mathcal{N}'(d_1)}{S \sigma \sqrt{\tau}}$ |
| `.vega` | $\mathcal{V} = S\sqrt{\tau}\,\mathcal{N}'(d_1)$ |
| `.mc()` | Pricing Monte Carlo vanille (simulation de $S_T$) |
| `.asian_mc()` | Pricing MC d'une option asiatique géométrique (trajectoire discrète) |
| `.asian_price` | Prix analytique de l'option asiatique (formule fermée via $\sigma_G$) |

### `demo_BS.ipynb` — Notebook de démonstration

- Visualisation de $\Delta$ en fonction du spot $S$ pour différentes maturités
- Couverture gamma/vega : portefeuille de deux calls
- Delta de Malliavin vs différences finies (estimation Monte Carlo de $\Delta$)
- Comparaison prix analytique / Monte Carlo

### `main.py` — Script de test

Comparaison du prix de l'option asiatique par :
- Formule analytique avec $\sigma_G = \sigma / \sqrt{3}$
- Simulation Monte Carlo
- Approximation par développement de vega

---

## Concepts clés

- Modèle de **Black-Scholes** (EDS log-normale sous mesure risque-neutre)
- **Grecques** analytiques : $\Delta$, $\Gamma$, $\mathcal{V}$
- **Options asiatiques** à moyenne géométrique — formule fermée & Monte Carlo
- **Calcul de Malliavin** pour l'estimation de $\Delta$ par simulation

---

## Stack

```python
langages = ["Python"]
librairies = ["numpy", "scipy", "matplotlib"]
```

---

## Usage

```python
from bs import Call

C = Call(tau=1, K=10, S=10, r=0.05, sigma=0.2)

print(C.price)        # Prix analytique
print(C.delta)        # Delta
print(C.mc())         # Estimation Monte Carlo
print(C.asian_price)  # Option asiatique (formule fermée)
```

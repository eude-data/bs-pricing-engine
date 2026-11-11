# Black-Scholes : pricing et grecques

Petit moteur de pricing écrit en Python à partir de zéro, dans le cadre du M2 ISIFAR (Université Paris Cité). Il calcule le prix d'un call européen dans le modèle de Black-Scholes, ses grecques, et le prix d'une option asiatique à moyenne géométrique, par formule fermée et par Monte Carlo.

## Contenu du dépôt

| Fichier | Rôle |
|---|---|
| `bs.py` | Classe `Call` : prix, grecques, Monte Carlo, option asiatique |
| `demo_BS.ipynb` | Notebook de démonstration (graphiques et tests numériques) |
| `main.py` | Comparaison des différents prix de l'option asiatique |

## La classe `Call`

On note τ la maturité résiduelle, K le strike, S le spot, r le taux sans risque et σ la volatilité, avec

$$d_1 = \frac{\ln(S/K) + (r + \sigma^2/2)\tau}{\sigma\sqrt{\tau}}, \qquad d_2 = d_1 - \sigma\sqrt{\tau}$$

| Méthode | Ce qu'elle calcule |
|---|---|
| `price` | Prix de Black-Scholes : S N(d₁) − K e^(−rτ) N(d₂) |
| `delta` | N(d₁) |
| `gamma` | φ(d₁) / (S σ √τ) |
| `vega` | S √τ φ(d₁) |
| `price_approx()` | Approximation à la monnaie 0.4 × S × σ × √τ, valable quand K = S et r proche de 0 |
| `mc()` | Prix par Monte Carlo en simulant directement S(τ) (100 000 tirages par défaut) |
| `asian_price` | Prix de l'asiatique géométrique en temps continu (formule fermée) |
| `asian_mc()` | Prix de la même option par Monte Carlo, moyenne sur 100 pas de temps |

N désigne la fonction de répartition de la loi normale centrée réduite et φ sa densité.

Pour l'option asiatique, la moyenne géométrique reste log-normale. On se ramène donc à une formule de type Black-Scholes avec

$$\sigma_G = \frac{\sigma}{\sqrt{3}}, \qquad b = \frac{1}{2}\left(r - \frac{\sigma_G^2}{2}\right)$$

La formule fermée correspond à une moyenne continue, alors que `asian_mc()` calcule une moyenne discrète sur 100 pas. Un petit écart entre les deux est donc normal.

## Ce que montre le notebook

Paramètres de base : S = K = 10, τ = 1, r = 0, σ = 0.2.

- Prix exact 0.7966 contre 0.80 pour l'approximation 0.4 × S × σ × √τ.
- Courbe du delta en fonction du spot pour six maturités entre 2 mois et 1 an : plus la maturité est courte, plus la transition autour du strike est brutale.
- Grecques d'un portefeuille long d'un call de maturité 2 ans et court d'un call de maturité 0.1 an (même strike, σ = 0.8) : gamma de -0.128 et vega de 3.31. Le portefeuille est donc exposé à la volatilité tout en étant court en gamma.
- Monte Carlo avec 1 000 000 de tirages (r = 0.05, σ = 0.15) : intervalle à 3 écarts-types [0.8559 ; 0.8625].
- Estimation du delta par différences finies (0.6602) et par la formule de Malliavin (0.6571), qui s'écrit

$$\Delta = e^{-rT}\, \mathbb{E}\left[(S_T - K)^+ \frac{W_T}{S_0 \sigma T}\right]$$

## Option asiatique (`main.py`)

Avec les paramètres de base :

| Méthode | Prix |
|---|---|
| Formule fermée | 0.443 |
| Monte Carlo (100 pas) | environ 0.442 |
| Call européen | 0.797 |
| Call européen avec σ/√3 | 0.460 |
| Approximation par la vega | 0.461 |

Les deux dernières lignes montrent qu'on ne retrouve pas le prix de l'asiatique en divisant seulement la volatilité par √3 : il faut aussi corriger le drift.

## Utilisation

```python
from bs import Call

C = Call(tau=1, K=10, S=10, r=0.05, sigma=0.2)

print(C.price)        # prix analytique
print(C.delta)        # delta
print(C.mc())         # estimation Monte Carlo
print(C.asian_price)  # option asiatique, formule fermée
```

Bibliothèques : numpy, scipy, matplotlib.

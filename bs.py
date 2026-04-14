import numpy as np
from scipy.stats import norm

class Call:

    def __init__(self, tau, K, S, r, sigma):
        self.tau = tau
        self.K = K
        self.S = S
        self.r = r
        self.sigma = sigma
        self.d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.tau) / (self.sigma * np.sqrt(self.tau))
        self.d2 = self.d1 - self.sigma * np.sqrt(self.tau)

    @property
    def price(self):
        return self.S * norm.cdf(self.d1) - self.K * np.exp(-self.r * self.tau) * norm.cdf(self.d2)

    @property
    def delta(self):
        return norm.cdf(self.d1)

    @property
    def gamma(self):
        return norm.pdf(self.d1)/(self.S * self.sigma * np.sqrt(self.tau))

    @property
    def vega(self):
        return norm.pdf(self.d1) * self.S * np.sqrt(self.tau)

    def price_approx(self):
        return 0.4 * self.S * self.sigma * np.sqrt(self.tau)

    def mc(self, nb_mc = 100_000) :
        WTs = np.random.normal(0, np.sqrt(self.tau), nb_mc)
        STs = self.S * np.exp((self.r - self.sigma**2/2.) * self.tau + self.sigma * WTs)
        return np.exp(-self.r * self.tau) * np.mean(np.maximum(STs - self.K, 0.))

    def asian_mc(self, nb_mc = 100_000):
        dt = self.tau / 100
        dWts = np.random.normal(0, np.sqrt(dt), (100, nb_mc))
        Wts = np.cumsum(dWts, axis=0)
        print(Wts.shape)
        Wts = np.vstack([np.zeros(nb_mc), Wts])
        ts = np.linspace(0, self.tau, 101)
        Sts = np.hstack([self.S * np.exp((self.r - self.sigma**2/2.)*ts).reshape([101,1]) for _ in range(nb_mc)]) * np.exp(self.sigma * Wts)
        print(Sts.shape)
        ATs = np.exp(np.mean(np.log(Sts), axis=0))
        print(Sts.shape)
        return np.exp(-self.r * self.tau) * np.mean(np.maximum(ATs - self.K, 0.))

    @property
    def asian_price(self):
        sigma_G = self.sigma / np.sqrt(3)
        b = 0.5 * (self.r - 0.5 * sigma_G ** 2)
        numerator_d1 = np.log(self.S / self.K) + (b + 0.5 * sigma_G ** 2) * self.tau
        denominator_d1 = sigma_G * np.sqrt(self.tau)
        d1 = numerator_d1 / denominator_d1
        d2 = d1 - sigma_G * np.sqrt(self.tau)
        return self.S * np.exp((b-self.r)*self.tau) * norm.cdf(d1) - self.K * np.exp(-self.r * self.tau) * norm.cdf(d2)





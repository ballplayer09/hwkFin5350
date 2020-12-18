import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, binom
from typing import Callable
import math


## Payoff functions
def call_payoff(spot, strike):
    return np.maximum(spot - strike, 0.0)

def put_payoff(spot, strike):
    return np.maximum(strike - spot, 0.0)    

## Pricing functions
def european_binomial_pricer(spot: float, strike: float, expiry: float, rate: float, div: float, vol: float, num: int, payoff: Callable) -> float:
    
    h = expiry / num
    # calculate u and d
    u = np.exp((rate - div)*h + vol*np.sqrt(h))
    d = np.exp((rate - div)*h - vol*np.sqrt(h))
    
    # calculate p*
    p_star = (np.exp((rate - div) * h) - d) / (u - d)
    
    # initalize array for the prices of the terminal nodes and calculate option premium
    terminal_spot_prices = np.zeros(num + 1)
    option_premium = 0
    
    for i in range(num+1):
        terminal_spot_prices[i] = spot * (u ** (num - i)) * (d ** i)
        
        option_premium += payoff(terminal_spot_prices[i], strike) * binom.pmf(num-i, num, p_star)
            
    discount_factor = np.exp(-rate * expiry)
        
    option_premium = option_premium * discount_factor

    return option_premium 

def american_binomial_pricer(spot: float, strike: float, expiry: float, rate: float, div: float, vol: float, num: int, payoff: Callable) -> float:
    h = expiry / num
    # calculate u and d
    u = np.exp((rate - div)*h + vol*np.sqrt(h))
    d = np.exp((rate - div)*h - vol*np.sqrt(h))
    
    discount_factor = np.exp(-rate * h)
    
    # calculate p*
    p_star = (np.exp((rate - div) * h) - d) / (u - d)
    
    # initalize array for the prices of the terminal nodes and calculate option premium
    spot_t = np.zeros(num+1)
    option_t = np.zeros(num+1)
    
    for i in range(num+1):
        spot_t[i] = spot * (u ** (num - i)) * (d ** i)
        option_t[i] = payoff(spot_t[i], strike) 

    for i in range((num - 1), -1, -1):
        for j in range(i + 1):
            option_t[j] = discount_factor * ((p_star) * option_t[j] + (1.0 - p_star) * option_t[j+1])
            spot_t[j] /= u
            option_t[j] = np.maximum(option_t[j], payoff(spot_t[j], strike))

    return option_t[0]

def black_scholes_call(spot: float, strike: float, expiry: float, rate: float, div: float, vol: float) -> float:
    d1 = (np.log(spot/strike) + (rate - div + 0.5 * vol * vol) * expiry) / (vol * np.sqrt(expiry))
    d2 = d1 - vol * np.sqrt(expiry) 
    return (spot * np.exp(-div * expiry) * norm.cdf(d1)) - (strike * np.exp(-rate * expiry) * norm.cdf(d2))

def black_scholes_put(spot: float, strike: float, expiry: float, rate: float, div: float, vol: float) -> float:
    d1 = (np.log(spot/strike) + (rate - div + 0.5 * vol * vol) * expiry) / (vol * np.sqrt(expiry))
    d2 = d1 - vol * np.sqrt(expiry) 
    return (strike * np.exp(-rate * expiry) * norm.cdf(-d2)) - (spot * np.exp(-div * expiry) * norm.cdf(-d1))


## Delta
def black_scholes_call_delta(spot: float, strike: float, tau: float, rate: float, div: float, vol: float) -> float:
    d1 = (np.log(spot/strike) + (rate - div + 0.5 * vol * vol) * tau) / (vol * np.sqrt(tau))
    return np.exp(-div * tau) * norm.cdf(d1)


## Simulations
def binomial_path(spot: float, expiry: float, rate: float, div: float, vol: float, num: int) -> np.ndarray:
    # calculate h
    h = expiry / num    
    
    # calculate u and d
    u = np.exp((rate - div)*h + vol*np.sqrt(h))
    d = np.exp((rate - div)*h - vol*np.sqrt(h))
    
    # calculate p*
    p_star = (np.exp((rate - div) * h) - d) / (u - d)
#     print(p_star)
    
    path = binom.rvs(1, p_star, size = num)
    
    prices = np.zeros(num + 1)
    prices[0] = spot
    j = 1
    
    for i in path:        
        if i == 1:
            prices[j] = prices[j-1] * u
        else:
            prices[j] = prices[j-1] * d
        j += 1
    return prices
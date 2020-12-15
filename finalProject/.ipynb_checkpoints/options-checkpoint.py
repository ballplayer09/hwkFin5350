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


# def simulate_prices(u, d, num, spot, strike):

#     stock_prices = {}
#     stock_prices['Period_0'] = np.array([spot])

#     for i in range(1, num+1):
#         previous_prices = stock_prices[f"Period_{i - 1}"]
        
#         temp = []
#         for price in previous_prices:
#             temp.append(price * u)
#             temp.append(price * d)

#         price_result = []

#         stock_prices[f"Period_{i}"] = np.array(price_result)

#     return (stock_prices)
        
   
        
    
#     for i in range(1, num+1):
#         current_period = option_values[f"Period_{i}"]
#         period_premiums = []
        
#         for j in range(len(current_period)-1):
            
#             cu = current_period[j]
#             cd = current_period[j+1]
        
#             delta = (math.e ** (-div * (expiry / num))) * ((cu - cd)/ (spot * (u - d)))
#             b = (math.e ** (-rate * expiry / num)) * ((u * cd - d * cu) / (u - d))
#             premium = delta * spot + b
    
#             period_premiums.append(premium)
        
#         option_premiums[f"Period_{i}"] = np.array(period_premiums)
        
#     return (prices, option_premiums)
    


## Pricing functions
def european_binomial_pricer(spot: float, strike: float, expiry: float, rate: float, div: float, vol: float, num: int, payoff: Callable) -> float:
    
    # calculate u and d
    u = math.e ** ((rate - div) * (expiry / num) + (vol * math.sqrt(expiry / num)))
    d = math.e ** ((rate - div) * (expiry / num) - (vol * math.sqrt(expiry / num)))
    
    # calculate p*
    p_star = (math.e ** ((rate - div) * (expiry / num)) - d) / (u - d)
    
    # initalize array for the prices of the terminal nodes and calculate option premium
    terminal_spot_prices = np.zeros(num+1)
    option_premium = 0
    
    for i in range(num+1):
        terminal_spot_prices[i] = spot * (u ** (num - i)) * (d ** i)
        
        option_premium += payoff(terminal_spot_prices[i], strike) * binom.pmf(num-i, num, p_star)
            
            
    discount_factor = math.e ** (-rate * expiry)
        
    option_premium = option_premium * discount_factor
    
    return option_premium

def american_binomial_pricer(spot: float, strike: float, expiry: float, rate: float, div: float, vol: float, num: int, payoff: Callable) -> float:
    # calculate u and d
    u = math.e ** ((rate - div) * (expiry / num) + (vol * math.sqrt(expiry / num)))
    d = math.e ** ((rate - div) * (expiry / num) - (vol * math.sqrt(expiry / num)))
    
    # calculate p*
    p_star = (math.e ** ((rate - div) * (expiry / num)) - d) / (u - d)
    
    # initalize array for the prices of the terminal nodes and calculate option premium
    terminal_spot_prices = np.zeros(num+1)
    option_premium = 0
    
    for i in range(num+1):
        terminal_spot_prices[i] = spot * (u ** (num - i)) * (d ** i)
        
        option_premium += payoff(terminal_spot_prices[i], strike) * binom.pmf(num-i, num, p_star)
            
            
    discount_factor = math.e ** (-rate * expiry)
        
    option_premium = option_premium * discount_factor
    
    return option_premium 

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
    pass   
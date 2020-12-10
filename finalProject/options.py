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


def simulate_prices(u, d, num, spot, strike):

    stock_prices = {}
    call_values = {}
    put_values = {}
    stock_prices['Period_0'] = np.array([spot])
    call_values['Period_0'] = np.array([spot - strike])
    put_values['Period_0'] = np.array([strike - spot])

    for i in range(1, num+1):
        previous_prices = stock_prices[f"Period_{i - 1}"]
        
        temp = []
        for price in previous_prices:
            temp.append(price * u)
            temp.append(price * d)

        price_result = []
        [price_result.append(price) for price in temp if price not in result]        

        stock_prices[f"Period_{i}"] = np.array(price_result)
        call_values[f"Period_{i}"] = np.array(price_result) - strike
        put_values[f"Period_{i}"] = strike - np.array(price_result)

    return (stock_prices, call_values, put_values)


def calculate_premium(spot: float, strike: float, expiry: float, rate: float, div: float, vol: float, num: int, payoff: Callable) -> float:
    
    # calculate u and d
    u = math.e ** ((rate - div) * (1+vol*math.sqrt(expiry / num)))
    d = math.e ** ((rate - div) * (1-vol*math.sqrt(expiry / num)))
    
    prices = simulate_prices(u, d, num, spot, strike)
    
    
    
    delta = (math.e ** (-div * (expiry / num))) * ((cu - cd)/(spot * (u - d)))
    b = (math.e ** (-rate * expiry / num)) * ((u * cd - d * cu) / (u - d))
    premium = delta * spot + b
    
    return premium
    


## Pricing functions
def european_binomial_pricer(spot: float, strike: float, expiry: float, rate: float, div: float, vol: float, num: int, payoff: Callable) -> float:
    
    # simulate stock prices until the final period
    
    # initialize an array the length of periods (num)
    data = np.fill(0, num)
    for i in range(num):
        print(hello)
        
    
        # calculate u and d
        # loop... for each point in time calculate Su and Sd
        # inside the loop keep track of the period we are in
        # stop when logic is executed num times

    # calculate value of option at each terminal node
    # calculate value of option at each inner node using
    # h = T/n --> expiry / num
    
    
    # what is t

def american_binomial_pricer(spot: float, strike: float, expiry: float, rate: float, div: float, vol: float, num: int, payoff: Callable) -> float:
    pass 

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
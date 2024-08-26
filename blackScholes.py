### Implementing the Black-Scholes formula for pricing European options

import numpy as np
from scipy.stats import norm

def black_scholes_price(risk_free_rate, spot_price, strike_price, time_to_maturity, volatility, option_type='Call'):
    """
    Calculates the Black-Scholes option price for a given set of parameters.
    Returns the option price
    """

    # Calculate d1 and d2
    d1 = (np.log(spot_price / strike_price) + (risk_free_rate + 0.5 * volatility ** 2) * time_to_maturity) / (volatility * np.sqrt(time_to_maturity))
    d2 = d1 - volatility * np.sqrt(time_to_maturity)
    
    # Calculate option price
    if option_type == 'Call':
        price = spot_price * norm.cdf(d1) - strike_price * np.exp(-risk_free_rate * time_to_maturity) * norm.cdf(d2)
    elif option_type == 'Put':
        price = strike_price * np.exp(-risk_free_rate * time_to_maturity) * norm.cdf(-d2) - spot_price * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'Call' or 'Put'")
    
    return price

def calculate_greeks(risk_free_rate, spot_price, strike_price, time_to_maturity, volatility, option_type='Call'):
    """
    Calculates the Greeks for the Black-Scholes option pricing model for a given set of parameters
    Returns a dictionary containing the calculated Greeks.
    """

    # Calculate d1 and d2
    d1 = (np.log(spot_price / strike_price) + (risk_free_rate + 0.5 * volatility ** 2) * time_to_maturity) / (volatility * np.sqrt(time_to_maturity))
    d2 = d1 - volatility * np.sqrt(time_to_maturity)
    
    # Calculate Greeks
    delta = norm.cdf(d1) if option_type == 'Call' else norm.cdf(d1) - 1
    gamma = norm.pdf(d1) / (spot_price * volatility * np.sqrt(time_to_maturity))
    vega = spot_price * norm.pdf(d1) * np.sqrt(time_to_maturity) / 100  # often quoted as per 1% change in volatility
    theta = (-spot_price * norm.pdf(d1) * volatility / (2 * np.sqrt(time_to_maturity)) 
             - risk_free_rate * strike_price * np.exp(-risk_free_rate * time_to_maturity) * norm.cdf(d2)) if option_type == 'Call' else \
            (-spot_price * norm.pdf(d1) * volatility / (2 * np.sqrt(time_to_maturity)) 
             + risk_free_rate * strike_price * np.exp(-risk_free_rate * time_to_maturity) * norm.cdf(-d2))
    theta /= 365  # often quoted as per day
    rho = (strike_price * time_to_maturity * np.exp(-risk_free_rate * time_to_maturity) * norm.cdf(d2) / 100) if option_type == 'Call' else \
          (-strike_price * time_to_maturity * np.exp(-risk_free_rate * time_to_maturity) * norm.cdf(-d2) / 100)
    
    # Return the Greeks
    return {
        'delta': delta,
        'gamma': gamma,
        'vega': vega,
        'theta': theta,
        'rho': rho,
    }


import numpy as np
import math

# Calculate payoffs
def calculate_payoff(spot_price, strike_price, option_type):
    if option_type == 'Call':
        return np.maximum(spot_price - strike_price, 0)
    elif option_type == 'Put':
        return np.maximum(strike_price - spot_price, 0)
    
# Calculate the option price using Monte Carlo simulation
def monte_carlo_option_pricing(option_type, spot_price, strike_price, volatility, risk_free_rate, time_to_maturity, num_simulations):
    dt = time_to_maturity / 252  # Assuming 252 trading days in a year
    option_payoffs = []
    price_paths = []

    for _ in range(num_simulations):
        price_path = []
        spot_price_copy = spot_price

        for _ in range(int(252 * time_to_maturity)):
            drift = (risk_free_rate - 0.5 * volatility**2) * dt
            shock = volatility * math.sqrt(dt) * np.random.normal(0, 1)
            spot_price_copy *= math.exp(drift + shock)
            price_path.append(spot_price_copy)

        price_paths.append(price_path)
        option_payoff = calculate_payoff(spot_price_copy, strike_price, option_type)
        option_payoffs.append(option_payoff)
        
    option_price = np.exp(-risk_free_rate * time_to_maturity) * np.mean(option_payoffs)
    return price_paths, option_price

#Example
option_type = 'Call'
spot_price = 100
strike_price = 100
volatility = 0.2
risk_free_rate = 0.05
time_to_maturity = 1
num_simulations = 1000


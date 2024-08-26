# Options Pricing app

This project provides an interactive dashboard for pricing options using the Black-Scholes model and Monte Carlo simulations. It allows users to explore various options pricing scenarios with real-time inputs and visualizations.

## Features
- Black-Scholes Model: Calculate and display the prices of Call and Put options using the Black-Scholes formula.
- Greeks Calculation: Compute and visualize the Greeks (Delta, Gamma, Vega, Theta, Rho) for both Call and Put options.
- Heatmap Visualization: Interactive heatmaps to explore how option prices fluctuate with varying spot prices and volatility.
- Monte Carlo Simulation: Simulate option price paths and estimate option prices using Monte Carlo methods.
- Interactive Inputs: Modify key parameters such as spot price, strike price, volatility, and risk-free rate to see real-time changes in option pricing.

## Installation
### Prerequisites
Ensure you have Python 3.7 or later installed. You will also need to install the following Python packages:

- streamlit
- pandas
- numpy
- matplotlib
- seaborn
- scipy
- plotly

## Customization
- **Color Scheme**: Modify the color scheme of the heatmaps by adjusting the create_custom_colormap function in app.py.
- **Input Parameters**: Adjust default values and ranges for input parameters in the sidebar to fit your specific needs.

## Acknowledgments
This project uses the Black-Scholes model for options pricing, a fundamental tool in financial mathematics.

This idea for this app was inspired by the work of Prudvhi Reddy. 
The layout is based on the following repository: https://github.com/prudhvi-reddy-m/BlackScholes


import streamlit as st

import pandas as pd
import numpy as np

from math import log, sqrt, exp
from scipy.stats import norm

import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

from blackScholes import black_scholes_price, calculate_greeks
from rates import get_10y_bond_yield
from monte_carlo_simulations import monte_carlo_option_pricing
from custom_cmap import create_custom_colormap

#######################
# Page configuration
st.set_page_config(
    page_title="Options Pricing Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")


# Custom CSS to inject into Streamlit
st.markdown("""
<style>
/* Adjust the size and alignment of the CALL and PUT value containers */
.metric-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 8px; /* Adjust the padding to control height */
    width: auto; /* Auto width for responsiveness, or set a fixed width if necessary */
    margin: 0 auto; /* Center the container */
}

/* Custom classes for CALL and PUT values */
.metric-call {
    background-color: #90ee90; /* Light green background */
    color: black; /* Black font color */
    margin-right: 10px; /* Spacing between CALL and PUT */
    border-radius: 10px; /* Rounded corners */
}

.metric-put {
    background-color: #ffcccb; /* Light red background */
    color: black; /* Black font color */
    border-radius: 10px; /* Rounded corners */
}

/* Style for the value text */
.metric-value {
    font-size: 1.5rem; /* Adjust font size */
    font-weight: bold;
    margin: 0; /* Remove default margins */
}

/* Style for the label text */
.metric-label {
    font-size: 1rem; /* Adjust font size */
    margin-bottom: 4px; /* Spacing between label and value */
}

</style>
""", unsafe_allow_html=True)


# Sidebar for User Inputs
with st.sidebar:
    st.title("📊 Black-Scholes Model")
    
    spot_price = st.number_input("Current Asset Price", value=100.0)
    strike_price = st.number_input("Strike Price", value=100.0)
    time_to_maturity = st.number_input("Time to Maturity (Years)", value=1.0)
    volatility = st.number_input("Volatility (σ)", value=0.2)
    
    # Risk-Free Rate Input
    risk_free_rate_source = st.selectbox(
        "Select Risk-Free Rate Source", 
        ["Custom Rate", "US 10Y", "UK 10Y", "Germany 10Y", "Japan 10Y"]
    )
    
    if risk_free_rate_source == "Custom Rate":
        risk_free_rate = st.number_input("Risk-Free Interest Rate", value=0.05)
        st.write(f"Using Custom Rate: {risk_free_rate * 100:.2f}%")
    else:
            try:
                risk_free_rate = get_10y_bond_yield(risk_free_rate_source)
                st.write(f"Current {risk_free_rate_source} 10-Year Bond Yield: {risk_free_rate * 100:.2f}%")
            except ValueError as e:
                st.error(str(e))
                risk_free_rate = 0.0

    st.markdown("---")
    st.title("Heatmap Parameters")
    spot_min = st.number_input('Min Spot Price', min_value=0.01, value=spot_price*0.8, step=0.01)
    spot_max = st.number_input('Max Spot Price', min_value=0.01, value=spot_price*1.2, step=0.01)
    vol_min = st.slider('Min Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility*0.5, step=0.01)
    vol_max = st.slider('Max Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility*1.5, step=0.01)
    
    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)
    
    st.markdown("---")
    st.title("Monte Carlo Simulation")
    num_simulations = st.number_input("Number of Simulations", value=100)

# Black-Scholes Price Calculation
call_price = black_scholes_price(risk_free_rate, spot_price, strike_price, time_to_maturity, volatility, option_type='Call')
put_price = black_scholes_price(risk_free_rate, spot_price, strike_price, time_to_maturity, volatility, option_type='Put')

custom_cmap = create_custom_colormap()

def plot_heatmap(spot_range, vol_range, strike, risk_free_rate, time_to_maturity):
    call_prices = np.zeros((len(vol_range), len(spot_range)))
    put_prices = np.zeros((len(vol_range), len(spot_range)))

    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            call_prices[i, j] = black_scholes_price(risk_free_rate, spot, strike, time_to_maturity, vol, option_type='Call')
            put_prices[i, j] = black_scholes_price(risk_free_rate, spot, strike, time_to_maturity, vol, option_type='Put')

    # Plotting Call Price Heatmap
    fig_call, ax_call = plt.subplots(figsize=(10, 8))
    sns.heatmap(call_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap=custom_cmap, ax=ax_call)
    ax_call.set_title('CALL')
    ax_call.set_xlabel('Spot Price')
    ax_call.set_ylabel('Volatility')

    # Plotting Put Price Heatmap
    fig_put, ax_put = plt.subplots(figsize=(10, 8))
    sns.heatmap(put_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap=custom_cmap, ax=ax_put)
    ax_put.set_title('PUT')
    ax_put.set_xlabel('Spot Price')
    ax_put.set_ylabel('Volatility')

    return fig_call, fig_put

# Main Page for Output Display
st.title("Black-Scholes Pricing Model")

# Table of Inputs
input_data = {
    "Current Asset Price": [spot_price],
    "Strike Price": [strike_price],
    "Time to Maturity (Years)": [time_to_maturity],
    "Volatility (σ)": [volatility],
    "Risk-Free Interest Rate": [risk_free_rate],
    "Number of Simulations": [num_simulations],
}
input_df = pd.DataFrame(input_data)
st.table(input_df)

# Display Call and Put Values in colored tables
col1, col2 = st.columns([1,1], gap="small")

with col1:
    # Using the custom class for CALL value
    st.markdown(f"""
        <div class="metric-container metric-call">
            <div>
                <div class="metric-label">CALL Value</div>
                <div class="metric-value">${call_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # Using the custom class for PUT value
    st.markdown(f"""
        <div class="metric-container metric-put">
            <div>
                <div class="metric-label">PUT Value</div>
                <div class="metric-value">${put_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("")
st.title("Options Price - Interactive Heatmap")
st.info("Explore how option prices fluctuate with varying 'Spot Prices and Volatility' levels using interactive heatmap parameters, all while maintaining a constant 'Strike Price'.")

# Interactive Sliders and Heatmaps for Call and Put Options
col1, col2 = st.columns([1,1], gap="small")

with col1:
    st.subheader("Call Price Heatmap")
    heatmap_fig_call, _ = plot_heatmap(spot_range, vol_range, strike_price, risk_free_rate, time_to_maturity)
    st.pyplot(heatmap_fig_call)

with col2:
    st.subheader("Put Price Heatmap")
    _, heatmap_fig_put = plot_heatmap(spot_range, vol_range, strike_price, risk_free_rate, time_to_maturity)
    st.pyplot(heatmap_fig_put)
    
    
# Monte Carlo Simulation
with col1:
    st.write("## Monte Carlo Simulation - Call Option")
    # Calculate the option price using Monte Carlo simulation and obtain price paths
    price_paths_call, option_price_call= monte_carlo_option_pricing('Call', spot_price, strike_price, volatility, risk_free_rate, time_to_maturity, num_simulations)

    st.metric("The estimated call option price after " + str(num_simulations) + " simulation runs is: ", f"{option_price_call:.2f}")

    # Combine the simulated price paths into a single DataFrame
    df = pd.DataFrame(price_paths_call).T
    # Rename columns
    df.columns = [f"Path {i+1}" for i in range(num_simulations)]

    # Create an interactive plot using Plotly Express
    fig = px.line(df, labels={"index": "Time Steps", "value": "Spot Price"}, title="Simulated Price Paths")

    st.plotly_chart(fig, use_container_width=True)
    
with col2:
    st.write("## Monte Carlo Simulation - Put Option")
    # Calculate the option price using Monte Carlo simulation and obtain price paths
    price_paths_put, option_price_put= monte_carlo_option_pricing('Put', spot_price, strike_price, volatility, risk_free_rate, time_to_maturity, num_simulations)

    st.metric("The estimated put option price after " + str(num_simulations) + " simulation runs is: ", f"{option_price_put:.2f}")

    # Combine the simulated price paths into a single DataFrame
    df = pd.DataFrame(price_paths_put).T
    # Rename columns
    df.columns = [f"Path {i+1}" for i in range(num_simulations)]

    # Create an interactive plot using Plotly Express
    fig = px.line(df, labels={"index": "Time Steps", "value": "Spot Price"}, title="Simulated Price Paths")

    st.plotly_chart(fig, use_container_width=True)
    
    
# Greeks Calculation
# Calculate Greeks for both Call and Put options
greeks_call = calculate_greeks(risk_free_rate, spot_price, strike_price, time_to_maturity, volatility, option_type='Call')
greeks_put = calculate_greeks(risk_free_rate, spot_price, strike_price, time_to_maturity, volatility, option_type='Put')

# Display the Greeks in a metric format
st.write("## Greeks")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Delta (Call)", f"{greeks_call['delta']:.2f}")
    st.metric("Delta (Put)", f"{greeks_put['delta']:.2f}")

with col2:
    st.metric("Gamma (Call)", f"{greeks_call['gamma']:.2f}")
    st.metric("Gamma (Put)", f"{greeks_put['gamma']:.2f}")

with col3:
    st.metric("Vega (Call)", f"{greeks_call['vega']:.2f}")
    st.metric("Vega (Put)", f"{greeks_put['vega']:.2f}")

with col4:
    st.metric("Theta (Call)", f"{greeks_call['theta']:.2f}")
    st.metric("Theta (Put)", f"{greeks_put['theta']:.2f}")

with col5:
    st.metric("Rho (Call)", f"{greeks_call['rho']:.2f}")
    st.metric("Rho (Put)", f"{greeks_put['rho']:.2f}")

# Optional: Create a DataFrame and plot for further analysis
greeks_df = pd.DataFrame({
    'Greek': ['Delta', 'Gamma', 'Vega', 'Theta', 'Rho'],
    'Call': [greeks_call['delta'], greeks_call['gamma'], greeks_call['vega'], greeks_call['theta'], greeks_call['rho']],
    'Put': [greeks_put['delta'], greeks_put['gamma'], greeks_put['vega'], greeks_put['theta'], greeks_put['rho']]
})

# Interactive Plot for Greeks
fig = px.bar(greeks_df, x='Greek', y=['Call', 'Put'], barmode='group', title="Comparison of Greeks for Call and Put Options")
st.plotly_chart(fig, use_container_width=True)
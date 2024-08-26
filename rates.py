import requests
from config import API_KEY

import requests

def get_10y_bond_yield(API_KEY: str, country: str) -> float:
    # Define FRED series IDs for different countries
    series_ids = {
        "US 10Y": "DGS10",         # 10-Year Treasury Constant Maturity Rate for the US
        "UK 10Y": "IRLTLT01GBM156N", # 10-Year Government Bond Yield for the UK (using appropriate FRED series ID)
        "Germany 10Y": "IRLTLT01DEQ156N", # 10-Year Government Bond Yield for Germany (using appropriate FRED series ID)
        "Japan 10Y": "IRLTLT01JPQ156N"   # 10-Year Government Bond Yield for Japan (using appropriate FRED series ID)
    }
    
    if country not in series_ids:
        raise ValueError(f"Country '{country}' is not supported or series ID is missing.")
    
    series_id = series_ids[country]
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={API_KEY}&file_type=json"
    
    response = requests.get(url)
    data = response.json()
    
    # Extract the most recent yield value
    try:
        recent_data = data['observations'][-1]
        yield_value = float(recent_data['value']) / 100
        return yield_value
    except KeyError:
        raise ValueError("API response doesn't contain expected data. Please check the API key and response format.")

# Example use
yield_10y = get_10y_bond_yield(API_KEY, "US 10Y")
print(f"10-Year Bond Yield: {yield_10y * 100:.2f}%")

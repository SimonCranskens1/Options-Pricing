import matplotlib.colors as mcolors

def create_custom_colormap():
    # Define the colors for the colormap
    colors = ["red", "white", "green"]
    
    # Create a LinearSegmentedColormap
    cmap = mcolors.LinearSegmentedColormap.from_list("RedGreen", colors, N=256)
    
    return cmap
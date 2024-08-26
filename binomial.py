# Option pricing using binomial asset pricing model

# Import libraries
import numpy as np

# Initial parameters
S0 = 100      
K = 100       
T = 1        
r = 0.06      
N = 3         
u = 1.1       
d = 1/u
opttype = 'C' # Call option

def binomial_tree(S0, K, T, r, N, u, d, opttype='C'):
    # Calculate delta t
    dt = T/N
    
    # Calculate probability of up and down movements
    q = (np.exp(r*dt) - d) / (u - d)
    
    # Calculate discount
    discount = np.exp(-r*dt)
    
    # Initialize the asset prices at maturity - Time Step N
    C = S0* d**(np.arange(N, -1, -1)) * u**(np.arange(0, N+1, 1))
    
    #Initialize option values at maturity
    C = np.maximum(np.zeros(N+1), C-K)
    
        # step backwards through tree
    for i in np.arange(N,0,-1):
        C = discount * ( q * C[1:i+1] + (1-q) * C[0:i] )

    return C[0]

for N in [3, 100, 1000]:
    print(binomial_tree(K,T,S0,r,N,u,d,opttype='C'))
    
    
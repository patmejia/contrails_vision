import numpy as np
import sys

filename = sys.argv[1] 

data = np.load(filename) 

print(f'Shape: {data.shape}')
print(f'Size: {data.size}')  
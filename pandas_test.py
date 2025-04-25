import pandas as pd
import numpy as np

print("Successfully imported pandas and numpy!")

# Create a simple dataframe
df = pd.DataFrame({
    'x': np.random.normal(0, 1, 5),
    'y': np.random.normal(0, 1, 5),
    'group': ['A', 'B', 'A', 'B', 'C']
})

print("DataFrame created:")
print(df)

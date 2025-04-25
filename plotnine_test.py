"""
Test file to verify that tidyplots functionality is working with plotnine.
"""
import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_point

# Try to import tidyplots
try:
    from tidyplots import TidyPlot
    print("Successfully imported tidyplots!")
except ImportError as e:
    print(f"Failed to import tidyplots: {e}")

# Create a simple dataframe
try:
    df = pd.DataFrame({
        'x': np.random.normal(0, 1, 100),
        'y': np.random.normal(0, 1, 100),
        'group': np.random.choice(['A', 'B', 'C'], 100)
    })
    print("Successfully created test dataframe!")
except Exception as e:
    print(f"Failed to create dataframe: {e}")

# Try to create a simple plot with plotnine
try:
    plot = ggplot(df, aes(x='x', y='y', color='group')) + geom_point()
    print("Successfully created a plotnine plot!")
except Exception as e:
    print(f"Failed to create plotnine plot: {e}")

# Try to create a simple plot if tidyplots is available
try:
    # Check if tidyplot method is available
    if hasattr(df, 'tidyplot'):
        plot = df.tidyplot(x='x', y='y', fill='group').add_scatter()
        print("Successfully created a tidyplot!")
    else:
        print("tidyplot method not available on DataFrame")
except Exception as e:
    print(f"Failed to create tidyplot: {e}")

print("Test completed!")

"""
Examples of heatmap visualizations using TidyPlots.
"""

import pandas as pd
import numpy as np
from tidyplots import tidyplot

print("\nExample 1: Basic Heatmap (Default Palette)")
# Create sample data
data = pd.DataFrame({
    'x': np.repeat(range(5), 5),
    'y': np.tile(range(5), 5),
    'value': np.random.rand(25)
})

# Using default palette (npg)
(data.tidyplot(x='x', y='y', fill='value')
 .add_heatmap()
 .save('figures/basic_heatmap.png'))

print("\nExample 2: Correlation Matrix Heatmap (NEJM)")
# Create correlation matrix
np.random.seed(42)
corr_data = pd.DataFrame(np.random.randn(5, 5), columns=['A', 'B', 'C', 'D', 'E'])
corr_matrix = corr_data.corr()

# Convert correlation matrix to long format
corr_long = pd.DataFrame([
    {'x': i, 'y': j, 'value': corr_matrix.iloc[i, j]}
    for i in range(len(corr_matrix))
    for j in range(len(corr_matrix))
])

(corr_long.tidyplot(x='x', y='y', fill='value')
 .adjust_colors(palette='nejm')
 .add_heatmap(show_values=True)
 .save('figures/correlation_heatmap.png'))

print("\nExample 3: Categorical Heatmap (Lancet)")
# Create categorical data
categories = ['A', 'B', 'C', 'D']
data = pd.DataFrame({
    'x': np.repeat(categories, 4),
    'y': np.tile(categories, 4),
    'value': np.random.randint(1, 10, 16)
})

(data.tidyplot(x='x', y='y', fill='value')
 .adjust_colors(palette='lancet')
 .add_heatmap(show_values=True, value_format='{:.0f}')
 .save('figures/categorical_heatmap.png'))

print("\nExample 4: Time Series Heatmap (JCO)")
# Create time series data
dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
hours = range(24)
data = pd.DataFrame({
    'date': np.repeat(dates, 24),
    'hour': np.tile(hours, len(dates)),
    'value': np.random.rand(len(dates) * 24)
})

(data.tidyplot(x='date', y='hour', fill='value')
 .adjust_colors(palette='jco')
 .add_heatmap()
 .save('figures/timeseries_heatmap.png'))

print("\nExample 5: Custom Style Heatmap (AAAS)")
# Create sample data with custom style
data = pd.DataFrame({
    'x': np.repeat(range(10), 10),
    'y': np.tile(range(10), 10),
    'value': np.random.rand(100)
})

(data.tidyplot(x='x', y='y', fill='value')
 .adjust_colors(palette='aaas')
 .add_heatmap(alpha=0.8)
 .save('figures/custom_heatmap.png'))

print("\nExample 6: Palette Comparison")
# Create sample data
data = pd.DataFrame({
    'x': np.repeat(range(5), 5),
    'y': np.tile(range(5), 5),
    'value': np.random.rand(25)
})

print("6.1: Default NPG Palette")
(data.tidyplot(x='x', y='y', fill='value')
 .add_heatmap()
 .save('figures/palette_default.png'))

print("6.2: JAMA Palette")
(data.tidyplot(x='x', y='y', fill='value')
 .adjust_colors(palette='jama')
 .add_heatmap()
 .save('figures/palette_jama.png'))

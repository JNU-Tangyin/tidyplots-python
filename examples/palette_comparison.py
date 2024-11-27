"""Comparison of scientific color palettes from TidySci."""

import pandas as pd
import numpy as np
from tidyplots import TidyPlot
import os

# Create directory for figures if it doesn't exist
os.makedirs("figures", exist_ok=True)

# Create sample data with multiple groups
np.random.seed(42)
n = 50
palettes = ['npg', 'aaas', 'nejm', 'lancet', 'jama', 'd3', 'material', 'igv']

# Create a plot for each palette
for i, palette in enumerate(palettes):
    data = pd.DataFrame({
        'x': np.random.normal(0, 1, n * 6),
        'y': np.random.normal(0, 1, n * 6),
        'group': np.repeat(['A', 'B', 'C', 'D', 'E', 'F'], n)
    })
    
    # Create scatter plot with the current palette
    (data.tidyplot(x='x', y='y', color='group')
     .add_scatter()
     .adjust_colors(palette)
     .adjust_labels(title=f'{palette.upper()} Color Palette',
                   x='X Value',
                   y='Y Value')
     .save(f'figures/palette_{palette}.png'))

# Create a bar plot comparing all palettes
data = pd.DataFrame({
    'x': np.tile(np.arange(6), len(palettes)),
    'y': np.random.uniform(0, 1, 6 * len(palettes)),
    'group': np.repeat(['A', 'B', 'C', 'D', 'E', 'F'], len(palettes)),
    'palette': np.repeat(palettes, 6)
})

# Create faceted bar plot
(data.tidyplot(x='group', y='y', color='group')
 .add_bar()
 .adjust_colors('npg')  # Use NPG palette for the combined plot
 .adjust_labels(title='Scientific Color Palettes Comparison',
               x='Group',
               y='Value')
 .save('figures/palette_comparison.png'))

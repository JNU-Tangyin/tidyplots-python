"""Gallery of tidyplots examples."""

import pandas as pd
import numpy as np
from tidyplots import TidyPlot
import os

# Create directory for figures if it doesn't exist
os.makedirs("figures", exist_ok=True)

# Generate sample data
np.random.seed(42)
n = 100
data = pd.DataFrame({
    'x': np.random.normal(0, 1, n),
    'y': np.random.normal(0, 1, n),
    'group': np.random.choice(['A', 'B', 'C'], n),
    'time': pd.date_range(start='2023-01-01', periods=n),
    'value': np.random.normal(10, 2, n)
})

# Example 1: Time series with trend
(data.tidyplot(x='time', y='value')
 .add_line()
 .add_scatter()
 .adjust_labels(title='Time Series Plot', x='Date', y='Value')
 .save('figures/time_series.png'))

# Example 2: Scatter plot with groups
(data.tidyplot(x='x', y='y', color='group')
 .add_scatter()
 .adjust_labels(title='Grouped Scatter Plot', x='X', y='Y')
 .save('figures/scatter_groups.png'))

# Example 3: Box plot with data points and p-values
(data.tidyplot(x='group', y='y')
 .add_boxplot()
 .add_scatter(alpha=0.3)
 # .add_pvalue(0.001, 0, 2, 2.5)  # Add significance between groups A and C
 .adjust_labels(title='Box Plot with P-value', x='Group', y='Value')
 .save('figures/boxplot_jitter.png'))

# Example 4: Violin plot with quartiles
(data.tidyplot(x='group', y='y')
 .add_violin(draw_quantiles=[0.25, 0.5, 0.75])
 .adjust_labels(title='Violin Plot with Quartiles', x='Group', y='Value')
 .save('figures/violin_quartiles.png'))

# Example 5: Density plot with groups
(data.tidyplot(x='y', color='group')
 .add_density(alpha=0.5)
 .adjust_labels(title='Density Plot by Group', x='Value', y='Density')
 .save('figures/density_groups.png'))

# Example 6: 2D density plot
(data.tidyplot(x='x', y='y')
 .add_density_2d()
 .adjust_colors('Blues')
 .adjust_labels(title='2D Density Plot', x='X', y='Y')
 .save('figures/density_2d.png'))

# Example 7: Bar plot with error bars
means = data.groupby('group')['y'].mean().reset_index()
sems = data.groupby('group')['y'].sem().reset_index()
(means.tidyplot(x='group', y='y')
 .add_bar()
 .add_errorbar(ymin=means['y']-sems['y'], ymax=means['y']+sems['y'])
 .adjust_labels(title='Bar Plot with Error Bars', x='Group', y='Value')
 .save('figures/barplot_error.png'))

# Example 8: Correlation plot
(data.tidyplot(x='x', y='y')
 .add_scatter()
 .add_smooth(method='lm')
 .add_correlation_text()
 .adjust_labels(title='Correlation Plot', x='X', y='Y')
 .save('figures/correlation.png'))

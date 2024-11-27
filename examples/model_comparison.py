"""
Example script demonstrating tidyplots capabilities using model comparison data.
"""
import os
import pandas as pd
from tidyplots import tidyplot

# Create figures directory if it doesn't exist
os.makedirs('../figures', exist_ok=True)

# Read the data
df = pd.read_csv('result.csv')

# 1. Box plot of CGAR by dataset
(tidyplot(df, x='dataset', y='CGAR', color='dataset')
 .add_boxplot(alpha=0.3)
 .add_data_points_jitter(width=0.2, alpha=0.5)
 .adjust_colors('Blues')
 .adjust_axis_text_angle(45)
 .adjust_labels(title='CGAR Distribution by Dataset',
            x='Dataset',
            y='CGAR')
 .save('../figures/cgar_boxplot.png'))

# 2. Scatter plot with trend line
(tidyplot(df, x='volatility', y='sharp_ratio', color='dataset')
 .add_scatter(alpha=0.7)
 .add_smooth(method='lm')
 .adjust_colors('Blues')
 .adjust_labels(title='Sharp Ratio vs Volatility',
               x='Volatility', y='Sharp Ratio')
 .save('../figures/sharp_ratio_vs_volatility.png'))

# 3. Violin plot with data points
(tidyplot(df, x='dataset', y='total_return', color='dataset')
 .add_violin(alpha=0.4)
 .add_data_points_jitter(width=0.2, alpha=0.5)
 .adjust_colors('Blues')
 .adjust_axis_text_angle(45)
 .adjust_labels(title='Total Return Distribution by Dataset',
            x='Dataset',
            y='Total Return')
 .save('../figures/total_return_violin.png'))

# 4. Error bar plot of average returns by model type
model_stats = df.groupby('model_name').agg({
    'CGAR': ['mean', 'std']
}).reset_index()
model_stats.columns = ['model_name', 'CGAR_mean', 'CGAR_std']

(tidyplot(model_stats, x='model_name', y='CGAR_mean')
 .add_errorbar(ymin='CGAR_mean - CGAR_std', 
               ymax='CGAR_mean + CGAR_std')
 .add_mean_bar(alpha=0.4)
 .adjust_labels(title='Average CGAR by Model Type (with std dev)',
               x='Model', y='CGAR')
 .adjust_axis_text_angle(45)
 .save('../figures/model_performance_comparison.png'))

# 5. Hexbin plot of returns vs volatility
(tidyplot(df, x='volatility', y='total_return')
 .add_hex(bins=20)
 .scale_color_gradient(low='lightblue', high='darkblue')
 .adjust_labels(title='Returns vs Volatility (Hexbin)',
            x='Volatility',
            y='Returns')
 .save('../figures/returns_volatility_hexbin.png'))

# 6. Density plot of returns by dataset
(tidyplot(df, x='total_return', color='dataset')
 .add_density(alpha=0.3)
 .adjust_colors('Blues')
 .adjust_labels(title='Return Distribution by Dataset',
               x='Total Return', y='Density')
 .save('../figures/return_density.png'))

# 7. Bar plot of average VaR by dataset
(tidyplot(df, x='dataset', y='value_at_risk')
 .add_mean_bar()
 .add_data_points_jitter(width=0.2, alpha=0.3)
 .adjust_labels(title='Value at Risk by Dataset',
               x='Dataset', y='Value at Risk')
 .adjust_colors('Set1')
 .save('../figures/var_by_dataset.png'))

# 8. Scatter plot matrix of key metrics
key_metrics = ['CGAR', 'sharp_ratio', 'volatility', 'value_at_risk']
(tidyplot(df, key_metrics)
 .add_scatter_matrix(alpha=0.5)
 .adjust_labels(title='Correlation Matrix of Key Metrics')
 .save('../figures/metrics_correlation_matrix.png'))

print("All example plots have been generated in the figures directory.")

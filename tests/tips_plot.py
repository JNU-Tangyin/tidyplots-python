import pandas as pd
import seaborn as sns
from tidyplots import tidyplot
import os

# Create figures directory if it doesn't exist
os.makedirs('figures', exist_ok=True)

# Load the tips dataset
tips = sns.load_dataset("tips")

# Create faceted scatter plot
plot = (tips.tidyplot(x='total_bill', y='tip', split_by=['day', 'time'], fill='smoker')
 .add_scatter(alpha=0.6)
 .adjust_labels(title='Tips by Day and Time',
               x='Total Bill', y='Tip')
 .save('figures/13.2_tips_facet_grid.png'))

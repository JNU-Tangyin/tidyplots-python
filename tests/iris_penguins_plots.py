import pandas as pd
import seaborn as sns
from tidyplots import tidyplot
import os

# Create figures directory if it doesn't exist
os.makedirs('figures', exist_ok=True)

# Load the datasets
iris = sns.load_dataset("iris")
penguins = sns.load_dataset("penguins")

# Create faceted scatter plot for iris data
iris_plot = (iris.tidyplot(x='sepal_length', y='sepal_width', split_by='species', fill='species')
 .add_scatter(alpha=0.6)
 .adjust_labels(title='Iris Measurements by Species',
               x='Sepal Length', y='Sepal Width')
 .save('figures/iris_scatter.png'))

# Create faceted violin plot for penguins data
penguins_plot = (penguins.tidyplot(x='species', y='body_mass_g', split_by='island', fill='species')
 .add_violin(alpha=0.7)
 .adjust_labels(title='Penguin Body Mass by Island',
               x='Species', y='Body Mass (g)')
 .save('figures/penguins_violin.png'))

"""
Examples demonstrating the faceting functionality in tidyplots.
"""
import pandas as pd
import seaborn as sns
from tidyplots import TidyPlot

# Example 1: Iris Dataset with single variable faceting
print("\nExample 1: Iris Dataset with facet_wrap")
iris = sns.load_dataset("iris")
(iris.tidyplot(x='sepal_length', y='sepal_width', fill='species', split_by='species')
 .add_scatter(alpha=0.6)
 .adjust_labels(title='Iris Measurements by Species',
               x='Sepal Length', y='Sepal Width')
 .save('figures/13.1_iris_facet_wrap.png'))

# Example 2: Tips Dataset with two variable faceting
print("\nExample 2: Tips Dataset with facet_grid")
tips = sns.load_dataset("tips")
(tips.tidyplot(x='total_bill', y='tip', fill='smoker', split_by=['day', 'time'])
 .add_scatter(alpha=0.6)
 .adjust_labels(title='Tips by Day and Time',
               x='Total Bill', y='Tip')
 .save('figures/13.2_tips_facet_grid.png'))

# Example 3: Penguins Dataset with facet_wrap and violin plots
print("\nExample 3: Penguins Dataset with facet_wrap and violin plots")
penguins = sns.load_dataset("penguins")
(penguins.tidyplot(x='species', y='body_mass_g', fill='species', split_by='island')
 .add_violin(alpha=0.7)
 .adjust_labels(title='Penguin Body Mass by Island',
               x='Species', y='Body Mass (g)')
 .save('figures/13.3_penguins_facet_wrap.png'))

# Example 4: Diamonds Dataset with facet_grid and boxplots
print("\nExample 4: Diamonds Dataset with facet_grid and boxplots")
diamonds = sns.load_dataset("diamonds")
# Create a smaller subset for better visualization
diamonds_subset = diamonds.sample(n=1000, random_state=42)
(diamonds_subset.tidyplot(x='cut', y='price', fill='color', split_by=['color', 'clarity'])
 .add_boxplot(alpha=0.7)
 .adjust_labels(title='Diamond Prices by Cut, Color, and Clarity',
               x='Cut', y='Price')
 .save('figures/13.4_diamonds_facet_grid.png'))

# Example 5: Titanic Dataset with facet_wrap and bar plots
print("\nExample 5: Titanic Dataset with facet_wrap and bar plots")
titanic = sns.load_dataset("titanic")
# Convert 'survived' to string for better labels
titanic['survived'] = titanic['survived'].map({0: 'No', 1: 'Yes'})
survival_data = titanic.groupby(['class', 'sex', 'survived']).size().reset_index(name='count')

(survival_data.tidyplot(x='class', y='count', fill='survived', split_by='sex')
 .add_bar(position='dodge', alpha=0.7)
 .adjust_labels(title='Titanic Survival by Class and Sex',
               x='Class', y='Count')
 .save('figures/13.5_titanic_facet_wrap.png'))

print("\nAll faceting examples have been generated in the 'figures' directory.")

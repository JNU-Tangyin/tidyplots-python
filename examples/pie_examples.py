import pandas as pd
import seaborn as sns
from tidyplots import tidyplot
from plotnine import facet_wrap
import os
import numpy as np

# Create figures directory if it doesn't exist
os.makedirs('figures', exist_ok=True)

# Load example datasets
titanic = sns.load_dataset('titanic')
tips = sns.load_dataset('tips')
diamonds = sns.load_dataset('diamonds')

# Example 1: Titanic Survival Pie Chart
print("\nExample 1: Titanic Survival Pie Chart")
survival_counts = titanic.groupby('survived', observed=True).size().reset_index(name='count')
survival_counts['survived'] = survival_counts['survived'].map({0: 'Did Not Survive', 1: 'Survived'})

(survival_counts.tidyplot(x='survived', y='count')
 .add_pie()
 .save('figures/survival_pie.png'))

# Example 2: Tips by day distribution as a donut chart
print("\nExample 2: Tips by Day Donut Chart")
day_counts = tips.groupby('day', observed=True).size().reset_index(name='count')

(day_counts.tidyplot(x='day', y='count')
 .add_donut(inner_radius=0.6)
 .save('figures/tips_by_day_donut.png'))

# Example 3: Tips by day as a pie chart with white edges
print("\nExample 3: Tips by Day Pie Chart")
class_counts = tips.groupby('day', observed=True).agg({
    'total_bill': 'mean',
    'tip': 'mean'
}).reset_index()

# Custom colors for each slice
colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99']

# First chart - Total Bill
(class_counts.tidyplot(x='day', y='total_bill')
 .add_pie(fill=colors)
 .save('figures/tips_by_day_pie.png'))

# Second chart - Tips
(class_counts.tidyplot(x='day', y='tip')
 .add_donut(inner_radius=0.7, fill=colors)
 .save('figures/tips_donut.png'))

# Example 4: Diamond cut distribution as a donut chart with larger hole
print("\nExample 4: Diamonds Cut Distribution")
cut_counts = diamonds.groupby('cut', observed=True).size().reset_index(name='count')

(cut_counts.tidyplot(x='cut', y='count')
 .add_donut(inner_radius=0.7)
 .save('figures/diamond_cut_donut.png'))

# Example 5: Faceted pie charts showing survival by class
print("\nExample 5: Titanic Survival by Class")
survival_by_class = titanic.groupby(['class', 'survived'], observed=True).size().reset_index(name='count')
# Map survived values to readable labels
survival_labels = {0: 'Did Not Survive', 1: 'Survived'}
survival_by_class['survived'] = survival_by_class['survived'].map(survival_labels)

# Create plot with faceting
plot = (survival_by_class.tidyplot(x='survived', y='count')
        .add_pie()
        .plot + facet_wrap('class', nrow=1))

# Save the plot
plot.save('figures/survival_by_class_pies.png')

# Example 6: Donut chart with custom colors and very thin ring
print("\nExample 6: Thin Ring Donut Chart")
class_counts = titanic.groupby('class', observed=True).size().reset_index(name='count')

(class_counts.tidyplot(x='class', y='count')
 .add_donut(inner_radius=0.8, fill=['#FF9999', '#66B2FF', '#99FF99'])
 .save('figures/thin_ring_donut.png'))

# Example 7: Side-by-side donut charts
print("\nExample 7: Side-by-side Donut Charts")
# First create the class distribution donut
(class_counts.tidyplot(x='class', y='count')
 .add_donut(inner_radius=0.6, fill=['#FF9999', '#66B2FF', '#99FF99'])
 .save('figures/class_donut.png'))

# Then create the survival distribution donut
survival_counts = titanic.groupby('survived', observed=True).size().reset_index(name='count')
survival_counts['survived'] = survival_counts['survived'].map({0: 'Did Not Survive', 1: 'Survived'})

(survival_counts.tidyplot(x='survived', y='count')
 .add_donut(inner_radius=0.7, fill=['#ffcc99', '#ff99cc'])
 .save('figures/survival_donut.png'))

# Example 8: Multiple small donut charts in a grid
print("\nExample 8: Small Donut Charts Grid")
# Create separate donut charts for each class
for i, passenger_class in enumerate(titanic['class'].unique()):
    class_survival = (
        titanic[titanic['class'] == passenger_class]
        .groupby('survived', observed=True)
        .size()
        .reset_index(name='count')
    )
    class_survival['survived'] = class_survival['survived'].map({0: 'Did Not Survive', 1: 'Survived'})
    
    (class_survival.tidyplot(x='survived', y='count')
     .add_donut(inner_radius=0.6, fill=['#ff9999', '#66b3ff'])
     .save(f'figures/class_{passenger_class.lower()}_survival_donut.png'))

# Example 9: Sorted pie chart with percentage labels
print("\nExample 9: Sorted Pie Chart with Labels")
day_counts = tips.groupby('day', observed=True).size().reset_index(name='count')

(day_counts.tidyplot(x='day', y='count')
 .add_pie(sort=True, show_labels=True, label_type='both', label_radius=1.2, label_size=12)
 .save('figures/sorted_pie_with_labels.png'))

# Example 10: Exploded pie chart
print("\nExample 10: Exploded Pie Chart")
class_counts = titanic.groupby('class', observed=True).size().reset_index(name='count')

(class_counts.tidyplot(x='class', y='count')
 .add_pie(explode=[0.1, 0.1, 0.2], start_angle=45, show_labels=True, label_type='{:.0f}', fill=['#FF9999', '#66B2FF', '#99FF99'])
 .save('figures/exploded_pie.png'))

# Example 11: Customized donut chart
print("\nExample 11: Customized Donut Chart")
cut_counts = diamonds.groupby('cut', observed=True).size().reset_index(name='count')

(cut_counts.tidyplot(x='cut', y='count')
 .add_donut(inner_radius=0.7, sort=True, show_labels=True, label_type='percent', label_radius=0.85, label_size=8)
 .save('figures/custom_donut.png'))

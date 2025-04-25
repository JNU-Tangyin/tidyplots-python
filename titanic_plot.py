import pandas as pd
import seaborn as sns
from tidyplots import tidyplot
import os

# Create figures directory if it doesn't exist
os.makedirs('figures', exist_ok=True)

# Load the Titanic dataset
titanic = sns.load_dataset("titanic")

# Prepare the data
survival_data = titanic.groupby(['class', 'sex', 'survived']).size().reset_index(name='count')

# Create faceted bar plot
(survival_data.tidyplot(x='class', y='count', fill='survived', split_by='sex')
 .add_bar(position='dodge', alpha=0.7)
 .adjust_labels(title='Titanic Survival by Class and Sex',
               x='Class', y='Count')
 .save('figures/titanic_survival.png'))

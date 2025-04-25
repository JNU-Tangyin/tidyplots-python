import pandas as pd
import numpy as np
import tidyplots
import os

# Get the absolute path to the figures directory
FIGURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures')

# Example 1: Monthly Sales Data
monthly_data = pd.DataFrame({
    'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'sales': [100, 120, 140, 160, 180, 200, 
              190, 180, 160, 140, 120, 100]
})

(monthly_data.tidyplot(x='month', y='sales')
 .adjust_title('Monthly Sales Distribution')
 .add_rose(show_labels=True, label_type='value')
 .adjust_colors(['#FF4B4B'])  # Use a single red color
 .save(os.path.join(FIGURES_DIR, 'rose_monthly.png')))

# Example 2: Basic Rose Chart
data = pd.DataFrame({
    'category': ['A', 'B', 'C', 'D', 'E', 'F'],
    'value': [30, 45, 20, 35, 25, 40]
})

(data.tidyplot(x='category', y='value')
 .adjust_title('Basic Nightingale Rose Chart')
 .add_rose(show_labels=True, label_type='both')
 .adjust_colors(['#FF4B4B'])  # Use a single red color
 .save(os.path.join(FIGURES_DIR, 'rose_basic.png')))

# Example 3: Sorted Rose Chart
(data.tidyplot(x='category', y='value')
 .adjust_title('Sorted Nightingale Rose Chart')
 .add_rose(sort=True, show_labels=True, label_type='both')
 .adjust_colors(['#FF4B4B'])  # Use a single red color
 .save(os.path.join(FIGURES_DIR, 'rose_sorted.png')))

# Example 4: Two-Color Rose Chart
(data.tidyplot(x='category', y='value')
 .adjust_title('Two-Color Rose Chart')
 .add_rose(show_labels=True, label_type='value')
 .adjust_colors(['#FF4B4B', '#4B4BFF'])  # Alternate between red and blue
 .save(os.path.join(FIGURES_DIR, 'rose_colors.png')))

# Example 5: Many Categories
np.random.seed(42)  # For reproducible results
many_data = pd.DataFrame({
    'category': [f'Cat{i+1}' for i in range(12)],
    'value': np.random.randint(20, 100, 12)
})

(many_data.tidyplot(x='category', y='value')
 .adjust_title('Rose Chart with Many Categories')
 .add_rose(show_labels=True, label_type='value', label_size=8)
 .adjust_colors(['#FF4B4B'])  # Use a single red color
 .save(os.path.join(FIGURES_DIR, 'rose_many.png')))

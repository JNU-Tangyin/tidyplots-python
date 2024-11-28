"""
Comprehensive test of ALL functions in TidyPlots API using seaborn datasets.
This script tests every single function documented in api.md.
"""

import pandas as pd
import seaborn as sns
import os
import numpy as np
import tidyplots  # Import the package which will monkey-patch pandas

# Create figures directory if it doesn't exist
os.makedirs("figures", exist_ok=True)

# Load all available seaborn datasets
iris = sns.load_dataset("iris")
tips = sns.load_dataset("tips")
titanic = sns.load_dataset("titanic")
planets = sns.load_dataset("planets")
diamonds = sns.load_dataset("diamonds")
flights = sns.load_dataset("flights")

# 1. Basic Plots

# 1.1 Scatter Plot
print("\nCreating scatter plot...")
(iris.tidyplot(x='sepal_length', y='sepal_width', color='species')
 .add_scatter(size=3, alpha=0.7)
 .adjust_labels(title='Scatter: Iris Dimensions',
               x='Sepal Length', y='Sepal Width')
 .adjust_colors('npg')
 .adjust_legend_position('right')
 .save('figures/01_scatter_iris.png'))

# 1.2 Line Plot
monthly_passengers = flights.groupby('year')['passengers'].mean().reset_index()
(monthly_passengers.tidyplot(x='year', y='passengers')
 .add_line(size=1, alpha=1.0)
 .adjust_labels(title='Line: Average Passengers by Year',
               x='Year', y='Passengers')
 .save('figures/02_line_flights.png'))

# 1.3 Bar Plot
(tips.tidyplot(x='day', y='tip')
 .add_bar(stat='identity', width=0.7, alpha=0.7)
 .adjust_labels(title='Bar: Tips by Day',
               x='Day', y='Total Tips')
 .save('figures/03_bar_tips.png'))

# 1.4 Box Plot
(iris.tidyplot(x='species', y='petal_width')
 .add_boxplot(alpha=0.4, outlier_alpha=0.5)
 .adjust_labels(title='Box: Petal Width by Species',
               x='Species', y='Petal Width')
 .save('figures/04_box_iris.png'))

# 1.5 Violin Plot
(iris.tidyplot(x='species', y='petal_length')
 .add_violin(alpha=0.4, draw_quantiles=[0.25, 0.5, 0.75])
 .adjust_labels(title='Violin: Petal Length by Species',
               x='Species', y='Petal Length')
 .save('figures/05_violin_iris.png'))

# 1.6 Density Plot
(tips.tidyplot(x='total_bill')
 .add_density(alpha=0.4)
 .adjust_labels(title='Density: Total Bill Distribution',
               x='Total Bill', y='Density')
 .save('figures/06_density_tips.png'))

# 1.7 Step Plot
tips_sorted = tips.sort_values('tip')
tips_sorted['cumsum'] = tips_sorted['tip'].cumsum()
(tips_sorted.tidyplot(x=range(len(tips)), y='cumsum')
 .add_step(direction='hv')
 .adjust_labels(title='Step: Cumulative Tips',
               x='Count', y='Cumulative Tips')
 .save('figures/07_step_tips.png'))

# 1.8 Dot Plot
(iris.tidyplot(x='petal_length', color='species')
 .add_dotplot(binwidth=0.2, stackdir='up', binaxis='x')
 .adjust_labels(title='Dot: Petal Length Distribution',
               x='Petal Length', y='Count')
 .save('figures/08_dot_iris.png'))

# 2. Statistical Plots

# 2.1 Mean Bar
(tips.tidyplot(x='day', y='tip')
 .add_mean_bar(alpha=0.4, width=0.7)
 .adjust_labels(title='Mean Bar: Average Tips by Day',
               x='Day', y='Average Tip')
 .save('figures/09_mean_bar_tips.png'))

# 2.2 SEM Error Bar
(tips.tidyplot(x='day', y='tip')
 .add_mean_bar(alpha=0.4, width=0.7)
 .add_sem_errorbar(width=0.2)
 .adjust_labels(title='SEM: Tips by Day',
               x='Day', y='Tip Amount')
 .save('figures/10_sem_errorbar_tips.png'))

# 2.3 SD Error Bar
(tips.tidyplot(x='day', y='tip')
 .add_mean_bar(alpha=0.4, width=0.7)
 .add_sd_errorbar(width=0.2)
 .adjust_labels(title='SD: Tips by Day',
               x='Day', y='Tip Amount')
 .save('figures/11_sd_errorbar_tips.png'))

# 2.4 CI Error Bar
(tips.tidyplot(x='day', y='tip')
 .add_mean_bar(alpha=0.4, width=0.7)
 .add_ci_errorbar(width=0.2, ci=0.95)
 .adjust_labels(title='CI: Tips by Day',
               x='Day', y='Tip Amount')
 .save('figures/12_ci_errorbar_tips.png'))

# 2.5 Custom Error Bar
tips_summary = tips.groupby('day').agg({
    'tip': ['mean', lambda x: x.mean() - x.std(), lambda x: x.mean() + x.std()]
}).reset_index()
tips_summary.columns = ['day', 'mean', 'lower', 'upper']
(tips_summary.tidyplot(x='day', y='mean')
 .add_mean_bar(alpha=0.4, width=0.7)
 .add_errorbar(ymin='lower', ymax='upper', width=0.2)
 .adjust_labels(title='Custom Error: Tips by Day',
               x='Day', y='Tip Amount')
 .save('figures/13_custom_errorbar_tips.png'))

# 2.6 Test P-value
(iris.tidyplot(x='species', y='petal_length')
 .add_boxplot(alpha=0.4)
 .add_test_pvalue(test='anova', paired=False)
 .adjust_labels(title='P-value: Petal Length by Species',
               x='Species', y='Petal Length')
 .save('figures/14_pvalue_iris.png'))

# 2.7 Correlation Text
(tips.tidyplot(x='total_bill', y='tip')
 .add_scatter(size=3, alpha=0.7)
 .add_correlation_text(method='pearson', format='.3f')
 .adjust_labels(title='Correlation: Tips vs Total Bill',
               x='Total Bill', y='Tip')
 .save('figures/15_correlation_tips.png'))

# 2.8 Smooth Line
(tips.tidyplot(x='total_bill', y='tip')
 .add_scatter(size=3, alpha=0.7)
 .add_smooth(method='lm', se=True, alpha=0.2)
 .adjust_labels(title='Smooth: Tips vs Total Bill',
               x='Total Bill', y='Tip')
 .save('figures/16_smooth_tips.png'))

# 2.9 Regression Line
(tips.tidyplot(x='total_bill', y='tip')
 .add_scatter(size=3, alpha=0.7)
 .add_regression_line(ci=True, alpha=0.2)
 .adjust_labels(title='Regression: Tips vs Total Bill',
               x='Total Bill', y='Tip')
 .save('figures/17_regression_tips.png'))

# 2.10 Quantiles
(tips.tidyplot(x='total_bill', y='tip')
 .add_scatter(size=3, alpha=0.7)
 .add_quantiles(quantiles=[0.25, 0.5, 0.75], alpha=0.5, color='red')
 .adjust_labels(title='Quantiles: Tips vs Total Bill',
               x='Total Bill', y='Tip')
 .save('figures/18_quantiles_tips.png'))

# 3. Distribution Plots

# 3.1 2D Density
(iris.tidyplot(x='sepal_length', y='sepal_width')
 .add_density_2d(alpha=0.7)
 .adjust_labels(title='2D Density: Sepal Dimensions',
               x='Sepal Length', y='Sepal Width')
 .save('figures/19_density_2d_iris.png'))

# 3.2 2D Density Filled
(iris.tidyplot(x='sepal_length', y='sepal_width')
 .add_density_2d_filled(alpha=0.7)
 .adjust_labels(title='2D Density Filled: Sepal Dimensions',
               x='Sepal Length', y='Sepal Width')
 .save('figures/20_density_2d_filled_iris.png'))

# 3.3 Hex Plot
(tips.tidyplot(x='total_bill', y='tip')
 .add_hex(bins=20)
 .adjust_labels(title='Hex: Tips vs Total Bill',
               x='Total Bill', y='Tip')
 .save('figures/21_hex_tips.png'))

# 3.4 Rug Plot
(tips.tidyplot(x='total_bill', y='tip')
 .add_scatter(size=3, alpha=0.7)
 .add_rug(sides='b', alpha=0.5, length=0.03)
 .adjust_labels(title='Rug: Tips vs Total Bill',
               x='Total Bill', y='Tip')
 .save('figures/22_rug_tips.png'))

# 3.5 Count Plot
(titanic.tidyplot(x='class', color='survived')
 .add_count(stat='count', position='stack')
 .adjust_labels(title='Count: Survival by Class',
               x='Class', y='Count')
 .save('figures/23_count_titanic.png'))

# 4. Data Point Visualizations

# 4.1 Beeswarm
(tips.tidyplot(x='day', y='tip')
 .add_data_points_beeswarm(size=3, alpha=0.5)
 .adjust_labels(title='Beeswarm: Tips by Day',
               x='Day', y='Tip Amount')
 .save('figures/24_beeswarm_tips.png'))

# 4.2 Jitter
(tips.tidyplot(x='day', y='tip')
 .add_data_points_jitter(width=0.2, point_size=3, alpha=0.5)
 .adjust_labels(title='Jitter: Tips by Day',
               x='Day', y='Tip Amount')
 .save('figures/25_jitter_tips.png'))

# 5. Reference Lines and Annotations

# 5.1 Horizontal Line
mean_tip = tips['tip'].mean()
(tips.tidyplot(x='total_bill', y='tip')
 .add_scatter(size=3, alpha=0.7)
 .add_hline(yintercept=mean_tip, linetype='dashed', color='red', alpha=1.0)
 .adjust_labels(title='HLine: Tips with Mean',
               x='Total Bill', y='Tip')
 .save('figures/26_hline_tips.png'))

# 5.2 Vertical Line
median_bill = tips['total_bill'].median()
(tips.tidyplot(x='total_bill', y='tip')
 .add_scatter(size=3, alpha=0.7)
 .add_vline(xintercept=median_bill, linetype='dashed', color='blue', alpha=1.0)
 .adjust_labels(title='VLine: Tips with Median Bill',
               x='Total Bill', y='Tip')
 .save('figures/27_vline_tips.png'))

# 5.3 Text Annotation
(tips.tidyplot(x='total_bill', y='tip')
 .add_scatter(size=3, alpha=0.7)
 .add_text(label='Mean Tip Line', x=20, y=mean_tip,
          ha='right', va='bottom', size=11)
 .add_hline(yintercept=mean_tip, linetype='dashed', color='red')
 .adjust_labels(title='Text: Annotated Tips',
               x='Total Bill', y='Tip')
 .save('figures/28_text_tips.png'))

# 5.4 Ribbon
tips_rolling = pd.DataFrame({
    'x': range(len(tips)),
    'y': tips['tip'].rolling(10).mean(),
    'ymin': tips['tip'].rolling(10).min(),
    'ymax': tips['tip'].rolling(10).max()
}).dropna()
(tips_rolling.tidyplot(x='x', y='y')
 .add_line(size=1, alpha=1.0)
 .add_ribbon(ymin='ymin', ymax='ymax', alpha=0.3)
 .adjust_labels(title='Ribbon: Rolling Tips Range',
               x='Index', y='Tip Amount')
 .save('figures/29_ribbon_tips.png'))

# Test all customization methods
(iris.tidyplot(x='sepal_length', y='sepal_width', color='species')
 .add_scatter(size=3, alpha=0.7)
 .adjust_labels(title='Customization Test',
               x='Sepal Length', y='Sepal Width')
 .adjust_colors('aaas')
 .adjust_legend_position('top')
 .save('figures/30_customization_iris.png'))

# Same plot with removed legend
(iris.tidyplot(x='sepal_length', y='sepal_width', color='species')
 .add_scatter(size=3, alpha=0.7)
 .adjust_labels(title='No Legend Test',
               x='Sepal Length', y='Sepal Width')
 .remove_legend()
 .save('figures/31_no_legend_iris.png'))

# Test adjust_axis_text_angle with long category names
diamonds_cut = diamonds.groupby('cut')['price'].mean().reset_index()
(diamonds_cut.tidyplot(x='cut', y='price')
 .add_bar(alpha=0.7)
 .adjust_labels(title='Bar Plot with Rotated Labels',
               x='Diamond Cut Category', y='Average Price')
 .adjust_axis_text_angle(45)
 .save('figures/32_rotated_labels_diamonds.png'))

print("All API functions have been tested with example plots. Check the 'figures' directory for output.")

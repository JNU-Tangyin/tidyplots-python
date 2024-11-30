"""
Comprehensive test of ALL functions in TidyPlots API using seaborn datasets.
This script tests every single function documented in api.md.
"""
import pandas as pd
import seaborn as sns
import os
import numpy as np
import tidyplots  # Import the package which will monkey-patch pandas
import scipy.stats as stats

# Create figures directory if it doesn't exist
os.makedirs("figures", exist_ok=True)

# Load all available seaborn datasets
iris = sns.load_dataset("iris")
tips = sns.load_dataset("tips")
titanic = sns.load_dataset("titanic")
planets = sns.load_dataset("planets")
diamonds = sns.load_dataset("diamonds")
flights = sns.load_dataset("flights")

# TidyPlots API Examples
# Comprehensive test of ALL functions in TidyPlots API using seaborn datasets.

# 1. Basic Plots

print("\nCreating scatter plot...")
(iris.tidyplot(x='sepal_length', y='sepal_width', fill='species')
 .add_scatter(size=5, alpha=0.7)
 .adjust_labels(title='Scatter: Iris Dimensions',
               x='Sepal Length', y='Sepal Width')
 .adjust_legend_position('right')
 .save('figures/1_scatter.png'))

monthly_passengers = flights.groupby('year', observed=True)['passengers'].mean().reset_index()
(monthly_passengers.tidyplot(x='year', y='passengers', fill='year')
 .add_line(size=1, alpha=1.0)
 .adjust_labels(title='Line: Average Passengers by Year',
               x='Year', y='Passengers')
 .save('figures/1_line.png'))

# 1.3 Bar Plot

(tips.tidyplot(x='day', y='tip', fill='day')
 .add_bar(stat='identity', width=0.7, alpha=0.7)
 .adjust_labels(title='Bar: Tips by Day',
               x='Day', y='Total Tips')
 .save('figures/1.3_bar.png'))

# 1.4 Box Plot

(iris.tidyplot(x='species', y='petal_width', fill='species')
 .add_boxplot(alpha=0.8, outlier_alpha=0.5, width=0.5)
 .add_data_points_beeswarm(size=3, alpha=0.3)
 .adjust_labels(title='Box: Petal Width by Species',
               x='Species', y='Petal Width')
 .save('figures/1.4_box.png'))

# 1.5 Violin Plot

(iris.tidyplot(x='species', y='petal_length', fill='species')
 .add_violin(alpha=0.4, draw_quantiles=[0.25, 0.5, 0.75])
 .add_data_points_jitter(width=0.2, size=3, alpha=0.5)
 .adjust_labels(title='Violin: Petal Length by Species',
               x='Species', y='Petal Length')
 .save('figures/1.5_violin.png'))

# 1.6 Density Plot

(tips.tidyplot(x='total_bill', fill='time')
 .add_density(alpha=0.5)
 .adjust_labels(title='Density: Total Bill Distribution',
               x='Total Bill', y='Density')
 .save('figures/1.6_density.png'))

# 1.7 Step Plot

tips_sorted = tips.sort_values('tip')
tips_sorted['cumsum'] = tips_sorted['tip'].cumsum()
(tips_sorted.tidyplot(x=range(len(tips_sorted)), y='cumsum', fill='day')
 .add_step(direction='hv')
 .adjust_labels(title='Step: Cumulative Tips',
               x='Count', y='Cumulative Tips')
 .save('figures/1.7_step.png'))

# 1.8 Dot Plot

(iris.tidyplot(x='petal_length', fill='species')
 .add_dotplot(binwidth=0.2, stackdir='down', binaxis='x')
 .adjust_labels(title='Dot: Petal Length Distribution',
               x='Petal Length', y='Count')
 .save('figures/1.8_dot.png'))

# 2. Statistical Plots

# 2.1 Mean Bar

(tips.tidyplot(x='day', y='tip', fill='day')
 .add_mean_bar(alpha=0.4, width=0.7)
 .adjust_labels(title='Mean Bar: Average Tips by Day',
               x='Day', y='Average Tip')
 .save('figures/2.1_mean_bar.png'))

# 2.2 SEM Error Bar

(tips.tidyplot(x='day', y='tip', fill='day')
 .add_mean_bar(alpha=0.4, width=0.7)
 .add_sem_errorbar(width=0.2)
 .adjust_labels(title='SEM: Tips by Day',
               x='Day', y='Tip Amount')
 .save('figures/2.2_mean_bar.png'))

# 2.3 SD Error Bar

(tips.tidyplot(x='day', y='tip', fill='day')
 .add_mean_bar(alpha=0.4, width=0.7)
 .add_sd_errorbar(width=0.2)
 .adjust_labels(title='SD: Tips by Day',
               x='Day', y='Tip Amount')
 .save('figures/2.3_mean_bar.png'))

# 2.4 CI Error Bar

(tips.tidyplot(x='day', y='tip', fill='day')
 .add_mean_bar(alpha=0.9, width=0.5)
 .add_ci_errorbar(width=0.2, ci=0.95)
 .adjust_labels(title='CI: Tips by Day',
               x='Day', y='Tip Amount')
 .save('figures/2.4_mean_bar.png'))

# 2.5 Custom Error Bar

tips_summary = tips.groupby('day', observed=True).agg({
    'tip': ['mean', lambda x: x.mean() - x.std(), lambda x: x.mean() + x.std()]
}).reset_index()
tips_summary.columns = ['day', 'mean', 'lower', 'upper']
(tips_summary.tidyplot(x='day', y='mean', fill='day')
 .add_mean_bar(alpha=0.4, width=0.7)
 .add_errorbar(ymin='lower', ymax='upper', width=0.2)
 .adjust_labels(title='Custom Error: Tips by Day',
               x='Day', y='Tip Amount')
 .save('figures/2.5_mean_bar.png'))

# 2.6 Test P-value

(iris.tidyplot(x='species', y='petal_length', fill='species')
 .add_boxplot(alpha=.9, width=0.5)
 .add_data_points_beeswarm(size=3, alpha=0.3)
 .add_test_pvalue(test='anova', paired=True)
 .adjust_labels(title='P-value: Petal Length by Species',
               x='Species', y='Petal Length')
 .save('figures/2.6_box.png'))

# 2.7 Correlation Text

(tips.tidyplot(x='total_bill', y='tip', fill='time')
 .add_scatter(size=5, alpha=0.5)
 .add_correlation_text(method='pearson', format='.3f')
 .adjust_labels(title='Correlation: Tips vs Total Bill',
               x='Total Bill', y='Tip')
 .save('figures/2.7_scatter.png'))

# 2.8 Smooth Line

tips

(tips.tidyplot(x='total_bill', y='tip', fill='time')
 .add_scatter(size=5, alpha=0.5, color='black')
 .add_smooth(method='loess', se=True, alpha=0.2)
 .adjust_labels(title='Smooth: Tips vs Total Bill',
               x='Total Bill', y='Tip')
 .save('figures/2.8_scatter.png'))

# 2.9 Regression Line

(tips.tidyplot(x='total_bill', y='tip', fill='time')
 .add_scatter(size=5, alpha=0.5, color='black')
 .add_regression_line(ci=True, alpha=0.2)
 .adjust_labels(title='Regression: Tips vs Total Bill',
               x='Total Bill', y='Tip')
 .save('figures/2.9_scatter.png'))

# 2.10 Quantiles

(tips.tidyplot(x='total_bill', y='tip', fill='day', color='day')
 .add_scatter(size=5, alpha=0.5)
#  .add_quantiles(quantiles=[0.25, 0.5, 0.75], alpha=0.5, color='red')
 .adjust_labels(title='Quantiles: Tips vs Total Bill',
               x='Total Bill', y='Tip')
 .save('figures/2.10_scatter.png'))

# 3. Distribution Plots

# 3.1 Density 2D Plot

(iris.tidyplot(x='sepal_length', y='sepal_width', fill='species', color='species')
 .add_density_2d(alpha=0.3)
 .add_scatter(size=5, alpha=0.5)
 .adjust_labels(title='Density 2D: Sepal Length vs Width',
               x='Sepal Length', y='Sepal Width')
 .save('figures/3.1_scatter.png'))

# 3.4 Rug Plot

(tips.tidyplot(x='total_bill', y='tip', fill='day', color='day')
 .add_scatter(size=5, alpha=0.5)
 .add_rug(sides='b', alpha=0.5, length=0.03)
 .adjust_labels(title='Rug: Tips vs Total Bill',
               x='Total Bill', y='Tip')
 .save('figures/3.4_scatter.png'))

# 3.5 Count Plot

titanic

(titanic.tidyplot(x='class', color='survived', fill='sex')
 .add_count(stat='count', position='stack')
 .adjust_labels(title='Count: Survival by Class',
               x='Class', y='Count')
 .save('figures/3.5_count.png'))

# 4. Data Point Visualizations

# 4.1 Beeswarm

(tips.tidyplot(x='day', y='tip', fill='sex')
 .add_data_points_beeswarm(size=5, alpha=0.6, color='black')
 .adjust_labels(title='Beeswarm: Tips by Day', x='Day', y='Tip Amount')
 .save('figures/4.1_plot.png'))

# 4.2 Jitter

(tips.tidyplot(x='day', y='tip', fill='sex')
 .add_data_points_jitter(width=0.2, size=5, alpha=0.5)
 .adjust_labels(title='Jitter: Tips by Day', x='Day', y='Tip Amount')
 .save('figures/4.2_plot.png'))

# 5. Reference Lines and Annotations

# 5.1 Horizontal Line

mean_tip = tips['tip'].mean()
(tips.tidyplot(x='total_bill', y='tip', fill='day')
 .add_scatter(size=5, alpha=0.5)
 .add_hline(yintercept=mean_tip, linetype='dashed', color='red', alpha=1.0)
 .adjust_labels(title='HLine: Tips with Mean', x='Total Bill', y='Tip')
 .save('figures/5.1_scatter.png'))

# 5.2 Vertical Line

median_bill = tips['total_bill'].median()
(tips.tidyplot(x='total_bill', y='tip', fill='smoker', color="smoker")
 .add_scatter(size=5, alpha=0.9)
 .add_vline(xintercept=median_bill, linetype='dashed', color='black', alpha=1.0)
 .adjust_labels(title='VLine: Tips with Median Bill',
               x='Total Bill', y='Tip')
 .save('figures/5.2_scatter.png'))

# 5.3 Text Annotation

(tips.tidyplot(x='total_bill', y='tip', fill='day')
 .add_scatter(size=5, alpha=0.5)
 .add_text(label='Mean Tip Line', x=12, y=mean_tip,
          ha='right', va='bottom', size=11)
 .add_hline(yintercept=mean_tip, linetype='dashed', color='red')
 .adjust_labels(title='Text: Annotated Tips', x='Total Bill', y='Tip')
 .save('figures/5.3_scatter.png'))

# 5.4 Ribbon

tips_rolling = pd.DataFrame({
    'x': range(len(tips)),
    'y': tips['tip'],#.rolling(10).mean(),
    'ymin': tips['tip'].rolling(20).min(),
    'ymax': tips['tip'].rolling(20).max()
}).dropna()
(tips_rolling.tidyplot(x='x', y='y')
 .add_line(size=1, alpha=.8, color='cyan')
 .add_ribbon(ymin='ymin', ymax='ymax', alpha=0.1, color='grey')
 .adjust_labels(title='Ribbon: Rolling Tips Range', x='Index', y='Tip Amount')
 .save('figures/5.4.1_line.png'))

# Test all customization methods

(iris.tidyplot(x='sepal_length', y='sepal_width', fill='species')
 .add_scatter(size=5, alpha=0.5)
 .add_density_2d(alpha=0.1)
 .adjust_labels(title='Customization Test',
               x='Sepal Length', y='Sepal Width')
 .adjust_colors(['#1f77b4', '#ff7f0e', '#2ca02c'])
 .adjust_legend_position('right')
 .save('figures/5.4.2_scatter.png'))

# Same plot with removed legend

(iris.tidyplot(x='sepal_length', y='sepal_width', color ='species')
 .add_scatter(size=5, alpha=0.5)
 .add_density_2d(alpha=0.1)
 .adjust_labels(title='No Legend Test', x='Sepal Length', y='Sepal Width')
 .remove_legend()
 .save('figures/5.4.3_scatter.png'))

# Test adjust_axis_text_angle with long category names

diamonds_cut = diamonds.groupby('cut', observed=True)['price'].mean().reset_index()
(diamonds_cut.tidyplot(x='cut', fill='cut')
 .add_bar(stat='count')
 .sort_x_axis_labels('ascending')
 .adjust_axis_text_angle(45)
 .save('figures/8.1_bar.png'))

# Test rename_x_axis_labels
cut_rename = {'Fair': 'Low Grade', 'Good': 'Medium Grade', 
              'Very Good': 'High Grade', 'Premium': 'Premium Grade', 
              'Ideal': 'Ideal Grade'}
(diamonds_cut.tidyplot(x='cut', fill='cut')
 .add_bar(stat='count')
 .rename_x_axis_labels(cut_rename)
 .adjust_labels(title='Diamond Prices by Grade')
 .adjust_axis_text_angle(45)
 .save('figures/8.2_bar.png'))

# 3. Sum Functions

print("\nTesting sum functions...")

# Group tips by day

tips_by_day = tips.groupby('day', observed=True)['total_bill'].sum().reset_index()
(tips_by_day.tidyplot(x='day', y='total_bill', fill='day')
 .add_sum_line()
 .add_sum_dot(size=5, alpha=0.5)
 .adjust_labels(title='Sum Line with Dots: Total Bills by Day')
 .save('figures/3_plot.png'))

# 4. Median Functions

tips_median = tips.groupby('day', observed=True)['total_bill'].median().reset_index()
(tips_median.tidyplot(x='day', y='total_bill', fill='day')
 .add_median_bar()
 .adjust_labels(title='Median Bar: Bills by Day')
 .save('figures/4_plot.png'))


(tips.tidyplot(x='total_bill', y='tip', fill='day', color='day')
 .add_scatter(size=5, alpha=0.5)
 .add_curve_fit()
 .adjust_labels(title='Curve Fit: Tips vs Total Bill')
 .save('figures/4_scatter.png'))

# 5. Ribbon Functions

print("\nTesting ribbon functions...")

# Create time series data

np.random.seed(42)
dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
values = np.random.normal(loc=10, scale=2, size=len(dates))
ts_data = pd.DataFrame({'date': dates, 'value': values})
(ts_data.tidyplot(x='date', y='value')
#  .add_line(alpha=0.2)
 .add_scatter(size=3, alpha=0.5)
 .add_sem_ribbon()
 .adjust_labels(title='Time Series with SEM Ribbon')
 .save('figures/5.1_scatter.png'))


(ts_data.tidyplot(x='date', y='value')
#  .add_line(alpha=0.2)
 .add_scatter(size=3, alpha=0.5)
 .add_ci95_ribbon()
 .adjust_labels(title='Time Series with 95% CI Ribbon')
 .save('figures/5.2_scatter.png'))

# 6. Stack Functions

print("\nTesting stack functions...")

# Calculate survival rates by class

titanic_class = (titanic.groupby(['class', 'survived'], observed=True)
                 .size()
                 .unstack()
                 .fillna(0))
titanic_class.columns = ['Not Survived', 'Survived']
titanic_class = titanic_class.reset_index()

# Calculate percentages

total = titanic_class['Not Survived'] + titanic_class['Survived']
titanic_class['Survived %'] = titanic_class['Survived'] / total * 100
titanic_class['Not Survived %'] = titanic_class['Not Survived'] / total * 100

# Melt for plotting

titanic_relative = pd.melt(titanic_class, 
                          id_vars=['class'],
                          value_vars=['Survived %', 'Not Survived %'],
                          var_name='Status',
                          value_name='Percentage')
titanic_absolute = pd.melt(titanic_class,
                          id_vars=['class'],
                          value_vars=['Survived', 'Not Survived'],
                          var_name='Status',
                          value_name='Count')
(titanic_relative.tidyplot(x='class', y='Percentage', fill='Status')
 .add_barstack_relative()
 .adjust_labels(title='Survival Rate by Class',
               y='Percentage')
 .save('figures/6.1_bar.png'))


(titanic_absolute.tidyplot(x='class', y='Count', fill='Status')
 .add_barstack_absolute()
 .adjust_labels(title='Survival Count by Class', y='Count')
 .save('figures/6.2_bar.png'))

# 7. Pie and Donut Charts

titanic

# print("\nTesting pie and donut charts...")
class_counts = titanic['class'].value_counts().reset_index()
class_counts.columns = ['class', 'count']
(class_counts.tidyplot(x='class', y='count', fill='class')
 .add_pie()
 .adjust_labels(title='Passenger Distribution by Class')
 .save('figures/7.1_pie.png'))


(class_counts.tidyplot(x='class', y='count', fill='class')
 .add_donut()
 .adjust_labels(title='Passenger Distribution by Class (Donut)')
 .save('figures/7.2_plot.png'))

# 8. Advanced Label Management

print("\nTesting label management functions...")

# Sort diamonds by price

diamonds_sorted = diamonds.groupby('cut', observed=True)['price'].mean().reset_index()
(diamonds_sorted.tidyplot(x='cut', fill='cut')
 .add_bar(stat='count')
 .sort_x_axis_labels('ascending')
 .add_data_labels_repel()
 .adjust_axis_text_angle(45)
 .save('figures/8.1_bar.png'))

# Test label renaming

cut_rename = {'Fair': 'Low Grade', 'Good': 'Medium Grade', 
              'Very Good': 'High Grade', 'Premium': 'Premium Grade', 
              'Ideal': 'Ideal Grade'}
(diamonds_sorted.tidyplot(x='cut', fill='cut')
 .add_bar(stat='count')
 .rename_x_axis_labels(cut_rename)
 .adjust_labels(title='Diamond Prices by Grade')
 .adjust_axis_text_angle(45)
 .save('figures/8.2_bar.png'))

print("\nAll examples have been generated in the 'figures' directory.")

print("\nAll examples have been generated in the 'figures' directory.")

# 7. Additional Plot Types

# 7.1 Hexbin Plot
print("\nCreating hexbin plot...")
(iris.tidyplot(x='sepal_length', y='sepal_width', fill='species')
 .add_hex(bins=20)
 .adjust_labels(title='Hexbin: Sepal Dimensions',
               x='Sepal Length', y='Sepal Width')
 .save('figures/7.1_hexbin.png'))

# 7.2 Filled 2D Density
(iris.tidyplot(x='sepal_length', y='sepal_width', fill='species')
 .add_density_2d_filled(alpha=0.4)
 .adjust_labels(title='Filled 2D Density: Sepal Dimensions',
               x='Sepal Length', y='Sepal Width')
 .save('figures/7.2_density_2d_filled.png'))

# 7.3 Sum Statistics
tips_by_day = tips.groupby('day')['total_bill'].sum().reset_index()

print("\nCreating sum statistics plots...")
(tips_by_day.tidyplot(x='day', y='total_bill', fill='day')
 .add_sum_bar(width=0.7, alpha=0.7)
 .add_sum_value(size=11, format="%.1f")
 .adjust_labels(title='Sum Bar with Values: Total Bills by Day',
               x='Day', y='Total Bills')
 .save('figures/7.3.1_sum_bar_value.png'))

(tips_by_day.tidyplot(x='day', y='total_bill', fill='day')
 .add_sum_line(size=1, alpha=1)
 .add_sum_dot(size=3, alpha=0.7)
 .adjust_labels(title='Sum Line with Dots: Total Bills by Day',
               x='Day', y='Total Bills')
 .save('figures/7.3.2_sum_line_dot.png'))

(tips_by_day.tidyplot(x='day', y='total_bill', fill='day')
 .add_sum_area(alpha=0.7)
 .adjust_labels(title='Sum Area: Total Bills by Day',
               x='Day', y='Total Bills')
 .save('figures/7.3.3_sum_area.png'))

# 7.4 Median Statistics
print("\nCreating median statistics plots...")
(tips_by_day.tidyplot(x='day', y='total_bill', fill='day')
 .add_median_bar(width=0.7, alpha=0.7)
 .add_median_value(size=11, format="%.1f")
 .adjust_labels(title='Median Bar: Bills by Day',
               x='Day', y='Median Bills')
 .save('figures/7.4.1_median_bar_value.png'))

(tips_by_day.tidyplot(x='day', y='total_bill', fill='day')
 .add_median_line(size=1, alpha=1)
 .add_median_dot(size=3, alpha=0.7)
 .adjust_labels(title='Median Line with Dots: Bills by Day',
               x='Day', y='Median Bills')
 .save('figures/7.4.2_median_line_dot.png'))

(tips_by_day.tidyplot(x='day', y='total_bill', fill='day')
 .add_median_area(alpha=0.7)
 .adjust_labels(title='Median Area: Bills by Day',
               x='Day', y='Median Bills')
 .save('figures/7.4.3_median_area.png'))

# 7.5 Curve Fitting
print("\nCreating curve fit plot...")
(tips.tidyplot(x='total_bill', y='tip', fill='day')
 .add_scatter(size=3, alpha=0.5)
 .add_curve_fit()
 .adjust_labels(title='Curve Fit: Tips vs Total Bill',
               x='Total Bill', y='Tip')
 .save('figures/7.5_curve_fit.png'))

# 7.6 Statistical Ribbons
# Generate time series data
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
n_samples = 10
data = []
for date in dates:
    base = 100 + 20 * np.sin(date.dayofyear * 2 * np.pi / 365)
    for _ in range(n_samples):
        value = base + np.random.normal(0, 5)
        data.append({'date': date, 'value': value})
ts_data = pd.DataFrame(data)

print("\nCreating statistical ribbon plots...")
ts_data.tidyplot(x='date', y='value')
    .add_line(size=1, alpha=.1, color='grey')
    .add_sem_ribbon(alpha=0.1, color='navy', size=2)
    .adjust_labels(title='Time Series with SEM Ribbon',
                x='Date', y='Value')
    .save('figures/7.6.1_sem_ribbon.png'))

(ts_data.tidyplot(x='date', y='value')
 .add_line(size=1, alpha=1)
 .add_range_ribbon(alpha=0.2)
 .adjust_labels(title='Time Series with Range Ribbon',
               x='Date', y='Value')
 .save('figures/7.6.2_range_ribbon.png'))

(ts_data.tidyplot(x='date', y='value')
 .add_line(size=1, alpha=1)
 .add_sd_ribbon(alpha=0.2)
 .adjust_labels(title='Time Series with SD Ribbon',
               x='Date', y='Value')
 .save('figures/7.6.3_sd_ribbon.png'))

(ts_data.tidyplot(x='date', y='value')
 .add_line(size=1, alpha=1)
 .add_ci95_ribbon(alpha=0.2)
 .adjust_labels(title='Time Series with 95% CI Ribbon',
               x='Date', y='Value')
 .save('figures/7.6.4_ci95_ribbon.png'))

# 7.7 Stacked Plots
survival_data = titanic.groupby(['class', 'survived']).size().reset_index(name='count')

print("\nCreating stacked plots...")
(survival_data.tidyplot(x='class', y='count', fill='survived')
 .add_barstack_absolute(width=0.7, alpha=0.7)
 .adjust_labels(title='Absolute Stacked Bars: Survival by Class',
               x='Class', y='Count')
 .save('figures/7.7.1_barstack_absolute.png'))

(survival_data.tidyplot(x='class', y='count', fill='survived')
 .add_barstack_relative(width=0.7, alpha=0.7)
 .adjust_labels(title='Relative Stacked Bars: Survival by Class',
               x='Class', y='Proportion')
 .save('figures/7.7.2_barstack_relative.png'))

# Create time series data for area stacks
class_counts = titanic.groupby(['class']).size()
dates = pd.date_range('2023-01-01', periods=len(class_counts), freq='M')
area_data = pd.DataFrame({
    'date': dates.repeat(len(class_counts)),
    'class': np.tile(class_counts.index, len(dates)),
    'count': np.tile(class_counts.values, len(dates))
})

(area_data.tidyplot(x='date', y='count', fill='class')
 .add_areastack_absolute(alpha=0.7)
 .adjust_labels(title='Absolute Stacked Areas',
               x='Date', y='Count')
 .save('figures/7.7.3_areastack_absolute.png'))

(area_data.tidyplot(x='date', y='count', fill='class')
 .add_areastack_relative(alpha=0.7)
 .adjust_labels(title='Relative Stacked Areas',
               x='Date', y='Proportion')
 .save('figures/7.7.4_areastack_relative.png'))

# 7.8 Pie and Donut Charts
class_distribution = titanic.groupby('class').size().reset_index(name='count')

print("\nCreating pie and donut charts...")
(class_distribution.tidyplot(x='class', y='count', fill='class')
 .add_pie()
 .adjust_labels(title='Passenger Distribution by Class')
 .save('figures/7.8.1_pie.png'))

(class_distribution.tidyplot(x='class', y='count', fill='class')
 .add_donut(inner_radius=0.5)
 .adjust_labels(title='Passenger Distribution by Class (Donut)')
 .save('figures/7.8.2_donut.png'))

# 7.9 Data Labels with Repulsion
tips_sample = tips.sample(n=10, random_state=42)
(tips_sample.tidyplot(x='total_bill', y='tip', fill='day')
 .add_scatter(size=5, alpha=0.7)
 .add_data_labels_repel(size=8)
 .adjust_labels(title='Tips with Repelled Labels',
               x='Total Bill', y='Tip')
 .save('figures/7.9_data_labels_repel.png'))

# 8. Advanced Customization

# 8.1 Title and Axis Customization
print("\nCreating customized plots...")
p = (tips.tidyplot(x='day', y='tip', fill='day')
     .add_boxplot(alpha=0.7))

# Apply various customizations
p = (p.adjust_title('Daily Tip Distribution', size=16)
     .adjust_x_axis_title('Day of Week', size=12)
     .adjust_y_axis_title('Tip Amount ($)', size=12)
     .adjust_caption('Data source: Seaborn tips dataset', size=10)
     .adjust_size(10, 6)
     .adjust_padding(left=0.1, right=0.1, top=0.1, bottom=0.1))

# Save the customized plot
p.save('figures/8.1_customized_plot.png')

# 8.2 Axis Manipulation
diamonds_cut = diamonds.groupby('cut')['price'].mean().reset_index()

# Create mapping for renaming
cut_rename = {
    'Fair': 'Grade 1 - Fair',
    'Good': 'Grade 2 - Good',
    'Very Good': 'Grade 3 - Very Good',
    'Premium': 'Grade 4 - Premium',
    'Ideal': 'Grade 5 - Ideal'
}

(diamonds_cut.tidyplot(x='cut', fill='cut')
 .add_bar(stat='count', alpha=.8)
 .adjust_labels(title='Bar Plot with Rotated Labels', x='Diamond Cut Category', y='Average Price')
 .adjust_axis_text_angle(45)
 .adjust_colors("Set1")
 .rename_x_axis_labels(cut_rename)
 .save('figures/8.2_axis_manipulation.png'))

# 8.3 Label Ordering
print("\nCreating plots with ordered labels...")
# Sort tips by day total
tips_by_day_sorted = tips.groupby('day')['total_bill'].sum().reset_index()

(tips_by_day_sorted.tidyplot(x='day', y='total_bill', fill='day')
 .add_bar(stat='identity', alpha=0.7)
 .sort_x_axis_labels(ascending=False)
 .adjust_labels(title='Total Bills by Day (Sorted)',
               x='Day', y='Total Bill')
 .save('figures/8.3.1_sorted_labels.png'))

# Reorder specific labels
custom_order = ['Thur', 'Fri', 'Sat', 'Sun']
(tips_by_day_sorted.tidyplot(x='day', y='total_bill', fill='day')
 .add_bar(stat='identity', alpha=0.7)
 .reorder_x_axis_labels(custom_order)
 .adjust_labels(title='Total Bills by Day (Custom Order)',
               x='Day', y='Total Bill')
 .save('figures/8.3.2_reordered_labels.png'))

# 8.4 Statistical Annotations
print("\nCreating plots with statistical annotations...")
# Add p-value bracket
(iris.tidyplot(x='species', y='sepal_length', fill='species')
 .add_boxplot(alpha=0.7)
 .add_pvalue(0.001, 0, 2, 8, height=0.2, format='stars')
 .adjust_labels(title='Sepal Length by Species with P-value',
               x='Species', y='Sepal Length')
 .save('figures/8.4_pvalue_annotation.png'))

print("\nAll examples have been generated in the 'figures' directory.")

# 9. Additional Statistical Functions
print("\nTesting additional statistical functions...")

# Test sum dash
(tips.tidyplot(x='day', y='tip', fill='day')
 .add_sum_dash(width=0.5, alpha=0.8)
 .adjust_labels(title='Sum Dash: Tips by Day')
 .save('figures/9.1_sum_dash.png'))

# Test median dash
(tips.tidyplot(x='day', y='tip', fill='day')
 .add_median_dash(width=0.5, alpha=0.8)
 .adjust_labels(title='Median Dash: Tips by Day')
 .save('figures/9.2_median_dash.png'))

# Test heatmap
tips_pivot = tips.pivot_table(index='day', columns='time', values='total_bill', aggfunc='mean')
(tips_pivot.reset_index().melt(id_vars=['day'])
 .tidyplot(x='day', y='time', fill='value')
 .add_heatmap(alpha=0.7)
 .adjust_labels(title='Heatmap: Average Bill by Day and Time')
 .save('figures/9.3_heatmap.png'))

# 10. Advanced Axis Manipulation
print("\nTesting advanced axis manipulation...")

# Test axis adjustments
(tips.tidyplot(x='total_bill', y='tip', fill='time')
 .add_scatter(alpha=0.5)
 .adjust_x_axis(limits=(0, 60), breaks=list(range(0, 61, 10)))
 .adjust_y_axis(limits=(0, 10), breaks=list(range(0, 11, 2)))
 .adjust_title('Custom Axis Settings')
 .adjust_x_axis_title('Total Bill ($)')
 .adjust_y_axis_title('Tip Amount ($)')
 .adjust_caption('Data from tips dataset')
 .adjust_size(10, 6)
 .adjust_padding(left=0.15, right=0.15)
 .save('figures/10.1_axis_adjustments.png'))

# 11. Advanced Label Management
print("\nTesting advanced label management...")

# Test label renaming
day_rename = {'Thur': 'Thursday', 'Fri': 'Friday', 'Sat': 'Saturday', 'Sun': 'Sunday'}
(tips.tidyplot(x='day', y='tip', fill='day')
 .add_boxplot()
 .rename_x_axis_labels(day_rename)
 .rename_color_labels(day_rename)
 .adjust_labels(title='Renamed Labels')
 .save('figures/11.1_renamed_labels.png'))

# Test label reordering
custom_order = ['Sunday', 'Saturday', 'Friday', 'Thursday']
(tips.tidyplot(x='day', y='tip', fill='day')
 .add_boxplot()
 .rename_x_axis_labels(day_rename)
 .reorder_x_axis_labels(custom_order)
 .adjust_labels(title='Reordered Labels')
 .save('figures/11.2_reordered_labels.png'))

# Test label sorting
(tips.tidyplot(x='day', y='tip', fill='day')
 .add_boxplot()
 .sort_x_axis_labels(ascending=True)
 .adjust_labels(title='Sorted Labels')
 .save('figures/11.3_sorted_labels.png'))

# Test label reversing
(tips.tidyplot(x='day', y='tip', fill='day')
 .add_boxplot()
 .reverse_x_axis_labels()
 .adjust_labels(title='Reversed Labels')
 .save('figures/11.4_reversed_labels.png'))

# 12. P-value with Bracket
print("\nTesting p-value with bracket...")

# Calculate p-value between two groups
group1 = tips[tips['day'] == 'Thur']['tip']
group2 = tips[tips['day'] == 'Fri']['tip']
t_stat, p_val = stats.ttest_ind(group1, group2)

# Add p-value with bracket
(tips[tips['day'].isin(['Thur', 'Fri'])].tidyplot(x='day', y='tip', fill='day')
 .add_boxplot()
 .add_pvalue(p_val, x1=0, x2=1, y=10, height=0.5)
 .adjust_labels(title='P-value with Bracket')
 .save('figures/12.1_pvalue_bracket.png'))

print("\nAll examples have been generated in the 'figures' directory.")

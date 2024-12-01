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
 .add_scatter(size=5, alpha=1)
 .adjust_labels(title='Scatter: Iris Dimensions',
               x='Sepal Length', y='Sepal Width')
 .adjust_legend_position('right')
 .save('figures/1_scatter.png'))

monthly_passengers = flights.groupby('year', observed=True)['passengers'].mean().reset_index()
(monthly_passengers.tidyplot(x='year', y='passengers', fill='year')
 .add_line(size=1, alpha=1)
 .adjust_labels(title='Line: Average Passengers by Year',
               x='Year', y='Passengers')
 .save('figures/1_line.png'))

# 1.3 Bar Plot
(tips.tidyplot(x='day', y='tip', fill='day')
 .add_bar(stat='identity', width=0.7, alpha=1)
 .adjust_labels(title='Bar: Tips by Day',
               x='Day', y='Total Tips')
 .save('figures/1.3_bar.png'))

# 1.4 Box Plot
(tips.tidyplot(x='day', y='tip', fill='day')
 .add_boxplot(alpha=1)
 .adjust_labels(title='Box: Tips by Day',
               x='Day', y='Tips')
 .save('figures/1.4_box.png'))

# 1.5 Violin Plot
(tips.tidyplot(x='day', y='tip', fill='day')
 .add_violin(alpha=1)
 .adjust_labels(title='Violin: Tips by Day',
               x='Day', y='Tips')
 .save('figures/1.5_violin.png'))

# 1.6 Density Plot
(tips.tidyplot(x='total_bill', fill='time')
 .add_density(alpha=1)
 .adjust_labels(title='Density: Bill Distribution by Time',
               x='Total Bill', y='Density')
 .save('figures/1.6_density.png'))

# 1.7 Hex Plot
(iris.tidyplot(x='sepal_length', y='sepal_width', fill='species')
 .add_hex(bins=20)
 .adjust_labels(title='Hex: Iris Dimensions',
               x='Sepal Length', y='Sepal Width')
 .save('figures/1.7_hex.png'))

# 1.8 Error Bar Plot
tips_summary = tips.groupby('day', observed=True).agg({
    'tip': ['mean', 'std']
}).reset_index()
tips_summary.columns = ['day', 'mean', 'std']
tips_summary['ymin'] = tips_summary['mean'] - tips_summary['std']
tips_summary['ymax'] = tips_summary['mean'] + tips_summary['std']

(tips_summary.tidyplot(x='day', y='mean', fill='day')
 .add_errorbar(ymin='ymin', ymax='ymax')
 .adjust_labels(title='Error Bar: Tips by Day',
               x='Day', y='Tips (Mean ± SD)')
 .save('figures/1.8_errorbar.png'))

# 1.9 Jitter Plot
(iris.tidyplot(x='species', y='sepal_length', fill='species')
 .add_data_points_jitter(size=5, alpha=1)
 .adjust_labels(title='Jitter: Sepal Length by Species',
               x='Species', y='Sepal Length')
 .save('figures/1.9_jitter.png'))

# 2. Statistical Plots

print("\nCreating statistical plots...")
# 2.1 Mean Bar
(tips.tidyplot(x='day', y='tip', fill='day')
 .add_mean_bar()
 .adjust_labels(title='Mean Bar: Tips by Day',
               x='Day', y='Mean Tips')
 .save('figures/2.1_mean_bar.png'))

# 2.2 SEM Error Bar
(tips.tidyplot(x='day', y='tip', fill='day')
 .add_sem_errorbar()
 .adjust_labels(title='SEM Error Bar: Tips by Day',
               x='Day', y='Tips (Mean ± SEM)')
 .save('figures/2.2_sem_errorbar.png'))

# 2.3 SD Error Bar
(tips.tidyplot(x='day', y='tip', fill='smoker')
 .add_sd_errorbar()
 .adjust_labels(title='SD Error Bar: Tips by Day',
               x='Day', y='Tips (Mean ± SD)')
 .save('figures/2.3_sd_errorbar.png'))

# 2.4 CI Error Bar
(tips.tidyplot(x='day', y='tip', fill='sex')
 .add_ci_errorbar()
 .adjust_labels(title='CI Error Bar: Tips by Day',
               x='Day', y='Tips (Mean ± 95% CI)')
 .save('figures/2.4_ci_errorbar.png'))

# 2.5 Statistical Test P-value
(iris.tidyplot(x='species', y='sepal_length', fill='species')
 .add_boxplot()
 .add_test_pvalue(test='anova')
 .adjust_labels(title='P-value: Sepal Length by Species',
               x='Species', y='Sepal Length')
 .save('figures/2.5_pvalue.png'))

# 2.6 Correlation Text
(iris.tidyplot(x='sepal_length', y='sepal_width', fill='species')
 .add_scatter()
 .add_correlation_text()
 .adjust_labels(title='Correlation: Sepal Dimensions',
               x='Sepal Length', y='Sepal Width')
 .save('figures/2.6_correlation.png'))

# 2.7 Regression Line
(iris.tidyplot(x='sepal_length', y='sepal_width', color='species')
 .add_scatter()
 .add_regression_line()
 .adjust_labels(title='Regression: Sepal Dimensions',
               x='Sepal Length', y='Sepal Width')
 .save('figures/2.7_regression.png'))

# 2.8 Quantile Lines
(iris.tidyplot(x='sepal_length', y='sepal_width', color='species')
 .add_scatter()
 .add_quantiles()
 .adjust_labels(title='Quantiles: Sepal Dimensions',
               x='Sepal Length', y='Sepal Width')
 .save('figures/2.8_quantiles.png'))

# 3. Advanced Plots

print("\nCreating advanced plots...")
# 3.1 2D Density Contours
(iris.tidyplot(x='sepal_length', y='sepal_width', color='species')
 .add_density_2d()
 .adjust_labels(title='2D Density: Sepal Dimensions',
               x='Sepal Length', y='Sepal Width')
 .save('figures/3.1_density_2d.png'))

# 3.2 2D Density Filled
(iris.tidyplot(x='sepal_length', y='sepal_width', fill='species')
 .add_density_2d_filled()
 .adjust_labels(title='2D Density Filled: Sepal Dimensions',
               x='Sepal Length', y='Sepal Width')
 .save('figures/3.2_density_2d_filled.png'))

# 3.3 Dot Plot
(tips.tidyplot(x='total_bill', fill='time')
 .add_dotplot()
 .adjust_labels(title='Dot Plot: Bill Distribution',
               x='Total Bill', y='Count')
 .save('figures/3.3_dotplot.png'))

# 3.4 Step Plot
(flights.tidyplot(x='year', y='passengers', fill='year')
 .add_step()
 .adjust_labels(title='Step: Passengers Over Time',
               x='Year', y='Passengers')
 .save('figures/3.4_step.png'))

# 3.5 Rug Plot
(iris.tidyplot(x='sepal_length', y='sepal_width', fill='species')
 .add_scatter()
 .add_rug()
 .adjust_labels(title='Rug: Sepal Dimensions',
               x='Sepal Length', y='Sepal Width')
 .save('figures/3.5_rug.png'))

# 3.6 Count Plot
(tips.tidyplot(x='day', fill='time')
 .add_count()
 .adjust_labels(title='Count: Tips by Day',
               x='Day', y='Count')
 .save('figures/3.6_count.png'))

# 3.7 Beeswarm Plot
(iris.tidyplot(x='species', y='sepal_length', fill='species')
 .add_data_points_beeswarm()
 .adjust_labels(title='Beeswarm: Sepal Length by Species',
               x='Species', y='Sepal Length')
 .save('figures/3.7_beeswarm.png'))

# 4. Annotations and Lines

print("\nCreating annotations and lines...")
mean_bill = tips['total_bill'].mean()
(tips.tidyplot(x='total_bill', fill='time')
 .add_density()
 .add_vline(xintercept=mean_bill)
 .adjust_labels(title='Vertical Line: Bill Distribution',
               x='Total Bill', y='Density')
 .save('figures/4.1_vline.png'))

# 4.2 Text Annotation
(iris.tidyplot(x='sepal_length', y='sepal_width', fill='species')
 .add_scatter()
 .add_text(label='Correlation', x=5, y=4)
 .adjust_labels(title='Text: Sepal Dimensions',
               x='Sepal Length', y='Sepal Width')
 .save('figures/4.2_text.png'))

# 4.3 Ribbon Plot
tips_summary = tips.groupby('day', observed=True).agg({
    'tip': ['mean', 'std']
}).reset_index()
tips_summary.columns = ['day', 'mean', 'std']
tips_summary['ymin'] = tips_summary['mean'] - tips_summary['std']
tips_summary['ymax'] = tips_summary['mean'] + tips_summary['std']

(tips_summary.tidyplot(x='day', y='mean', fill='day')
 .add_ribbon(ymin='ymin', ymax='ymax')
 .adjust_labels(title='Ribbon: Tips by Day',
               x='Day', y='Tips (Mean ± SD)')
 .save('figures/4.3_ribbon.png'))

# 5. Theme and Style

print("\nTesting theme and style modifications...")
# 5.1 Color Palette
(iris.tidyplot(x='species', y='sepal_length', fill='species')
 .add_boxplot()
 .adjust_colors('Set2')
 .adjust_labels(title='Custom Colors: Sepal Length by Species',
               x='Species', y='Sepal Length')
 .save('figures/5.1_colors.png'))

# 5.2 Axis Text Angle
(tips.tidyplot(x='day', y='tip', fill='day')
 .add_bar()
 .adjust_axis_text_angle(45)
 .adjust_labels(title='Angled Text: Tips by Day',
               x='Day', y='Tips')
 .save('figures/5.2_text_angle.png'))

# 5.3 Legend Position
(iris.tidyplot(x='sepal_length', y='sepal_width', color='species', fill='species')
 .add_scatter()
 .adjust_legend_position('top')
 .adjust_labels(title='Legend Position Test',
               x='Sepal Length', y='Sepal Width')
 .save('figures/5.3_legend_position.png'))

# 5.4 No Legend
(iris.tidyplot(x='sepal_length', y='sepal_width', color='species', fill='species')
 .add_scatter()
 .remove_legend()
 .adjust_labels(title='No Legend Test',
               x='Sepal Length', y='Sepal Width')
 .save('figures/5.4_no_legend.png'))

# 6. Additional Features

print("\nTesting additional features...")
# 6.1 Faceting by Single Variable
(tips.tidyplot(x='day', y='tip', fill='day', split_by='time')
 .add_boxplot()
 .adjust_labels(title='Faceted Box Plot: Tips by Day and Time',
               x='Day', y='Tips')
 .save('figures/6.1_facet_single.png'))

# 6.2 Sorting
diamonds_sorted = diamonds.copy()
(diamonds_sorted.tidyplot(x='cut', fill='cut')
 .add_bar(stat='count')
 .sort_x_axis_labels(ascending=True)
 .adjust_axis_text_angle(45)
 .adjust_labels(title='Sorted Bar Plot: Diamond Cuts',
               x='Cut', y='Count')
 .save('figures/6.2_sorting.png'))

# 7. Statistical Summaries

print("\nTesting statistical summaries...")
# 7.1 Sum Bar
(tips.tidyplot(x='day', y='tip', fill='day')
 .add_sum_bar()
 .adjust_labels(title='Sum Bar: Total Tips by Day',
               x='Day', y='Total Tips')
 .save('figures/7.1_sum_bar.png'))

# 7.2 Median Bar
(tips.tidyplot(x='day', y='tip', fill='day')
 .add_median_bar()
 .adjust_labels(title='Median Bar: Median Tips by Day',
               x='Day', y='Median Tips')
 .save('figures/7.2_median_bar.png'))

# 8. Stacked Plots

print("\nCreating stacked plots...")
survival_data = titanic.groupby(['class', 'survived'], observed=True).size().reset_index(name='count')

# 8.1 Absolute Stacked Bar
(survival_data.tidyplot(x='class', y='count', fill='survived')
 .add_barstack_absolute()
 .adjust_labels(title='Stacked Bar: Survival by Class',
               x='Class', y='Count')
 .save('figures/8.1_stack_absolute.png'))

# 8.2 Relative Stacked Bar
(survival_data.tidyplot(x='class', y='count', fill='survived')
 .add_barstack_relative()
 .adjust_labels(title='Relative Stacked Bar: Survival by Class',
               x='Class', y='Proportion')
 .save('figures/8.2_stack_relative.png'))

print("\nAll examples have been generated in the 'figures' directory.")

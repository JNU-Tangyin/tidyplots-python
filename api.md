# TidyPlots Python API Reference

TidyPlots is a lightweight, publication-ready plotting library for Python, inspired by R's ggplot2. It provides a clean, intuitive interface for creating beautiful statistical visualizations.

## Installation

```bash
pip install tidyplots-python
```

## Quick Start

```python
import seaborn as sns
import tidyplots

# Create a plot
iris = sns.load_dataset("iris")
(iris.tidyplot(x='time', y='value')
   .add_line()
   .add_scatter()
   .adjust_labels(title='Time Series Plot'))
```

## Core API

### TidyPlot Class

#### Constructor

```python
TidyPlot(data: pd.DataFrame, x: str, y: str = None, color: Optional[str] = None)
```

Creates a new TidyPlot object.

Parameters:

- `data`: Input DataFrame
- `x`: Column name for x-axis
- `y`: Column name for y-axis (optional for count plots)
- `color`: Column name for color grouping (optional)

### Data Visualization Methods

#### Basic Plots

##### add_scatter

```python
add_scatter(size: float = 3, alpha: float = 0.7)
```

Creates a scatter plot.

##### add_line

```python
add_line(size: float = 1, alpha: float = 1.0)
```

Creates a line plot.

##### add_bar

```python
add_bar(stat: str = 'identity', width: float = 0.7, alpha: float = 0.7)
```

Creates a bar plot.

- `stat`: Type of bar plot ('identity', 'count', 'sum')
- `width`: Width of the bars
- `alpha`: Transparency of the bars

##### add_boxplot

```python
add_boxplot(alpha: float = 0.4, outlier_alpha: float = 0.5)
```

Creates a box plot.

##### add_violin

```python
add_violin(alpha: float = 0.4, draw_quantiles: list = [0.25, 0.5, 0.75])
```

Creates a violin plot with optional quantile lines.

##### add_density

```python
add_density(alpha: float = 0.4)
```

Creates a density plot.

##### add_step

```python
add_step(direction: str = "hv")
```

Creates a step plot.

- `direction`: Direction of steps ("hv" horizontal then vertical, "vh" vertical then horizontal)

##### add_dotplot

```python
add_dotplot(binwidth: float = None, stackdir: str = "up", binaxis: str = "x")
```

Creates a dot plot with stacking.

- `binwidth`: Width of the bins (optional)
- `stackdir`: Direction of stacking ("up", "down", "center")
- `binaxis`: Axis to bin along ("x" or "y")

#### Statistical Plots

##### add_mean_bar

```python
add_mean_bar(alpha: float = 0.4, width: float = 0.7)
```

Adds bars showing mean values.

##### add_sem_errorbar

```python
add_sem_errorbar(width: float = 0.2)
```

Adds error bars showing standard error of the mean.

##### add_sd_errorbar

```python
add_sd_errorbar(width: float = 0.2)
```

Adds error bars showing standard deviation.

##### add_ci_errorbar

```python
add_ci_errorbar(width: float = 0.2, ci: float = 0.95)
```

Adds error bars showing confidence interval.

##### add_errorbar

```python
add_errorbar(ymin: str, ymax: str, width: float = 0.2)
```

Adds error bars using explicit min/max values.

- `ymin`: Column name for lower bound
- `ymax`: Column name for upper bound
- `width`: Width of the error bars

##### add_test_pvalue

```python
add_test_pvalue(test: str = 't', paired: bool = False, ref_group: Optional[str] = None)
```

Adds statistical test p-values.

- `test`: Type of test ('t', 'wilcox', 'anova', 'kruskal')
- `paired`: Whether to perform paired tests
- `ref_group`: Reference group for pairwise comparisons

##### add_correlation_text

```python
add_correlation_text(method: str = 'pearson', format: str = '.3f')
```

Adds correlation coefficient text.

##### add_smooth

```python
add_smooth(method: str = "lm", se: bool = True, alpha: float = 0.2)
```

Adds a smoothed conditional mean with confidence interval.

- `method`: Smoothing method ("lm" for linear model, "loess" for local regression)
- `se`: Whether to display confidence interval
- `alpha`: Transparency of the confidence interval

##### add_regression_line

```python
add_regression_line(ci: bool = True, alpha: float = 0.2)
```

Adds a regression line with optional confidence interval.

##### add_quantiles

```python
add_quantiles(quantiles: list = [0.25, 0.5, 0.75], alpha: float = 0.5, color: str = "red")
```

Adds horizontal lines at specified quantiles.

#### Distribution Plots

##### add_density_2d

```python
add_density_2d(alpha: float = 0.7)
```

Adds 2D density estimation contours.

##### add_density_2d_filled

```python
add_density_2d_filled(alpha: float = 0.7)
```

Adds filled 2D density contours.

##### add_hex

```python
add_hex(bins: int = 20)
```

Adds a hexagonal binning plot.

##### add_rug

```python
add_rug(sides: str = "b", alpha: float = 0.5, length: float = 0.03)
```

Adds a marginal rug plot.

- `sides`: Which sides to draw the rug ("t" top, "b" bottom, "l" left, "r" right)
- `length`: Length of the rug lines as proportion of plot size

##### add_count

```python
add_count(stat: str = "count", position: str = "stack")
```

Adds a count/frequency plot.

- `stat`: Statistic to use ("count" or "proportion")
- `position`: Position adjustment ("stack", "dodge", "fill")

#### Data Point Visualizations

##### add_data_points_beeswarm

```python
add_data_points_beeswarm(size: float = 3, alpha: float = 0.5)
```

Adds points in beeswarm arrangement.

##### add_data_points_jitter

```python
add_data_points_jitter(width: float = 0.2, size: float = 3, alpha: float = 0.5)
```

Adds jittered points.

#### Reference Lines

##### add_hline

```python
add_hline(yintercept: float, linetype: str = "dashed", color: str = "black", alpha: float = 1.0)
```

Adds a horizontal reference line.

##### add_vline

```python
add_vline(xintercept: float, linetype: str = "dashed", color: str = "black", alpha: float = 1.0)
```

Adds a vertical reference line.

#### Annotations

##### add_text

```python
add_text(label: str, x: float = None, y: float = None, ha: str = "center", va: str = "center", size: float = 11)
```

Adds text annotation at specific coordinates.

- `ha`: Horizontal alignment ("left", "center", "right")
- `va`: Vertical alignment ("top", "center", "bottom")

##### add_ribbon

```python
add_ribbon(ymin: str, ymax: str, alpha: float = 0.3)
```

Adds a filled area between two lines.

- `ymin`: Column name for lower bound
- `ymax`: Column name for upper bound

#### Customization Methods

##### adjust_labels

```python
adjust_labels(title: str = None, x: str = None, y: str = None)
```

Modifies plot labels.

##### adjust_colors

```python
adjust_colors(palette: str)
```

Changes color scheme.

##### adjust_legend_position

```python
adjust_legend_position(position: str)
```

Modifies legend position ("right", "left", "top", "bottom", "none").

##### remove_legend

```python
remove_legend()
```

Removes the legend.

##### show

```python
show()
```

Displays the plot.

### Additional Functions

#### Data Points & Amounts
- `add_data_points()`
- `add_count_bar()`
- `add_count_dash()`
- `add_count_dot()`
- `add_count_value()`
- `add_count_line()`
- `add_count_area()`
- `add_sum_bar()`
- `add_sum_dash()`
- `add_sum_dot()`
- `add_sum_value()`
- `add_sum_line()`
- `add_sum_area()`
- `add_heatmap()`
- `add_area()`

#### Central Tendency
- `add_mean_dash()`
- `add_mean_dot()`
- `add_mean_value()`
- `add_mean_line()`
- `add_mean_area()`
- `add_median_bar()`
- `add_median_dash()`
- `add_median_dot()`
- `add_median_value()`
- `add_median_line()`
- `add_median_area()`
- `add_curve_fit()`

#### Distribution & Uncertainty
- `add_histogram()`
- `add_range_errorbar()`
- `add_ci95_errorbar()`
- `add_sem_ribbon()`
- `add_range_ribbon()`
- `add_sd_ribbon()`
- `add_ci95_ribbon()`

#### Proportion
- `add_barstack_absolute()`
- `add_barstack_relative()`
- `add_areastack_absolute()`
- `add_areastack_relative()`
- `add_pie()`
- `add_donut()`

#### Statistical Testing
- `add_test_asterisks()`

#### Annotation
- `add_title()`
- `add_caption()`
- `add_data_labels()`
- `add_data_labels_repel()`
- `add_reference_lines()`

#### Remove
- `remove_legend_title()`
- `remove_padding()`
- `remove_title()`
- `remove_caption()`
- `remove_x_axis()`
- `remove_x_axis_line()`
- `remove_x_axis_ticks()`
- `remove_x_axis_labels()`
- `remove_x_axis_title()`
- `remove_y_axis()`
- `remove_y_axis_line()`
- `remove_y_axis_ticks()`
- `remove_y_axis_labels()`
- `remove_y_axis_title()`

#### Adjust Components & Properties
- `adjust_font()`
- `adjust_legend_title()`
- `adjust_title()`
- `adjust_x_axis_title()`
- `adjust_y_axis_title()`
- `adjust_caption()`
- `adjust_size()`
- `adjust_padding()`
- `adjust_x_axis()`
- `adjust_y_axis()`

#### Axis and Color Labels
- `rename_x_axis_labels()`
- `rename_y_axis_labels()`
- `rename_color_labels()`
- `reorder_x_axis_labels()`
- `reorder_y_axis_labels()`
- `reorder_color_labels()`
- `sort_x_axis_labels()`
- `sort_y_axis_labels()`
- `sort_color_labels()`
- `reverse_x_axis_labels()`
- `reverse_y_axis_labels()`
- `reverse_color_labels()`

#### Themes
- `theme_tidyplot()`
- `theme_ggplot2()`
- `theme_minimal_xy()`
- `theme_minimal_x()`
- `theme_minimal_y()`

#### Color Schemes
- `colors_discrete_friendly`
- `colors_discrete_seaside`
- `colors_discrete_apple`
- `colors_discrete_friendly_long`
- `colors_discrete_okabeito`
- `colors_discrete_ibm`
- `colors_discrete_metro`
- `colors_discrete_candy`
- `colors_continuous_viridis`
- `colors_continuous_magma`
- `colors_continuous_inferno`
- `colors_continuous_plasma`
- `colors_continuous_cividis`
- `colors_continuous_rocket`
- `colors_continuous_mako`
- `colors_continuous_turbo`
- `colors_continuous_bluepinkyellow`
- `colors_diverging_blue2red`
- `colors_diverging_blue2brown`
- `colors_diverging_BuRd`
- `colors_diverging_BuYlRd`
- `colors_diverging_spectral`
- `colors_diverging_icefire`
- `new_color_scheme()`

#### Split
- `split_plot()`

#### Output
- `view_plot()`
- `save_plot()`

#### Helpers
- `all_rows()`
- `filter_rows()`
- `max_rows()`
- `min_rows()`
- `first_rows()`
- `last_rows()`
- `sample_rows()`
- `add()`
- `as_tidyplot()`
- `flip_plot()`
- `format_number()`
- `format_p_value()`

## Examples

Here are some common plotting scenarios:

### Time Series Plot

```python
(df.tidyplot(x='time', y='value')
   .add_line()
   .add_scatter()
   .adjust_labels(title='Time Series Plot', x='Date', y='Value'))
```

### Grouped Scatter Plot

```python
(df.tidyplot(x='x', y='y', color='group')
   .add_scatter()
   .adjust_labels(title='Grouped Scatter Plot', x='X', y='Y'))
```

### Statistical Plot with Error Bars

```python
(df.tidyplot(x='group', y='value')
   .add_mean_bar()
   .add_ci_errorbar()
   .adjust_labels(title='Mean Values with 95% CI', x='Group', y='Value'))
```

### Distribution Plot

```python
(df.tidyplot(x='value', color='group')
   .add_density(alpha=0.5)
   .adjust_labels(title='Distribution by Group', x='Value', y='Density'))
```

For more examples, check out the examples directory in the repository.

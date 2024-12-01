# Tidyplots for Python

<div align="center">
<table>
<tr>
<td><img src="figures/1_scatter.png" width="150"/></td>
<td><img src="figures/1.4_box.png" width="150"/></td>
<td><img src="figures/1.5_violin.png" width="150"/></td>
<td><img src="figures/1.6_density.png" width="150"/></td>
<td><img src="figures/1_line.png" width="150"/></td>
<td><img src="figures/1.3_bar.png" width="150"/></td>
</tr>
<tr>
<td><img src="figures/1.8_dot.png" width="150"/></td>
<td><img src="figures/2.1_mean_bar.png" width="150"/></td>
<td><img src="figures/7.5_curve_fit.png" width="150"/></td>
<td><img src="figures/7.6.1_sem_ribbon.png" width="150"/></td>
<td><img src="figures/7.1_hexbin.png" width="150"/></td>
<td><img src="figures/3.5_count.png" width="150"/></td>
</tr>
<tr>
<td><img src="figures/5.4.2_scatter.png" width="150"/></td>
<td><img src="figures/7.2_density_2d_filled.png" width="150"/></td>
<td><img src="figures/4.1_plot.png" width="150"/></td>
<td><img src="figures/5.4_bar.png" width="150"/></td>
<td><img src="figures/2.7_scatter.png" width="150"/></td>
<td><img src="figures/2.8_scatter.png" width="150"/></td>
</tr>
<tr>
<td><img src="figures/3.1_scatter.png" width="150"/></td>
<td><img src="figures/3.4_scatter.png" width="150"/></td>
<td><img src="figures/4.2_plot.png" width="150"/></td>
<td><img src="figures/4_scatter.png" width="150"/></td>
<td><img src="figures/5.1_scatter.png" width="150"/></td>
<td><img src="figures/5.2_scatter.png" width="150"/></td>
</tr>
<tr>
<td><img src="figures/5.3_scatter.png" width="150"/></td>
<td><img src="figures/5.4.1_line.png" width="150"/></td>
<td><img src="figures/5.4.3_scatter.png" width="150"/></td>
<td><img src="figures/6.1_bar.png" width="150"/></td>
<td><img src="figures/6.2_bar.png" width="150"/></td>
<td><img src="figures/7.2_plot.png" width="150"/></td>
</tr>
<tr>
<td><img src="figures/7.3.1_sum_bar_value.png" width="150"/></td>
<td><img src="figures/7.3.2_sum_line_dot.png" width="150"/></td>
<td><img src="figures/7.3.3_sum_area.png" width="150"/></td>
<td><img src="figures/7.4.1_median_bar_value.png" width="150"/></td>
<td><img src="figures/7.4.2_median_line_dot.png" width="150"/></td>
<td><img src="figures/7.4.3_median_area.png" width="150"/></td>
</tr>
</table>
</div>

A Python library for creating publication-ready plots with a fluent, chainable interface, inspired by [tidyplots R version](https://github.com/jbengler/tidyplots).

Built on top of plotnine, it provides a pandas DataFrame extension method for easy and intuitive plot creation.

todo list

* [X] complete the whole set of plotting that maps to R version
* [ ] more themes, such as ggprism
* [ ] more palettes, including palettes from famous journals, for instance, ggsci
* [ ] more plotting variations from ggpubr

## Features

- Fluent, chainable interface using pandas DataFrame extension
- Publication-ready plots with Nature Publishing Group (NPG) color palette by default
- Comprehensive set of plot types and statistical visualizations
- Flexible faceting with `split_by` parameter for both single and multi-variable splits
- Statistical annotations (p-values, correlations, etc.)
- Multiple scientific journal color palettes (NPG, AAAS, NEJM, etc.)
- Easy customization of colors, labels, and themes
- Prism-style publication themes

## Installation

```bash
pip install tidyplots-python
```

for development version:

```
pip install git+https://github.com/JNU-Tangyin/tidyplots-python.git
```

## Quick Start

```python
import pandas as pd
import numpy as np
import seaborn as sns
from tidyplots import TidyPlot

# Create sample data
iris = sns.load_dataset("iris")

# Create a scatter plot with groups
(iris.tidyplot(x='sepal_length', y='sepal_width', fill='species')
 .add_scatter(size=5, alpha=0.5)
 .add_density_2d(alpha=0.1)
 .adjust_labels(title='Customization Test',
               x='Sepal Length', y='Sepal Width')
 .adjust_colors(['#1f77b4', '#ff7f0e', '#2ca02c'])
 .adjust_legend_position('right')
 .show())
```

<img src="figures/5.4.2_scatter.png" width="500"/>

## API Reference

### Core Plot Creation

- `df.tidyplot(x, y=None, color=None)`: Initialize a plot with aesthetics

  ```python
  df.tidyplot(x='column1', y='column2', color='group')
  ```

### Plot Types

- `.add_scatter(alpha=0.6, size=3)`: Add scatter points
- `.add_line(alpha=0.8)`: Add line plot
- `.add_boxplot(alpha=0.3)`: Add box plot
- `.add_violin(draw_quantiles=[0.25, 0.5, 0.75])`: Add violin plot
- `.add_density(alpha=0.5)`: Add density plot
- `.add_density_2d()`: Add 2D density contour plot
- `.add_bar()`: Add bar plot
- `.add_errorbar(ymin, ymax)`: Add error bars
- `.add_hex(bins=20)`: Add hexbin plot
- `.add_data_points(alpha=0.3)`: Add jittered data points

### Statistical Features

- `.add_smooth(method='lm')`: Add smoothing line
- `.add_correlation_text()`: Add correlation coefficient
- `.add_pvalue(p_value, x1, x2, y)`: Add p-value annotation

### Customization

- `.adjust_labels(title=None, x=None, y=None)`: Set plot labels
- `.adjust_colors(palette)`: Change color palette
  - Available palettes: 'npg' (default), 'aaas', 'nejm', 'lancet', 'jama', 'd3', 'material', 'igv'
- `.scale_color_gradient(low, high)`: Set color gradient
- `.adjust_axis_text_angle(angle)`: Rotate axis text

### Themes

- Default theme: Prism-style with NPG colors
- Customizable base theme:

  ```python
  .adjust_theme(base_size=11, base_family="Arial")
  ```

## Examples

### Basic Plots

```python
import pandas as pd
import seaborn as sns
from tidyplots import TidyPlot

# Load sample data
iris = sns.load_dataset("iris")

# Simple scatter plot with groups
(iris.tidyplot(x='sepal_length', y='sepal_width', fill='species')
    .add_scatter()
    .show())

# Faceted plot using single variable
(iris.tidyplot(x='sepal_length', y='sepal_width', fill='species', split_by='species')
    .add_scatter()
    .show())

# Grid faceted plot using two variables
(iris.tidyplot(x='sepal_length', y='sepal_width', fill='species', 
              split_by=['species', 'petal_size_category'])  # petal_size_category is an example
    .add_scatter()
    .show())
```

### Scatter Plot

```python
import seaborn as sns
from tidyplots import TidyPlot

# Load iris dataset
iris = sns.load_dataset('iris')

# Create a scatter plot
(iris.tidyplot(x='sepal_length', y='sepal_width', fill='species')
     .add_scatter(size=5, alpha=0.7)
     .adjust_labels(title='Iris Sepal Dimensions', 
                    x='Sepal Length', y='Sepal Width'))
```

![Scatter Plot](figures/1_scatter.png)

### Box Plot

```python
# Create a box plot
(iris.tidyplot(x='species', y='sepal_length', fill='species')
     .add_boxplot(alpha=0.5)
     .add_jitter(width=0.2, size=3, alpha=0.7)
     .adjust_labels(title='Sepal Length by Species', 
                    x='Species', y='Sepal Length'))
```

![Box Plot](figures/1.4_box.png)

### Violin Plot

```python
# Create a violin plot
(iris.tidyplot(x='species', y='petal_length', fill='species')
     .add_violin(draw_quantiles=[0.25, 0.5, 0.75], alpha=0.6)
     .adjust_labels(title='Petal Length Distribution', 
                    x='Species', y='Petal Length'))
```

![Violin Plot](figures/1.5_violin.png)

### Density Plot

```python
# Create a density plot
(iris.tidyplot(x='sepal_width', fill='species')
     .add_density(alpha=0.3)
     .adjust_labels(title='Sepal Width Density', 
                    x='Sepal Width', y='Density'))
```

![Density Plot](figures/1.6_density.png)

### Line Plot

```python
# Load flights dataset
flights = sns.load_dataset('flights')

# Create a line plot
(flights.tidyplot(x='year', y='passengers', fill='month')
        .add_line(size=2)
        .adjust_labels(title='Passenger Trends', 
                       x='Year', y='Number of Passengers'))
```

![Line Plot](figures/1_line.png)

### Bar Plot

```python
# Create a bar plot
tips = sns.load_dataset('tips')

# Average tip by day
(tips.tidyplot(x='day', y='tip', fill='sex')
     .add_bar(stat='mean')
     .adjust_labels(title='Average Tip by Day', 
                    x='Day', y='Average Tip'))
```

![Bar Plot](figures/1.3_bar.png)

### Dot Plot

```python
# Create a dot plot
(iris.tidyplot(x='species', y='sepal_length', fill='species')
     .add_dotplot()
     .adjust_labels(title='Sepal Length Dot Plot', 
                    x='Species', y='Sepal Length'))
```

![Dot Plot](figures/1.8_dot.png)

### Mean Bar Plot

```python
# Mean bar plot with error bars
(tips.tidyplot(x='day', y='total_bill', fill='sex')
     .add_mean_bar(alpha=0.5)
     .add_sem_errorbar()
     .adjust_labels(title='Mean Total Bill by Day', 
                    x='Day', y='Total Bill'))
```

![Mean Bar Plot](figures/2.1_mean_bar.png)

### Curve Fitting

```python
# Scatter plot with curve fitting
(tips.tidyplot(x='total_bill', y='tip', fill='sex')
     .add_scatter()
     .add_smooth(method='lm')
     .adjust_labels(title='Tip vs Total Bill', 
                    x='Total Bill', y='Tip'))
```

![Curve Fitting](figures/7.5_curve_fit.png)

### Ribbon Plot (SEM)

```python
# Ribbon plot showing standard error
(tips.groupby('day')['total_bill']
     .apply(lambda x: pd.DataFrame({
         'mean': x.mean(),
         'sem': x.sem()
     }))
     .reset_index()
     .tidyplot(x='day', y='mean', fill='sex')
     .add_line(color='cyan')
     .add_ribbon(ymin='mean - sem', ymax='mean + sem', alpha=0.3)
     .adjust_labels(title='Total Bill with SEM', 
                    x='Day', y='Total Bill'))
```

![Ribbon Plot](figures/7.6.1_sem_ribbon.png)

### Hexbin Plot

```python
# Hexbin plot for density visualization
(tips.tidyplot(x='total_bill', y='tip', fill='sex')
     .add_hex(bins=20)
     .adjust_labels(title='Total Bill vs Tip Density', 
                    x='Total Bill', y='Tip'))
```

![Hexbin Plot](figures/7.1_hexbin.png)

### Count Plot

```python
# Count plot
titanic = sns.load_dataset('titanic')
(titanic.tidyplot(x='class', fill='survived')
        .add_bar(stat='count')
        .adjust_labels(title='Passenger Count by Class and Survival', 
                       x='Class', y='Count'))
```

![Count Plot](figures/3.5_count.png)

## Faceting

The `split_by` parameter allows you to create faceted plots in two ways:
1. Single variable faceting using `facet_wrap`
2. Two-variable faceting using `facet_grid`

### Single Variable Faceting (facet_wrap)

```python
# Create faceted scatter plot by species
(iris.tidyplot(x='sepal_length', y='sepal_width', split_by='species', fill='species')
 .add_scatter(alpha=0.6)
 .adjust_labels(title='Iris Measurements by Species',
               x='Sepal Length', y='Sepal Width')
 .show())

# Create faceted violin plot by island
penguins = sns.load_dataset("penguins")
(penguins.tidyplot(x='species', y='body_mass_g', split_by='island', fill='species')
 .add_violin(alpha=0.7)
 .adjust_labels(title='Penguin Body Mass by Island',
               x='Species', y='Body Mass (g)')
 .show())
```

<div align="center">
<table>
<tr>
<td><img src="figures/13.1_iris_facet_wrap.png" width="400"/></td>
<td><img src="figures/13.3_penguins_facet_wrap.png" width="400"/></td>
</tr>
</table>
</div>

### Two-Variable Faceting (facet_grid)

```python
# Create faceted scatter plot by day and time
tips = sns.load_dataset("tips")
(tips.tidyplot(x='total_bill', y='tip', split_by=['day', 'time'], fill='smoker')
 .add_scatter(alpha=0.6)
 .adjust_labels(title='Tips by Day and Time',
               x='Total Bill', y='Tip')
 .show())

# Create faceted boxplot by color and clarity
diamonds = sns.load_dataset("diamonds")
diamonds_subset = diamonds.sample(n=1000, random_state=42)
(diamonds_subset.tidyplot(x='cut', y='price', split_by=['color', 'clarity'], fill='color')
 .add_boxplot(alpha=0.7)
 .adjust_labels(title='Diamond Prices by Cut, Color, and Clarity',
               x='Cut', y='Price')
 .show())
```

<div align="center">
<table>
<tr>
<td><img src="figures/13.2_tips_facet_grid.png" width="400"/></td>
<td><img src="figures/13.4_diamonds_facet_grid.png" width="400"/></td>
</tr>
</table>
</div>

### Bar Plot with Faceting

```python
# Create faceted bar plot showing survival counts
titanic = sns.load_dataset("titanic")
titanic['survived'] = titanic['survived'].map({0: 'No', 1: 'Yes'})
survival_data = titanic.groupby(['class', 'sex', 'survived']).size().reset_index(name='count')
(survival_data.tidyplot(x='class', y='count', fill='survived', split_by='sex')
 .add_bar(position='dodge', alpha=0.7)
 .adjust_labels(title='Titanic Survival by Class and Sex',
               x='Class', y='Count')
 .show())
```

<div align="center">
<img src="figures/13.5_titanic_facet_wrap.png" width="400"/>
</div>

## Color Palettes

Default color palettes from scientific journals:

```python
# Change color palette to Nature Publishing Group (default)
df.tidyplot(...).adjust_colors('npg')  # 
```

Available palettes (thanks to ggsci):

- 'npg': Nature Publishing Group colors (default)
- 'aaas': Science/AAAS colors
- 'nejm': New England Journal of Medicine colors
- 'lancet': The Lancet colors
- 'jama': Journal of American Medical Association colors
- 'd3': D3.js colors
- 'material': Material Design colors
- 'igv': Integrative Genomics Viewer colors

and it supports the all color schemes in matplotlib by name:

```python
cmaps = [
('Perceptually Uniform Sequential', ['viridis', 'plasma', 'inferno', 'magma']),
('Sequential', [ 'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']),
('Sequential (2)', ['binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink', 'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia','hot', 'afmhot', 'gist_heat', 'copper']),
 ('Diverging', ['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']), ('Qualitative', [ 'Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c']),
('Miscellaneous', [ 'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'hsv', 'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar'])
]
# Change color palette using Matplotlib colormaps
df.tidyplot(...).adjust_colors('Set1')
```

more to come ...

## Dependencies

- pandas >= 1.0.0
- numpy >= 1.18.0
- plotnine >= 0.8.0

## Notices

This project is a Python transplant from [tidyplots R version](https://github.com/jbengler/tidyplots), and it is supported by [Windsurf](https://codeium.com/windsurf).

Althought I believe the philosophy we present in this work is convenient, pythonic, and easy to use, it is however rudimentary starting point, therefore it may contain bugs and missing features. Please forgive me if you find any.

And most importantly, contributions are more than welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Missing functions

Please note that not all the functions are available because of:

1. plotnine being a younger library with fewer contributors
2. Some R-specific features being harder to implement in Python
3. Different underlying graphics engines (R's grid vs Python's matplotlib)

The list is provided as below:

1. **Removed Functions** :

* `geom_hex()` - Hexagonal binning not available in plotnine
* `geom_text_repel()` - Text repulsion for avoiding overlaps not available
* `coord_polar()` - Polar coordinate system not fully supported
* `stat_density_2d_filled()` - Filled 2D density plots not available
* `geom_raster()` - High-performance raster rendering not available
* `geom_sf()` - Simple features (geographic data) not supported
* `geom_spoke()` - Spoke plots not available
* `stat_ellipse()` - Statistical ellipses not supported
* `geom_label()` - Labels with backgrounds not available
* `geom_curve()` - Curved line segments not available

2. **Modified Functions** :

* `add_data_labels_repel()` - Modified to use regular `geom_text()` instead of `geom_text_repel()`
* `add_pie_chart()` - Implemented using bar plots and coordinate transformations since native pie charts aren't supported
* `add_donut_chart()` - Similar to pie charts, implemented through workarounds
* `add_density_2d_filled()` - Had to use regular density_2d with modified aesthetics

3. **Limited Functionality** :

* `facet_grid()` - More limited options compared to ggplot2
* `scale_*_gradient2()` - Diverging color scales have limited options
* `theme()` - Some theme elements and customizations not available
* `coord_fixed()` - Fixed coordinate ratio support is limited
* `position_dodge2()` - Advanced dodging features not available

4. **Performance Differences** :

* Large dataset handling is generally slower in plotnine
* Some smoothing methods in `stat_smooth()` have fewer options
* Rendering of complex plots with many layers is less optimized

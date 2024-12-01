# API Reference

## TidyPlot Class

### Core Methods

#### `__call__(x, y=None, color=None, fill=None, shape=None, size=None, linetype=None, split_by=None, **kwargs)`

Creates a new plot with the given aesthetics.

**Parameters:**

- `x` (str): Column name for x-axis
- `y` (str, optional): Column name for y-axis
- `color` (str, optional): Column name for color aesthetic
- `fill` (str, optional): Column name for fill aesthetic
- `shape` (str, optional): Column name for shape aesthetic
- `size` (str, optional): Column name for size aesthetic
- `linetype` (str, optional): Column name for linetype aesthetic
- `split_by` (str or List[str], optional): Column name(s) for faceting
  - If str: Single column name for facet_wrap
  - If List[str]: Two column names for facet_grid (row, col)

**Returns:**
- `self`: Returns the TidyPlot object for method chaining

**Examples:**

```python
# Single column faceting
df.tidyplot(x='time', y='value', split_by='category')

# Two-column grid faceting
df.tidyplot(x='time', y='value', split_by=['treatment', 'group'])
```

### Geom Methods

#### `add_scatter(**kwargs)`
Add scatter points to the plot.

#### `add_line(**kwargs)`
Add line to the plot.

#### `add_smooth(**kwargs)`
Add smoothed conditional means.

#### `add_bar(stat='identity', **kwargs)`
Add bar plot.

#### `add_boxplot(**kwargs)`
Add boxplot to the plot.

#### `add_violin(draw_quantiles=[0.25, 0.5, 0.75], **kwargs)`
Add violin plot.

#### `add_density(alpha=0.3)`
Add density plot.

### Theme and Style Methods

#### `use_theme(theme_name)`
Change the plot theme.

#### `adjust_colors(palette)`
Change color palette. Available palettes:
- 'npg' (default)
- 'aaas'
- 'nejm'
- 'lancet'
- 'jama'
- 'd3'
- 'material'
- 'igv'

#### `scale_color_gradient(low, high)`
Set color gradient.

#### `adjust_axis_text_angle(angle)`
Rotate axis text.

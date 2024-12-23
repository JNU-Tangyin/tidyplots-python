# R tidyplots API Reference

## Core Functions

### Plot Creation
- `tidyplot()`: Create a new tidyplot from data
- `as_tidyplot()`: Convert a ggplot to tidyplot

### Data Points & Amounts
- `add_data_points()`: Add individual data points
- `add_data_points_jitter()`: Add jittered data points
- `add_data_points_beeswarm()`: Add data points in beeswarm arrangement
- `add_count_bar()`: Add bars showing counts
- `add_count_dash()`: Add dashes showing counts
- `add_count_dot()`: Add dots showing counts
- `add_count_value()`: Add text values showing counts
- `add_count_line()`: Add lines showing counts
- `add_count_area()`: Add areas showing counts
- `add_sum_bar()`: Add bars showing sums
- `add_sum_dash()`: Add dashes showing sums
- `add_sum_dot()`: Add dots showing sums
- `add_sum_value()`: Add text values showing sums
- `add_sum_line()`: Add lines showing sums
- `add_sum_area()`: Add areas showing sums
- `add_heatmap()`: Add heatmap visualization

### Central Tendency
- `add_mean_bar()`: Add bars showing means
- `add_mean_dash()`: Add dashes showing means
- `add_mean_dot()`: Add dots showing means
- `add_mean_value()`: Add text values showing means
- `add_mean_line()`: Add lines showing means
- `add_mean_area()`: Add areas showing means
- `add_median_bar()`: Add bars showing medians
- `add_median_dash()`: Add dashes showing medians
- `add_median_dot()`: Add dots showing medians
- `add_median_value()`: Add text values showing medians
- `add_median_line()`: Add lines showing medians
- `add_median_area()`: Add areas showing medians
- `add_curve_fit()`: Add fitted curve

### Distribution & Uncertainty
- `add_histogram()`: Add histogram
- `add_boxplot()`: Add box plot
- `add_violin()`: Add violin plot
- `add_sem_errorbar()`: Add error bars showing standard error of mean
- `add_range_errorbar()`: Add error bars showing range
- `add_sd_errorbar()`: Add error bars showing standard deviation
- `add_ci95_errorbar()`: Add error bars showing 95% confidence interval
- `add_sem_ribbon()`: Add ribbon showing standard error of mean
- `add_range_ribbon()`: Add ribbon showing range
- `add_sd_ribbon()`: Add ribbon showing standard deviation
- `add_ci95_ribbon()`: Add ribbon showing 95% confidence interval

### Proportion
- `add_barstack_absolute()`: Add stacked bars (absolute)
- `add_barstack_relative()`: Add stacked bars (relative)
- `add_areastack_absolute()`: Add stacked areas (absolute)
- `add_areastack_relative()`: Add stacked areas (relative)
- `add_pie()`: Add pie chart
- `add_donut()`: Add donut chart

### Statistical Testing
- `add_test_pvalue()`: Add p-value from statistical test
- `add_test_asterisks()`: Add significance asterisks

### Annotation
- `add_title()`: Add plot title
- `add_caption()`: Add plot caption
- `add_data_labels()`: Add data labels
- `add_data_labels_repel()`: Add data labels with repulsion
- `add_reference_lines()`: Add reference lines

### Remove Elements
- `remove_legend()`: Remove legend
- `remove_legend_title()`: Remove legend title
- `remove_padding()`: Remove plot padding
- `remove_title()`: Remove plot title
- `remove_caption()`: Remove plot caption
- `remove_x_axis()`: Remove x axis
- `remove_x_axis_line()`: Remove x axis line
- `remove_x_axis_ticks()`: Remove x axis ticks
- `remove_x_axis_labels()`: Remove x axis labels
- `remove_x_axis_title()`: Remove x axis title
- `remove_y_axis()`: Remove y axis
- `remove_y_axis_line()`: Remove y axis line
- `remove_y_axis_ticks()`: Remove y axis ticks
- `remove_y_axis_labels()`: Remove y axis labels
- `remove_y_axis_title()`: Remove y axis title

### Adjust Components
- `adjust_colors()`: Modify color scheme
- `adjust_font()`: Modify font properties
- `adjust_legend_title()`: Modify legend title
- `adjust_legend_position()`: Modify legend position
- `adjust_title()`: Modify plot title
- `adjust_x_axis_title()`: Modify x axis title
- `adjust_y_axis_title()`: Modify y axis title
- `adjust_caption()`: Modify plot caption
- `adjust_size()`: Modify plot size
- `adjust_padding()`: Modify plot padding
- `adjust_x_axis()`: Modify x axis properties
- `adjust_y_axis()`: Modify y axis properties

### Label Management
- `rename_x_axis_labels()`: Rename x axis labels
- `rename_y_axis_labels()`: Rename y axis labels
- `rename_color_labels()`: Rename color labels
- `reorder_x_axis_labels()`: Reorder x axis labels
- `reorder_y_axis_labels()`: Reorder y axis labels
- `reorder_color_labels()`: Reorder color labels
- `sort_x_axis_labels()`: Sort x axis labels
- `sort_y_axis_labels()`: Sort y axis labels
- `sort_color_labels()`: Sort color labels
- `reverse_x_axis_labels()`: Reverse x axis labels
- `reverse_y_axis_labels()`: Reverse y axis labels
- `reverse_color_labels()`: Reverse color labels

### Themes
- `theme_tidyplot()`: Apply tidyplot theme
- `theme_ggplot2()`: Apply ggplot2 theme
- `theme_minimal_xy()`: Apply minimal theme with both axes
- `theme_minimal_x()`: Apply minimal theme with x axis
- `theme_minimal_y()`: Apply minimal theme with y axis

### Color Schemes
#### Discrete Colors
- `colors_discrete_friendly`: Colorblind-friendly palette
- `colors_discrete_seaside`: Seaside-inspired palette
- `colors_discrete_apple`: Apple-inspired palette
- `colors_discrete_friendly_long`: Extended colorblind-friendly palette
- `colors_discrete_okabeito`: Okabe-Ito palette
- `colors_discrete_ibm`: IBM color palette
- `colors_discrete_metro`: Metro-inspired palette
- `colors_discrete_candy`: Candy-inspired palette

#### Continuous Colors
- `colors_continuous_viridis`: Viridis palette
- `colors_continuous_magma`: Magma palette
- `colors_continuous_inferno`: Inferno palette
- `colors_continuous_plasma`: Plasma palette
- `colors_continuous_cividis`: Cividis palette
- `colors_continuous_rocket`: Rocket palette
- `colors_continuous_mako`: Mako palette
- `colors_continuous_turbo`: Turbo palette
- `colors_continuous_bluepinkyellow`: Blue-Pink-Yellow palette

#### Diverging Colors
- `colors_diverging_blue2red`: Blue to Red
- `colors_diverging_blue2brown`: Blue to Brown
- `colors_diverging_BuRd`: Blue-Red
- `colors_diverging_BuYlRd`: Blue-Yellow-Red
- `colors_diverging_spectral`: Spectral
- `colors_diverging_icefire`: Ice-Fire

### Output
- `view_plot()`: Display plot
- `save_plot()`: Save plot to file

### Helper Functions
- `all_rows()`: Select all rows
- `filter_rows()`: Filter rows
- `max_rows()`: Select rows with maximum values
- `min_rows()`: Select rows with minimum values
- `first_rows()`: Select first rows
- `last_rows()`: Select last rows
- `sample_rows()`: Select random rows
- `format_number()`: Format numbers
- `format_p_value()`: Format p-values

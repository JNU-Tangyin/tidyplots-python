"""A Python library for creating publication-ready plots with a fluent, chainable interface."""

import pandas as pd
import numpy as np
from plotnine import (
    # Core components
    ggplot, aes, labs, annotate,
    # Geometries
    geom_point, geom_line, geom_bar, geom_boxplot, geom_violin, 
    geom_density, geom_step, geom_dotplot, geom_text, geom_jitter,
    geom_histogram, geom_col, geom_area, geom_tile, geom_rect, geom_segment,
    geom_smooth,
    geom_errorbar,
    # Statistics
    stat_summary, stat_density_2d,
)
from plotnine import (
    # Positions
    position_jitterdodge, position_stack, position_fill, position_dodge, position_jitter,
    # Coordinates and scales
    scale_x_continuous, scale_y_continuous, scale_x_discrete,
    scale_color_manual, scale_fill_manual, scale_fill_gradientn,
    # Themes and elements
    theme, theme_minimal, element_text, element_blank, element_line, element_rect,
    # Facets
    facet_wrap, facet_grid,
    # Guides
    guides, guide_legend, after_stat
)
from plotnine.layer import Layers, layer
from plotnine.positions.position import position
from plotnine.themes.theme import theme
from plotnine.themes.elements import element_blank
from plotnine.coords import coord_flip
from typing import Optional, List, Union, Dict, Any
from . import palettes
from . import themes
import scipy.stats as stats
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import matplotlib.path as mpath
from .plotnine import geom_pie, geom_rose

@pd.api.extensions.register_dataframe_accessor("tidyplot")
class TidyPlotAccessor:
    """Accessor for creating TidyPlots from pandas DataFrames."""
    
    def __init__(self, pandas_obj):
        """Initialize the accessor with a pandas DataFrame."""
        self._obj = pandas_obj
        
    def __call__(self, x=None, y=None, fill=None, color=None, size=None, alpha=None, split_by=None):
        """Create a TidyPlot from the DataFrame with aesthetic mappings."""
        return TidyPlot(self._obj, x=x, y=y, fill=fill, color=color, size=size, alpha=alpha, split_by=split_by)

class TidyPlot:
    """A fluent interface for creating publication-ready plots."""
    
    def __init__(self, data, x=None, y=None, fill=None, color=None, size=None, alpha=None, split_by=None):
        """Initialize TidyPlot with data and aesthetic mappings."""
        self._obj = data
        self._x = x
        self._y = y
        self._fill = fill
        self._color = color
        self._size = size
        self._alpha = alpha
        self._split_by = split_by
        self._colors = None
        self.fig = None
        self.ax = None
        self.prism = themes.TidyPrism()
        self._default_theme = self.prism.theme_prism()  # 设置默认主题为 theme_prism
        self._default_palette = 'npg'  # 设置默认调色板为 npg
        
        # Initialize the plot with basic aesthetics
        mapping_dict = {}
        if x is not None:
            mapping_dict['x'] = x
        if y is not None:
            mapping_dict['y'] = y
        if fill is not None:
            mapping_dict['fill'] = fill
        if color is not None:
            mapping_dict['color'] = color
        if size is not None:
            mapping_dict['size'] = size
        if alpha is not None:
            mapping_dict['alpha'] = alpha
            
        self.plot = (ggplot(self._obj, aes(**mapping_dict)) +
                    self._default_theme)  # Use default theme
        
        # Apply default color palette
        colors = palettes.get_palette(self._default_palette)
        if 'fill' in mapping_dict:
            self.plot = self.plot + scale_fill_manual(values=colors)
        if 'color' in mapping_dict:
            self.plot = self.plot + scale_color_manual(values=colors)
        
    def __call__(self, x: str, y: str = None, 
                color: Optional[str] = None, 
                fill: Optional[str] = None,
                shape: Optional[str] = None,
                size: Optional[str] = None,
                linetype: Optional[str] = None,
                split_by: Optional[Union[str, List[str]]] = None,
                **kwargs):
        """Create a new plot with the given aesthetics.
        
        Args:
            x: Column name for x-axis
            y: Column name for y-axis
            color: Column name for color aesthetic
            fill: Column name for fill aesthetic
            shape: Column name for shape aesthetic
            size: Column name for size aesthetic
            linetype: Column name for linetype aesthetic
            split_by: Column name(s) for faceting. Can be either:
                     - str: Single column name for facet_wrap
                     - List[str]: Two column names for facet_grid (row, col)
        """
        
        # 构建映射字典，排除self和非映射参数
        mapping_dict = {key: value for key, value in locals().items() 
                       if key not in ['self', 'kwargs'] and value is not None}
        
        # Remove split_by from mapping as it's not an aesthetic
        if 'split_by' in mapping_dict:
            del mapping_dict['split_by']

        self.plot = (ggplot(self._obj, aes(**mapping_dict)) +
                    self._default_theme)  # Use default theme
        
        # Apply default color palette
        colors = palettes.get_palette(self._default_palette)
        if 'y' not in mapping_dict:
            self.plot = self.plot + scale_fill_manual(values=colors)
        else:
            if color is not None:
                self.plot = self.plot + scale_color_manual(values=colors)
        
        # Handle split_by parameter
        if split_by is not None:
            if isinstance(split_by, str):
                # Single variable uses facet_wrap
                self.plot = self.plot + facet_wrap(f"~{split_by}")
            elif isinstance(split_by, (list, tuple)) and len(split_by) == 2:
                # Two variables use facet_grid
                self.plot = self.plot + facet_grid(f"{split_by[0]}~{split_by[1]}")
            else:
                raise ValueError("split_by must be either a string or a list/tuple of two strings")
                
        return self
    
    def add_scatter(self,**kwargs): 
        """Add scatter points to the plot."""
        self.plot = self.plot + geom_point(**kwargs)
        return self
    
    def add_line(self,**kwargs): 
        """Add line to the plot."""
        self.plot = self.plot + geom_line(**kwargs) 
        return self
    
    def add_smooth(self,**kwargs): 
        """Add smoothed conditional means."""
        self.plot = self.plot + geom_smooth(**kwargs)
        return self
    
    def add_bar(self,stat:str ='identity', **kwargs): 
        """Add bar plot."""
        self.plot = self.plot + geom_bar(stat=stat, **kwargs)
        return self
    
    def add_boxplot(self,**kwargs): 
        """Add boxplot to the plot."""
        self.plot = self.plot + geom_boxplot(**kwargs)
        return self
    
    def add_violin(self, draw_quantiles: List[float] = [0.25, 0.5, 0.75], **kwargs):
        """Add violin plot."""
        self.plot = self.plot + geom_violin(draw_quantiles=draw_quantiles, **kwargs)
        return self
    
    def add_density(self, alpha: float = 0.3):
        """Add density plot."""
        self.plot = self.plot + geom_density(alpha=alpha)
        return self
    
    def add_hex(self, bins: int = 20):
        """Add hexagonal binning."""
        self.plot = self.plot + geom_hex(bins=bins)
        return self
    
    def add_errorbar(self, ymin: str, ymax: str, alpha: float = 0.8, width: float = 0.2):
        """Add error bars with explicit min/max values."""
        self.plot = self.plot + geom_errorbar(
            aes(ymin=ymin, ymax=ymax), 
            alpha=alpha, 
            width=width
        )
        return self
        
    def add_data_points_jitter(self, **kwargs): 
        """Add jittered points to the plot."""
        self.plot = self.plot + geom_jitter(**kwargs)
        return self

    def add_mean_bar(self, alpha: float = 0.4, width: float = 0.7):
        """Add bars showing mean values."""
        self.plot = self.plot + stat_summary(fun_y=np.mean, geom='bar', alpha=alpha, width=width)
        return self

    def add_sem_errorbar(self, width: float = 0.2):
        """Add error bars showing standard error of the mean."""
        self.plot = self.plot + stat_summary(fun_data='mean_se', geom='errorbar', width=width)
        return self

    def add_sd_errorbar(self, width: float = 0.2):
        """Add error bars showing standard deviation."""
        def sd_fun(x):
            return pd.DataFrame({
                'y': [np.mean(x)],
                'ymin': [np.mean(x) - np.std(x)],
                'ymax': [np.mean(x) + np.std(x)]
            })
        self.plot = self.plot + stat_summary(fun_data=sd_fun, geom='errorbar', width=width)
        return self

    def add_ci_errorbar(self, width: float = 0.2, ci: float = 0.95):
        """Add error bars showing confidence interval."""
        def ci_fun(x):
            mean = np.mean(x)
            sem = np.std(x, ddof=1) / np.sqrt(len(x))
            ci_factor = stats.t.ppf((1 + ci) / 2, len(x) - 1)
            ci_width = ci_factor * sem
            return pd.DataFrame({
                'y': [mean],
                'ymin': [mean - ci_width],
                'ymax': [mean + ci_width]
            })
        self.plot = self.plot + stat_summary(fun_data=ci_fun, geom='errorbar', width=width)
        return self

    def add_test_pvalue(self, test: str = 'anova', paired: bool = False):
        """Add statistical test p-value."""
        if test not in ['anova', 't-test']:
            raise ValueError("test must be 'anova' or 't-test'")
        
        mapping = self.plot.mapping._starting
        x = mapping['x']
        y = mapping['y']
        
        if test == 'anova':
            groups = [group for name, group in self._obj.groupby(x)[y]]
            f_stat, p_val = stats.f_oneway(*groups)
        else:
            group1, group2 = [group for name, group in self._obj.groupby(x)[y]]
            if paired:
                t_stat, p_val = stats.ttest_rel(group1, group2)
            else:
                t_stat, p_val = stats.ttest_ind(group1, group2)
        
        y_max = self._obj[y].max()
        x_levels = self._obj[x].unique()
        x_pos = len(x_levels) // 2  # Position text above middle category
        
        self.plot = self.plot + annotate('text', x=x_levels[x_pos], y=y_max * 1.1,
                                       label=f'p = {p_val:.3f}')
        return self

    def add_correlation_text(self, method: str = 'pearson', format: str = '.2f'):
        """Add correlation coefficient text."""
        if method not in ['pearson', 'spearman']:
            raise ValueError("method must be 'pearson' or 'spearman'")
        
        mapping = self.plot.mapping
        x = mapping['x']
        y = mapping['y']
        
        if method == 'pearson':
            r, p = stats.pearsonr(self._obj[x], self._obj[y])
        else:
            r, p = stats.spearmanr(self._obj[x], self._obj[y])
        
        y_max = self._obj[y].max()
        x_mean = np.mean(self._obj[x])
        self.plot = self.plot + annotate('text', x=x_mean, y=y_max * 1.1,
                                       label=f'r = {r:{format}}\np = {p:{format}}')
        return self

    def add_regression_line(self, ci: bool = True, alpha: float = 0.2):
        """Add regression line with optional confidence interval."""
        self.plot = self.plot + geom_smooth(method='lm', se=ci, alpha=alpha)
        return self

    def add_quantiles(self, quantiles: List[float] = [0.25, 0.5, 0.75], alpha: float = 0.5, color: str = 'red'):
        """Add quantile lines."""
        mapping = self.plot.mapping
        x = mapping['x']
        y = mapping['y']
        
        for q in quantiles:
            # Calculate quantile values for each x
            df = pd.DataFrame()
            for x_val in sorted(self._obj[x].unique()):
                y_vals = self._obj[self._obj[x] == x_val][y]
                df = pd.concat([df, pd.DataFrame({
                    x: [x_val],
                    y: [np.quantile(y_vals, q)]
                })])
            
            # Add line for this quantile
            self.plot = self.plot + geom_line(data=df, mapping=aes(x=x, y=y),
                                            alpha=alpha, color=color)
        return self

    def add_density_2d(self, alpha: float = 0.6):
        """Add 2D density contours."""
        self.plot = self.plot + stat_density_2d(geom='polygon', alpha=alpha)
        return self
    
    def add_density_2d_filled(self, alpha: float = 0.6):
        """Add filled 2D density contours."""
        self.plot = self.plot + stat_density_2d(aes(fill='..level..'), geom='polygon', alpha=alpha)
        return self

    def add_dotplot(self, binwidth: float = 0.2, stackdir: str = 'up', binaxis: str = 'x'):
        """Add dot plot."""
        self.plot = self.plot + geom_dotplot(binwidth=binwidth, stackdir=stackdir, binaxis=binaxis)
        return self

    def add_step(self, direction: str = 'hv', **kwargs):
        """Add step plot."""
        self.plot = self.plot + geom_step(direction=direction, **kwargs)
        return self

    def add_rug(self, sides: str = 'b', alpha: float = 0.5, length: float = 0.03, **kwargs):
        """Add rug plot."""
        self.plot = self.plot + geom_rug(sides=sides, alpha=alpha, length=length, **kwargs)
        return self

    def add_count(self, stat: str = 'count', position: str = 'stack', **kwargs):
        """Add count plot."""
        self.plot = self.plot + geom_bar(stat=stat, position=position, **kwargs)
        return self

    def add_data_points_beeswarm(self, size: float = 3, alpha: float = 0.5, color: str = 'black', **kwargs):
        """Add beeswarm plot (approximated using controlled jitter)."""
        # Use jitter with very small width to approximate beeswarm
        self.plot = self.plot + geom_jitter(
            width=0.2, 
            height=0,
            size=size,
            alpha=alpha,
            color=color,
            random_state=42,  # For reproducibility
            **kwargs
        )
        return self

    def add_hline(self, yintercept: float, linetype: str = 'dashed', color: str = 'red', alpha: float = 1.0):
        """Add horizontal line."""
        self.plot = self.plot + geom_hline(yintercept=yintercept, linetype=linetype, color=color, alpha=alpha)
        return self

    def add_vline(self, xintercept: float, linetype: str = 'dashed', color: str = 'blue', alpha: float = 1.0):
        """Add vertical line."""
        self.plot = self.plot + geom_vline(xintercept=xintercept, linetype=linetype, color=color, alpha=alpha)
        return self

    def add_text(self, label: str, x: float, y: float, ha: str = 'right', va: str = 'bottom', size: int = 11, **kwargs):
        """Add text annotation."""
        self.plot = self.plot + annotate('text', x=x, y=y, label=label, ha=ha, va=va, size=size, **kwargs)
        return self

    def add_ribbon(self, ymin: str, ymax: str, alpha: float = 0.3, **kwargs):
        """Add ribbon plot."""
        self.plot = self.plot + geom_ribbon(aes(ymin=ymin, ymax=ymax), alpha=alpha, **kwargs)
        return self

    def adjust_labels(self, title: str = None, x: str = None, y: str = None):
        """Adjust plot labels."""
        self.plot = self.plot + labs(title=title, x=x, y=y)
        return self
    
    def adjust_colors(self, palette='jama', type='sequential'):
        """
        Adjust color palette for the plot.
        
        Args:
            palette (str): Name of the palette to use ('jama', 'nejm', 'lancet', etc.)
            type (str): Type of palette ('sequential', 'diverging', 'qualitative')
            
        Returns:
            TidyPlot: The plot object for method chaining
        """
        colors = palettes.get_palette(palette, type=type)
        
        # Add new scales, they will override any existing ones
        if 'fill' in self.plot.mapping:
            self.plot = self.plot + scale_fill_gradientn(colors=colors)
        if 'color' in self.plot.mapping:
            self.plot = self.plot + scale_color_gradientn(colors=colors)
        return self
    
    def adjust_axis_text_angle(self, angle: float = 45):
        """Rotate axis text."""
        self.plot = self.plot + theme(axis_text_x=element_text(angle=angle, hjust=1))
        return self
    
    def adjust_legend_position(self, position: str = 'right'):
        """Control legend placement."""
        if position not in ['right', 'left', 'top', 'bottom', 'none']:
            raise ValueError("position must be 'right', 'left', 'top', 'bottom', or 'none'")
        self.plot = self.plot + theme(legend_position=position)
        return self

    def remove_legend(self):
        """Remove the legend."""
        self.plot = self.plot + theme(legend_position='none')
        return self

    def show(self):
        """Display the plot."""
        # Draw the plot first if needed
        if self.plot is not None:
            self.plot.draw()
            
        # For matplotlib-based plots (pie charts)
        if hasattr(self, 'fig') and self.fig is not None:
            import matplotlib.pyplot as plt
            plt.show()
        # For plotnine-based plots
        elif hasattr(self, 'plot') and self.plot is not None:
            self.plot.show()
        else:
            raise ValueError("No plot to show. Create a plot first using one of the add_* methods.")
            
        return self
    
    def save(self, filepath):
        """Save the plot to a file."""
        # Create directory if it doesn't exist
        dirpath = os.path.dirname(filepath)
        if dirpath:  # Only create directories if path contains them
            os.makedirs(dirpath, exist_ok=True)
        
        if self.fig:  # For matplotlib-based plots (pie charts)
            self.fig.savefig(filepath, bbox_inches='tight')
        elif self.plot:  # For plotnine-based plots
            # Draw the plot
            fig = self.plot.draw()
            # Save the figure
            fig.savefig(filepath, bbox_inches='tight')
            # Close the figure to free memory
            plt.close(fig)
        return self

    def add_sum_bar(self, width: float = 0.7, alpha: float = 0.7):
        """Add bars showing sums."""
        self.plot = self.plot + stat_summary(fun_y=np.sum, geom='bar', width=width, alpha=alpha)
        return self

    def add_sum_dash(self, width: float = 0.7, alpha: float = 0.7):
        """Add dashes showing sums."""
        self.plot = self.plot + stat_summary(fun_y=np.sum, geom='linerange', width=width, alpha=alpha)
        return self

    def add_sum_dot(self, size: float = 3, alpha: float = 0.7):
        """Add dots showing sums."""
        self.plot = self.plot + stat_summary(fun_y=np.sum, geom='point', size=size, alpha=alpha)
        return self

    def add_sum_value(self, size: float = 11, format: str = "%.1f"):
        """Add text values showing sums."""
        def sum_label(x):
            return np.sum(x)
        self.plot = self.plot + stat_summary(fun_y=sum_label, geom='text', size=size, mapping=aes(label='y'), format_string=format)
        return self

    def add_sum_line(self, size: float = 1, alpha: float = 1):
        """Add lines showing sums."""
        self.plot = self.plot + stat_summary(fun_y=np.sum, geom='line', size=size, alpha=alpha)
        return self

    def add_sum_area(self, alpha: float = 0.7):
        """Add areas showing sums."""
        self.plot = self.plot + stat_summary(fun_y=np.sum, geom='area', alpha=alpha)
        return self

    def add_median_bar(self, width: float = 0.7, alpha: float = 0.7):
        """Add bars showing medians."""
        self.plot = self.plot + stat_summary(fun_y=np.median, geom='bar', width=width, alpha=alpha)
        return self

    def add_median_dash(self, width: float = 0.7, alpha: float = 0.7):
        """Add dashes showing medians."""
        self.plot = self.plot + stat_summary(fun_y=np.median, geom='linerange', width=width, alpha=alpha)
        return self

    def add_median_dot(self, size: float = 3, alpha: float = 0.7):
        """Add dots showing medians."""
        self.plot = self.plot + stat_summary(fun_y=np.median, geom='point', size=size, alpha=alpha)
        return self

    def add_median_value(self, size: float = 11, format: str = "%.1f"):
        """Add text values showing medians."""
        def median_label(x, format="%.1f"):
            """
            Calculate median and return numeric value.
            """
            return np.median(x)
        self.plot = self.plot + stat_summary(fun_y=median_label, geom='text', size=size, mapping=aes(label=after_stat('y')), format_string=format)
        return self

    def add_median_line(self, size: float = 1, alpha: float = 1, **kwargs):
        """Add lines showing medians."""
        self.plot = self.plot + stat_summary(fun_y=np.median, geom='line', size=size, alpha=alpha,  **kwargs)
        return self

    def add_median_area(self, alpha: float = 0.7):
        """Add areas showing medians."""
        self.plot = self.plot + stat_summary(fun_y=np.median, geom='area', alpha=alpha)
        return self

    def add_curve_fit(self):
        """Add fitted curve."""
        self.plot = self.plot + stat_smooth(method='loess', se=False)
        return self

    def add_sem_ribbon(self, alpha: float = 0.2, color: str = 'grey', **kwargs):
        """Add ribbon showing standard error of mean."""
        self.plot = self.plot + stat_smooth(method='loess', se=True, alpha=alpha, color=color, **kwargs)
        return self

    def add_range_ribbon(self, alpha: float = 0.2, color='grey', **kwargs):
        """Add ribbon showing range."""
        def range_fun(x):
            return pd.DataFrame({
                'y': [np.mean(x)],
                'ymin': [np.min(x)],
                'ymax': [np.max(x)]
            })
        self.plot = self.plot + stat_summary(fun_data=range_fun, geom='ribbon', alpha=alpha, color=color, **kwargs)
        return self

    def add_sd_ribbon(self, alpha: float = 0.2, color: str = 'grey', **kwargs):
        """Add ribbon showing standard deviation."""
        def sd_fun(x):
            return pd.DataFrame({
                'y': [np.mean(x)],
                'ymin': [np.mean(x) - np.std(x)],
                'ymax': [np.mean(x) + np.std(x)]
            })
        self.plot = self.plot + stat_summary(fun_data=sd_fun, geom='ribbon', alpha=alpha, color=color, **kwargs)
        return self

    def add_ci95_ribbon(self, alpha: float = 0.2, color='grey', **kwargs):
        """Add ribbon showing 95% confidence interval."""
        self.plot = self.plot + stat_smooth(method='lm', se=True, alpha=alpha, color=color, **kwargs)
        return self

    def add_barstack_absolute(self, stat: str = 'identity', width: float = 0.7, alpha: float = 0.7, **kwargs):
        """Add stacked bars (absolute)."""
        self.plot = self.plot + geom_bar(stat=stat, width=width, alpha=alpha, **kwargs)
        return self

    def add_barstack_relative(self, width: float = 0.7, alpha: float = 0.7, **kwargs):
        """Add stacked bars (relative)."""
        self.plot = self.plot + geom_bar(stat='identity', position='fill', width=width, alpha=alpha, **kwargs)
        return self

    def add_areastack_absolute(self, alpha: float = 0.7, **kwargs):
        """Add stacked areas (absolute)."""
        self.plot = self.plot + geom_area(position='stack', alpha=alpha, **kwargs)
        return self

    def add_areastack_relative(self, alpha: float = 0.7, **kwargs):
        """Add stacked areas (relative)."""
        self.plot = self.plot + geom_area(position='fill', alpha=alpha, **kwargs)
        return self

    def add_pie(self, **kwargs):
        """
        Add a pie chart layer to the plot.
        
        Args:
            show_labels (bool): Whether to show labels
            label_type (str): Type of labels ('value', 'percent', 'both')
            label_radius (float): Position of labels as fraction of radius
            label_size (float): Font size for labels
            sort (bool): Whether to sort slices by value
            start_angle (float): Starting angle in degrees
            inner_radius (float): Inner radius for donut chart
            **kwargs: Additional arguments passed to geom_pie
            
        Returns:
            TidyPlot: The plot object for method chaining
        """
        self.plot = self.plot + geom_pie(**kwargs)
        return self

    def add_donut(self, inner_radius=0.6, **kwargs):
        """
        Add a donut chart layer to the plot.
        
        Args:
            inner_radius (float): Inner radius as fraction of outer radius
            **kwargs: Additional arguments passed to add_pie
            
        Returns:
            TidyPlot: The plot object for method chaining
        """
        return self.add_pie(inner_radius=inner_radius, **kwargs)

    def add_rose(self, **kwargs):
        """
        Add a Nightingale Rose Chart layer to the plot.
        
        Args:
            show_labels (bool): Whether to show labels
            label_type (str): Type of labels ('value', 'percent', 'both')
            label_radius (float): Position of labels as fraction of radius
            label_size (float): Font size for labels
            sort (bool): Whether to sort slices by value
            start_angle (float): Starting angle in degrees
            **kwargs: Additional arguments passed to geom_rose
            
        Returns:
            TidyPlot: The plot object for method chaining
        """
        self.plot = self.plot + geom_rose(**kwargs)
        return self

    def adjust_title(self, text: str, size: float = 14):
        """Modify plot title."""
        self.plot = self.plot + theme(plot_title=element_text(size=size)) + labs(title=text)
        return self
    
    def adjust_x_axis_title(self, text: str, size: float = 11):
        """Modify x axis title."""
        self.plot = self.plot + theme(axis_title_x=element_text(size=size)) + labs(x=text)
        return self

    def adjust_y_axis_title(self, text: str, size: float = 11):
        """Modify y axis title."""
        self.plot = self.plot + theme(axis_title_y=element_text(size=size)) + labs(y=text)
        return self

    def adjust_caption(self, text: str, size: float = 10):
        """Modify plot caption."""
        self.plot = self.plot + theme(plot_caption=element_text(size=size)) + labs(caption=text)
        return self

    def adjust_size(self, width: float, height: float):
        """Modify plot size."""
        self.plot = self.plot + theme(figure_size=(width, height))
        return self

    def adjust_padding(self, left: float = 0.1, right: float = 0.1, top: float = 0.1, bottom: float = 0.1):
        """Modify plot padding."""
        # Convert the values to a tuple of numbers in inches
        margin = (top, right, bottom, left)
        self.plot = self.plot + theme(plot_margin=margin)
        return self
    
    def adjust_x_axis(self, limits: tuple = None, breaks: list = None, labels: list = None):
        """Modify x axis properties."""
        if limits:
            self.plot = self.plot + scale_x_continuous(limits=limits)
        if breaks:
            self.plot = self.plot + scale_x_continuous(breaks=breaks)
        if labels:
            self.plot = self.plot + scale_x_continuous(labels=labels)
        return self

    def adjust_y_axis(self, limits: tuple = None, breaks: list = None, labels: list = None):
        """Modify y axis properties."""
        if limits:
            self.plot = self.plot + scale_y_continuous(limits=limits)
        if breaks:
            self.plot = self.plot + scale_y_continuous(breaks=breaks)
        if labels:
            self.plot = self.plot + scale_y_continuous(labels=labels)
        return self

    def rename_y_axis_labels(self, mapping: dict):
        """Rename y axis labels."""
        self.plot = self.plot + scale_y_discrete(labels=mapping)
        return self

    def rename_x_axis_labels(self, mapping: Dict[str, str]):
        """Rename x-axis labels using a mapping dictionary."""
        self.plot = self.plot + scale_x_discrete(labels=mapping)
        return self

    def rename_color_labels(self, mapping: dict):
        """Rename color labels."""
        if 'color' in self.plot.mapping:
            self.plot = self.plot + scale_color_discrete(labels=mapping)
        else:
            self.plot = self.plot + scale_fill_discrete(labels=mapping)
        return self

    def reorder_x_axis_labels(self, order: list):
        """Reorder x axis labels."""
        self.plot = self.plot + scale_x_discrete(limits=order)
        return self

    def reorder_y_axis_labels(self, order: list):
        """Reorder y axis labels."""
        self.plot = self.plot + scale_y_discrete(limits=order)
        return self

    def reorder_color_labels(self, order: list):
        """Reorder color labels."""
        if 'color' in self.plot.mapping:
            self.plot = self.plot + scale_color_discrete(limits=order)
        else:
            self.plot = self.plot + scale_fill_discrete(limits=order)
        return self

    def sort_x_axis_labels(self, ascending: bool = True):
        """Sort x axis labels."""
        x = self.plot.mapping['x']
        order = sorted(self._obj[x].unique(), reverse=not ascending)
        return self.reorder_x_axis_labels(order)

    def sort_y_axis_labels(self, ascending: bool = True):
        """Sort y axis labels."""
        y = self.plot.mapping['y']
        order = sorted(self._obj[y].unique(), reverse=not ascending)
        return self.reorder_y_axis_labels(order)

    def sort_color_labels(self, ascending: bool = True):
        """Sort color labels."""
        if 'color' in self.plot.mapping:
            color = self.plot.mapping['color']
            order = sorted(self._obj[color].unique(), reverse=not ascending)
        else:
            color = self.plot.mapping.get('fill')
            if color:
                order = sorted(self._obj[color].unique(), reverse=not ascending)
            else:
                return self
        return self.reorder_color_labels(order)

    def reverse_x_axis_labels(self):
        """Reverse x axis labels."""
        x = self.plot.mapping['x']
        order = list(reversed(self._obj[x].unique()))
        return self.reorder_x_axis_labels(order)

    def reverse_y_axis_labels(self):
        """Reverse y axis labels."""
        y = self.plot.mapping['y']
        order = list(reversed(self._obj[y].unique()))
        return self.reorder_y_axis_labels(order)

    def reverse_color_labels(self):
        """Reverse color labels."""
        if 'color' in self.plot.mapping:
            color = self.plot.mapping['color']
            order = list(reversed(self._obj[color].unique()))
        else:
            color = self.plot.mapping.get('fill')
            if color:
                order = list(reversed(self._obj[color].unique()))
            else:
                return self
        return self.reorder_color_labels(order)

    def add_pvalue(self,p: float, x1: float, x2: float, y: float, height: float = 0.02,
                  format: str = "stars") -> List[Any]:
        """Add p-value annotation with bracket.
        
        Parameters:
        -----------
        p : float
            P-value to display
        x1, x2 : float
            x-coordinates for bracket ends
        y : float
            y-coordinate for bracket
        height : float
            Height of the bracket
        format : str
            Format for p-value display ('stars' or 'numeric')
            
        Returns:
        --------
        list
            List of annotation layers
        """
        if format == "stars":
            if p < 0.001:
                text = "***"
            elif p < 0.01:
                text = "**"
            elif p < 0.05:
                text = "*"
            else:
                text = "ns"
        else:
            text = f"p = {p:.3f}"
            
        return [
            geom_segment(aes(x=x1, xend=x1, y=y, yend=y+height)),
            geom_segment(aes(x=x2, xend=x2, y=y, yend=y+height)),
            geom_segment(aes(x=x1, xend=x2, y=y+height, yend=y+height)),
            annotate("text", x=(x1+x2)/2, y=y+height, label=text, size=8)
        ]

    def add_heatmap(self, show_values=False, value_format='{:.2f}', alpha=1):
        """
        Add a heatmap visualization to the plot.
        
        Args:
            show_values (bool): Whether to show values in each cell
            value_format (str): Format string for values (e.g., '{:.2f}' for 2 decimal places)
            alpha (float): Opacity of the heatmap cells
            
        Returns:
            TidyPlot: The plot object for method chaining
        """
        # Add heatmap tiles
        self.plot = self.plot + geom_tile(alpha=alpha)
        
        # Apply default palette if no palette has been set and no fill scale exists
        if 'fill' in self.plot.mapping:
            has_fill_scale = any(isinstance(layer, scale_fill_gradientn) for layer in self.plot.layers)
            has_fill_manual = any(isinstance(layer, scale_fill_manual) for layer in self.plot.layers)
            if not (has_fill_scale or has_fill_manual):
                self.adjust_colors(palette=self._default_palette)
        
        # Add value labels if requested
        if show_values:
            self.plot = self.plot + geom_text(
                aes(label='value'),  # Use the value column as the label
                format_string=value_format,
                size=8
            )
        
        # Remove axis elements
        self.plot = self.plot + theme(
            axis_title=element_blank(),
            axis_text=element_blank(),
            axis_ticks=element_blank(),
            axis_line=element_blank(),
            panel_grid_major=element_blank(),
            panel_grid_minor=element_blank()
        )
        
        return self

    def add_curve_fit(self):
        """Add fitted curve."""
        self.plot = self.plot + stat_smooth(method='loess', se=False)
        return self

    def add_sem_ribbon(self, alpha: float = 0.2, color: str = 'grey', **kwargs):
        """Add ribbon showing standard error of mean."""
        self.plot = self.plot + stat_smooth(method='loess', se=True, alpha=alpha, color=color, **kwargs)
        return self

    def add_range_ribbon(self, alpha: float = 0.2, color='grey', **kwargs):
        """Add ribbon showing range."""
        def range_fun(x):
            return pd.DataFrame({
                'y': [np.mean(x)],
                'ymin': [np.min(x)],
                'ymax': [np.max(x)]
            })
        self.plot = self.plot + stat_summary(fun_data=range_fun, geom='ribbon', alpha=alpha, color=color, **kwargs)
        return self

    def add_sd_ribbon(self, alpha: float = 0.2, color: str = 'grey', **kwargs):
        """Add ribbon showing standard deviation."""
        def sd_fun(x):
            return pd.DataFrame({
                'y': [np.mean(x)],
                'ymin': [np.mean(x) - np.std(x)],
                'ymax': [np.mean(x) + np.std(x)]
            })
        self.plot = self.plot + stat_summary(fun_data=sd_fun, geom='ribbon', alpha=alpha, color=color, **kwargs)
        return self

    def add_ci95_ribbon(self, alpha: float = 0.2, color='grey', **kwargs):
        """Add ribbon showing 95% confidence interval."""
        self.plot = self.plot + stat_smooth(method='lm', se=True, alpha=alpha, color=color, **kwargs)
        return self

    def add_barstack_absolute(self, stat: str = 'identity', width: float = 0.7, alpha: float = 0.7, **kwargs):
        """Add stacked bars (absolute)."""
        self.plot = self.plot + geom_bar(stat=stat, width=width, alpha=alpha, **kwargs)
        return self

    def add_barstack_relative(self, width: float = 0.7, alpha: float = 0.7, **kwargs):
        """Add stacked bars (relative)."""
        self.plot = self.plot + geom_bar(stat='identity', position='fill', width=width, alpha=alpha, **kwargs)
        return self

    def add_areastack_absolute(self, alpha: float = 0.7, **kwargs):
        """Add stacked areas (absolute)."""
        self.plot = self.plot + geom_area(position='stack', alpha=alpha, **kwargs)
        return self

    def add_areastack_relative(self, alpha: float = 0.7, **kwargs):
        """Add stacked areas (relative)."""
        self.plot = self.plot + geom_area(position='fill', alpha=alpha, **kwargs)
        return self

    def add_pie(self, **kwargs):
        """
        Add a pie chart layer to the plot.
        
        Args:
            show_labels (bool): Whether to show labels
            label_type (str): Type of labels ('value', 'percent', 'both')
            label_radius (float): Position of labels as fraction of radius
            label_size (float): Font size for labels
            sort (bool): Whether to sort slices by value
            start_angle (float): Starting angle in degrees
            inner_radius (float): Inner radius for donut chart
            **kwargs: Additional arguments passed to geom_pie
            
        Returns:
            TidyPlot: The plot object for method chaining
        """
        self.plot = self.plot + geom_pie(**kwargs)
        return self

    def add_donut(self, inner_radius=0.6, **kwargs):
        """
        Add a donut chart layer to the plot.
        
        Args:
            inner_radius (float): Inner radius as fraction of outer radius
            **kwargs: Additional arguments passed to add_pie
            
        Returns:
            TidyPlot: The plot object for method chaining
        """
        return self.add_pie(inner_radius=inner_radius, **kwargs)

    def add_rose(self, **kwargs):
        """
        Add a Nightingale Rose Chart layer to the plot.
        
        Args:
            show_labels (bool): Whether to show labels
            label_type (str): Type of labels ('value', 'percent', 'both')
            label_radius (float): Position of labels as fraction of radius
            label_size (float): Font size for labels
            sort (bool): Whether to sort slices by value
            start_angle (float): Starting angle in degrees
            **kwargs: Additional arguments passed to geom_rose
            
        Returns:
            TidyPlot: The plot object for method chaining
        """
        self.plot = self.plot + geom_rose(**kwargs)
        return self

    def adjust_title(self, text: str, size: float = 14):
        """Modify plot title."""
        self.plot = self.plot + theme(plot_title=element_text(size=size)) + labs(title=text)
        return self
    
    def adjust_x_axis_title(self, text: str, size: float = 11):
        """Modify x axis title."""
        self.plot = self.plot + theme(axis_title_x=element_text(size=size)) + labs(x=text)
        return self

    def adjust_y_axis_title(self, text: str, size: float = 11):
        """Modify y axis title."""
        self.plot = self.plot + theme(axis_title_y=element_text(size=size)) + labs(y=text)
        return self

    def adjust_caption(self, text: str, size: float = 10):
        """Modify plot caption."""
        self.plot = self.plot + theme(plot_caption=element_text(size=size)) + labs(caption=text)
        return self

    def adjust_size(self, width: float, height: float):
        """Modify plot size."""
        self.plot = self.plot + theme(figure_size=(width, height))
        return self

    def adjust_padding(self, left: float = 0.1, right: float = 0.1, top: float = 0.1, bottom: float = 0.1):
        """Modify plot padding."""
        # Convert the values to a tuple of numbers in inches
        margin = (top, right, bottom, left)
        self.plot = self.plot + theme(plot_margin=margin)
        return self
    
    def adjust_x_axis(self, limits: tuple = None, breaks: list = None, labels: list = None):
        """Modify x axis properties."""
        if limits:
            self.plot = self.plot + scale_x_continuous(limits=limits)
        if breaks:
            self.plot = self.plot + scale_x_continuous(breaks=breaks)
        if labels:
            self.plot = self.plot + scale_x_continuous(labels=labels)
        return self

    def adjust_y_axis(self, limits: tuple = None, breaks: list = None, labels: list = None):
        """Modify y axis properties."""
        if limits:
            self.plot = self.plot + scale_y_continuous(limits=limits)
        if breaks:
            self.plot = self.plot + scale_y_continuous(breaks=breaks)
        if labels:
            self.plot = self.plot + scale_y_continuous(labels=labels)
        return self

    def rename_y_axis_labels(self, mapping: dict):
        """Rename y axis labels."""
        self.plot = self.plot + scale_y_discrete(labels=mapping)
        return self

    def rename_x_axis_labels(self, mapping: Dict[str, str]):
        """Rename x-axis labels using a mapping dictionary."""
        self.plot = self.plot + scale_x_discrete(labels=mapping)
        return self

    def rename_color_labels(self, mapping: dict):
        """Rename color labels."""
        if 'color' in self.plot.mapping:
            self.plot = self.plot + scale_color_discrete(labels=mapping)
        else:
            self.plot = self.plot + scale_fill_discrete(labels=mapping)
        return self

    def reorder_x_axis_labels(self, order: list):
        """Reorder x axis labels."""
        self.plot = self.plot + scale_x_discrete(limits=order)
        return self

    def reorder_y_axis_labels(self, order: list):
        """Reorder y axis labels."""
        self.plot = self.plot + scale_y_discrete(limits=order)
        return self

    def reorder_color_labels(self, order: list):
        """Reorder color labels."""
        if 'color' in self.plot.mapping:
            self.plot = self.plot + scale_color_discrete(limits=order)
        else:
            self.plot = self.plot + scale_fill_discrete(limits=order)
        return self

    def sort_x_axis_labels(self, ascending: bool = True):
        """Sort x axis labels."""
        x = self.plot.mapping['x']
        order = sorted(self._obj[x].unique(), reverse=not ascending)
        return self.reorder_x_axis_labels(order)

    def sort_y_axis_labels(self, ascending: bool = True):
        """Sort y axis labels."""
        y = self.plot.mapping['y']
        order = sorted(self._obj[y].unique(), reverse=not ascending)
        return self.reorder_y_axis_labels(order)

    def sort_color_labels(self, ascending: bool = True):
        """Sort color labels."""
        if 'color' in self.plot.mapping:
            color = self.plot.mapping['color']
            order = sorted(self._obj[color].unique(), reverse=not ascending)
        else:
            color = self.plot.mapping.get('fill')
            if color:
                order = sorted(self._obj[color].unique(), reverse=not ascending)
            else:
                return self
        return self.reorder_color_labels(order)

    def reverse_x_axis_labels(self):
        """Reverse x axis labels."""
        x = self.plot.mapping['x']
        order = list(reversed(self._obj[x].unique()))
        return self.reorder_x_axis_labels(order)

    def reverse_y_axis_labels(self):
        """Reverse y axis labels."""
        y = self.plot.mapping['y']
        order = list(reversed(self._obj[y].unique()))
        return self.reorder_y_axis_labels(order)

    def reverse_color_labels(self):
        """Reverse color labels."""
        if 'color' in self.plot.mapping:
            color = self.plot.mapping['color']
            order = list(reversed(self._obj[color].unique()))
        else:
            color = self.plot.mapping.get('fill')
            if color:
                order = list(reversed(self._obj[color].unique()))
            else:
                return self
        return self.reorder_color_labels(order)

    def add_pvalue(self,p: float, x1: float, x2: float, y: float, height: float = 0.02,
                  format: str = "stars") -> List[Any]:
        """Add p-value annotation with bracket.
        
        Parameters:
        -----------
        p : float
            P-value to display
        x1, x2 : float
            x-coordinates for bracket ends
        y : float
            y-coordinate for bracket
        height : float
            Height of the bracket
        format : str
            Format for p-value display ('stars' or 'numeric')
            
        Returns:
        --------
        list
            List of annotation layers
        """
        if format == "stars":
            if p < 0.001:
                text = "***"
            elif p < 0.01:
                text = "**"
            elif p < 0.05:
                text = "*"
            else:
                text = "ns"
        else:
            text = f"p = {p:.3f}"
            
        return [
            geom_segment(aes(x=x1, xend=x1, y=y, yend=y+height)),
            geom_segment(aes(x=x2, xend=x2, y=y, yend=y+height)),
            geom_segment(aes(x=x1, xend=x2, y=y+height, yend=y+height)),
            annotate("text", x=(x1+x2)/2, y=y+height, label=text, size=8)
        ]

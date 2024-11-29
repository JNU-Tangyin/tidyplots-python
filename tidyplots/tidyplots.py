"""A Python library for creating publication-ready plots with a fluent, chainable interface."""

import pandas as pd
import numpy as np
from plotnine import (
    ggplot, aes, labs, annotate,
    # Geometries
    geom_point, geom_line, geom_bar, geom_boxplot, geom_violin, 
    geom_density, geom_step, geom_dotplot, geom_jitter, geom_text, 
    geom_smooth, geom_quantile, geom_rug, geom_ribbon, geom_area,
    geom_hline, geom_vline, geom_errorbar,
    # Stats
    stat_density_2d, stat_count, stat_bin_2d, stat_summary, stat_smooth,
    # Positions
    position_jitterdodge, position_stack, position_fill,
    # Coordinates and scales
    coord_flip, scale_x_continuous, scale_y_continuous, scale_x_discrete,
    scale_color_manual, scale_fill_manual,
    # Themes and elements
    theme, theme_minimal, element_text, element_blank, facet_wrap,
    # Guides
    guides, guide_legend
)
from typing import Optional, List, Union, Dict, Any
from . import palettes
from . import themes
import scipy.stats as stats

@pd.api.extensions.register_dataframe_accessor("tidyplot")
class TidyPlot:
    """A fluent interface for creating publication-ready plots."""
    
    def __init__(self, pandas_obj):
        """Initialize TidyPlot with a pandas DataFrame."""
        self._obj = pandas_obj
        self.plot = None
        self.prism = themes.TidyPrism()
    
    def __call__(self, x: str, y: str = None, color: Optional[str] = None, fill: Optional[str] = None):
        """Create a new plot with the given aesthetics.
        
        Parameters:
        -----------
        x : str
            Column name for x-axis
        y : str, optional
            Column name for y-axis
        color : str, optional
            Column name for color aesthetic
        fill : str, optional
            Column name for fill aesthetic
        """
        mapping = aes(x=x)
        if y is not None:
            mapping = aes(x=x, y=y)
        if color is not None:
            mapping = aes(x=x, y=y, color=color) if y is not None else aes(x=x, color=color)
        if fill is not None:
            mapping = aes(x=x, y=y, fill=fill) if y is not None else aes(x=x, fill=fill)
            
        self.plot = (ggplot(self._obj, mapping) +
                    themes.TidyPrism.theme_prism())  # Use Prism theme by default
        
        # Apply NPG colors by default
        colors = palettes.get_palette('npg')
        if 'y' not in mapping:
            self.plot = self.plot + scale_fill_manual(values=colors)
        else:
            if color is not None:
                self.plot = self.plot + scale_color_manual(values=colors)
                
        return self
    
    def add_scatter(self, alpha: float = 0.6, size: float = 3):
        """Add scatter points to the plot."""
        self.plot = self.plot + geom_point(alpha=alpha, size=size)
        return self
    
    def add_line(self, alpha: float = 0.8, size: float = 1):
        """Add line to the plot."""
        self.plot = self.plot + geom_line(alpha=alpha, size=size)
        return self
    
    def add_smooth(self, method: str = 'lm', se: bool = True, alpha: float = 0.2):
        """Add smoothed conditional means."""
        self.plot = self.plot + stat_smooth(method=method, se=se, alpha=alpha)
        return self
    
    def add_bar(self, stat: str = 'identity', width: float = 0.7, alpha: float = 0.7):
        """Add bar plot."""
        self.plot = self.plot + geom_bar(stat=stat, width=width, alpha=alpha)
        return self
    
    def add_boxplot(self, alpha: float = 0.3, outlier_alpha: float = 0.5):
        """Add boxplot to the plot."""
        self.plot = self.plot + geom_boxplot(alpha=alpha, outlier_alpha=outlier_alpha)
        return self
    
    def add_violin(self, alpha: float = 0.4, draw_quantiles: List[float] = [0.25, 0.5, 0.75]):
        """Add violin plot."""
        self.plot = self.plot + geom_violin(alpha=alpha, draw_quantiles=draw_quantiles)
        return self
    
    def add_density(self, alpha: float = 0.3):
        """Add density plot."""
        self.plot = self.plot + geom_density(alpha=alpha)
        return self
    
    def add_hex(self, bins: int = 20):
        """Add hexagonal binning."""
        self.plot = self.plot + stat_bin_2d(bins=bins)
        return self
    
    def add_errorbar(self, ymin: str, ymax: str, alpha: float = 0.8, width: float = 0.2):
        """Add error bars with explicit min/max values."""
        self.plot = self.plot + geom_errorbar(
            aes(ymin=ymin, ymax=ymax), 
            alpha=alpha, 
            width=width
        )
        return self
    
    def add_data_points_jitter(self, width: float = 0.2, height: float = 0, alpha: float = 0.5, point_size: float = 3):
        """Add jittered points to the plot."""
        self.plot = self.plot + geom_jitter(width=width, height=height, alpha=alpha, size=point_size)
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
        
        mapping = self.plot.mapping
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
        self.plot = self.plot + stat_smooth(method='lm', se=ci, alpha=alpha)
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

    def add_step(self, direction: str = 'hv'):
        """Add step plot."""
        self.plot = self.plot + geom_step(direction=direction)
        return self

    def add_rug(self, sides: str = 'b', alpha: float = 0.5, length: float = 0.03):
        """Add rug plot."""
        self.plot = self.plot + geom_rug(sides=sides, alpha=alpha, length=length)
        return self

    def add_count(self, stat: str = 'count', position: str = 'stack'):
        """Add count plot."""
        self.plot = self.plot + geom_bar(stat=stat, position=position)
        return self

    def add_data_points_beeswarm(self, size: float = 3, alpha: float = 0.5):
        """Add beeswarm plot (approximated using controlled jitter)."""
        # Use jitter with very small width to approximate beeswarm
        self.plot = self.plot + geom_jitter(
            width=0.2, 
            height=0,
            size=size,
            alpha=alpha,
            random_state=42  # For reproducibility
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

    def add_text(self, label: str, x: float, y: float, ha: str = 'right', va: str = 'bottom', size: int = 11):
        """Add text annotation."""
        self.plot = self.plot + annotate('text', x=x, y=y, label=label, ha=ha, va=va, size=size)
        return self

    def add_ribbon(self, ymin: str, ymax: str, alpha: float = 0.3):
        """Add ribbon plot."""
        self.plot = self.plot + geom_ribbon(aes(ymin=ymin, ymax=ymax), alpha=alpha)
        return self

    def adjust_labels(self, title: str = None, x: str = None, y: str = None):
        """Adjust plot labels."""
        self.plot = self.plot + labs(title=title, x=x, y=y)
        return self
    
    def adjust_colors(self, palette: str = 'npg'):
        """Change color palette."""
        colors = palettes.get_palette(palette)
        if 'y' not in self.plot.mapping:
            self.plot = self.plot + scale_fill_manual(values=colors)
        else:
            if 'color' in self.plot.mapping:
                self.plot = self.plot + scale_color_manual(values=colors)
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
        return self.plot
    
    def save(self, filename: str, **kwargs):
        """Save the plot to a file."""
        self.plot.save(filename, **kwargs)
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
            return f"{np.sum(x):{format}}"
        self.plot = self.plot + stat_summary(fun_y=sum_label, geom='text', size=size)
        return self

    def add_sum_line(self, size: float = 1, alpha: float = 1):
        """Add lines showing sums."""
        self.plot = self.plot + stat_summary(fun_y=np.sum, geom='line', size=size, alpha=alpha)
        return self

    def add_sum_area(self, alpha: float = 0.7):
        """Add areas showing sums."""
        self.plot = self.plot + stat_summary(fun_y=np.sum, geom='area', alpha=alpha)
        return self

    def add_heatmap(self, alpha: float = 0.7):
        """Add heatmap visualization."""
        self.plot = self.plot + geom_tile(alpha=alpha)
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
        def median_label(x):
            return f"{np.median(x):{format}}"
        self.plot = self.plot + stat_summary(fun_y=median_label, geom='text', size=size)
        return self

    def add_median_line(self, size: float = 1, alpha: float = 1):
        """Add lines showing medians."""
        self.plot = self.plot + stat_summary(fun_y=np.median, geom='line', size=size, alpha=alpha)
        return self

    def add_median_area(self, alpha: float = 0.7):
        """Add areas showing medians."""
        self.plot = self.plot + stat_summary(fun_y=np.median, geom='area', alpha=alpha)
        return self

    def add_curve_fit(self):
        """Add fitted curve."""
        self.plot = self.plot + stat_smooth(method='loess', se=False)
        return self

    def add_sem_ribbon(self, alpha: float = 0.2):
        """Add ribbon showing standard error of mean."""
        self.plot = self.plot + stat_smooth(method='loess', se=True, alpha=alpha)
        return self

    def add_range_ribbon(self, alpha: float = 0.2):
        """Add ribbon showing range."""
        def range_fun(x):
            return pd.DataFrame({
                'y': [np.mean(x)],
                'ymin': [np.min(x)],
                'ymax': [np.max(x)]
            })
        self.plot = self.plot + stat_summary(fun_data=range_fun, geom='ribbon', alpha=alpha)
        return self

    def add_sd_ribbon(self, alpha: float = 0.2):
        """Add ribbon showing standard deviation."""
        def sd_fun(x):
            return pd.DataFrame({
                'y': [np.mean(x)],
                'ymin': [np.mean(x) - np.std(x)],
                'ymax': [np.mean(x) + np.std(x)]
            })
        self.plot = self.plot + stat_summary(fun_data=sd_fun, geom='ribbon', alpha=alpha)
        return self

    def add_ci95_ribbon(self, alpha: float = 0.2):
        """Add ribbon showing 95% confidence interval."""
        self.plot = self.plot + stat_smooth(method='lm', se=True, alpha=alpha)
        return self

    def add_barstack_absolute(self, width: float = 0.7, alpha: float = 0.7):
        """Add stacked bars (absolute)."""
        self.plot = self.plot + geom_bar(stat='identity', position='stack', width=width, alpha=alpha)
        return self

    def add_barstack_relative(self, width: float = 0.7, alpha: float = 0.7):
        """Add stacked bars (relative)."""
        self.plot = self.plot + geom_bar(stat='identity', position='fill', width=width, alpha=alpha)
        return self

    def add_areastack_absolute(self, alpha: float = 0.7):
        """Add stacked areas (absolute)."""
        self.plot = self.plot + geom_area(position='stack', alpha=alpha)
        return self

    def add_areastack_relative(self, alpha: float = 0.7):
        """Add stacked areas (relative)."""
        self.plot = self.plot + geom_area(position='fill', alpha=alpha)
        return self

    def add_pie(self):
        """Add pie chart."""
        self.plot = self.plot + geom_bar(stat='identity', position='fill', width=1)
        return self

    def add_donut(self, inner_radius: float = 0.5):
        """Add donut chart."""
        self.plot = (self.plot + 
                    geom_bar(stat='identity', position='fill', width=1) +
                    theme(aspect_ratio=1) +
                    theme(panel_grid=element_blank()) +
                    theme(axis_text=element_blank()) +
                    theme(axis_ticks=element_blank()))
        return self

    def add_data_labels_repel(self, size: float = 8):
        """Add data labels with repulsion to avoid overlapping."""
        value_label = self._obj[self._obj.columns[0]].astype(str)
        self.plot = self.plot + geom_text(aes(label=value_label), size=size, va='bottom', nudge_y=0.05)
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
        self.plot = self.plot + theme(plot_margin={"l": left, "r": right, "t": top, "b": bottom})
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

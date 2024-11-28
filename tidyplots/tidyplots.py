"""A Python library for creating publication-ready plots with a fluent, chainable interface."""

import pandas as pd
import numpy as np
from plotnine import *
from plotnine import (
    ggplot, aes, labs, annotate,
    # Geometries
    geom_point, geom_line, geom_bar, geom_boxplot,
    geom_violin, geom_density, geom_errorbar, geom_text,
    geom_step, geom_dotplot, geom_jitter, geom_hline, geom_vline, geom_ribbon,
    geom_rug,
    # Statistics
    stat_summary, stat_density_2d, stat_smooth, stat_bin_2d,
    # Scales
    scale_x_continuous, scale_y_continuous,
    scale_color_manual, scale_fill_manual,
    # Themes
    theme, element_text, facet_wrap
)
from plotnine.stats import stat_bin_2d
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
    
    def __call__(self, x: str, y: str = None, color: Optional[str] = None):
        """Create a new plot with the given aesthetics.
        
        Parameters:
        -----------
        x : str
            Column name for x-axis
        y : str, optional
            Column name for y-axis
        color : str, optional
            Column name for color aesthetic
        """
        mapping = aes(x=x)
        if y is not None:
            mapping = aes(x=x, y=y)
            if color is not None:
                mapping = aes(x=x, y=y, color=color)
        else:
            if color is not None:
                mapping = aes(x=x, fill=color)
            
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

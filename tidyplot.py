'''
tidyplot is a brandnew, light-weight, publish ready R package for plotting.
https://github.com/jbengler/tidyplots
here use monkey patching to add a tidyplot() method to pd.Dataframe.
Then people can use df.tidyplot() in the code.
'''
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import sem
from typing import Optional, Union, Literal
import warnings
from plotnine import *
import pandas as pd

class TidyPlot:
    def __init__(self, data: pd.DataFrame, x: str, y: str = None, color: Optional[str] = None):
        """Initialize TidyPlot with data and mapping.
        
        Parameters:
        -----------
        data : pd.DataFrame
            Input data
        x : str
            Column name for x-axis
        y : str, optional
            Column name for y-axis. Not required for count plots.
        color : str, optional
            Column name for color grouping
        """
        self.data = data
        self.x = x
        self.y = y
        self.color = color
        self.mapping = aes(x=x)
        if y is not None:
            self.mapping = aes(x=x, y=y)
        if color:
            if y is not None:
                self.mapping = aes(x=x, y=y, color=color)
            else:
                self.mapping = aes(x=x, fill=color)  # Use fill for discrete color mapping
        self.plot = (ggplot(data, self.mapping)
                    + theme_minimal())
        if color and y is None:
            self.plot = self.plot + aes(fill=color)  # Use fill for discrete color mapping

    # Add data visualization elements
    def add_mean_bar(self, alpha: float = 0.4, width: float = 0.7):
        """Add bars showing mean values."""
        self.plot = self.plot + stat_summary(fun_y=np.mean, geom='bar', 
                                           alpha=alpha, width=width)
        return self

    def add_sem_errorbar(self, width: float = 0.2):
        """Add error bars showing standard error of the mean."""
        self.plot = self.plot + stat_summary(fun_data='mean_se', 
                                           geom='errorbar', width=width)
        return self

    def add_sd_errorbar(self, width: float = 0.2):
        """Add error bars showing standard deviation."""
        def sd_fun(y):
            return {'y': np.mean(y), 'ymin': np.mean(y) - np.std(y), 
                   'ymax': np.mean(y) + np.std(y)}
        self.plot = self.plot + stat_summary(fun_data=sd_fun, 
                                           geom='errorbar', width=width)
        return self

    def add_ci_errorbar(self, width: float = 0.2, ci: float = 0.95):
        """Add error bars showing confidence interval."""
        def ci_fun(y):
            from scipy import stats
            mean = np.mean(y)
            ci_val = stats.t.interval(ci, len(y)-1, loc=mean, scale=stats.sem(y))
            return {'y': mean, 'ymin': ci_val[0], 'ymax': ci_val[1]}
        self.plot = self.plot + stat_summary(fun_data=ci_fun, 
                                           geom='errorbar', width=width)
        return self

    def add_data_points_beeswarm(self, size: float = 3, alpha: float = 0.5):
        """Add individual data points in a beeswarm arrangement."""
        self.plot = self.plot + geom_point(position=position_jitter(width=0.2), 
                                         size=size, alpha=alpha)
        return self

    def add_data_points_jitter(self, width: float = 0.2, size: float = 3, 
                              alpha: float = 0.5):
        """Add jittered data points."""
        self.plot = self.plot + geom_jitter(width=width, size=size, alpha=alpha)
        return self

    def add_violin(self, alpha: float = 0.4, draw_quantiles: list = [0.25, 0.5, 0.75]):
        """Add violin plot."""
        self.plot = self.plot + geom_violin(alpha=alpha, draw_quantiles=draw_quantiles)
        return self

    def add_density(self, alpha: float = 0.4):
        """Add density plot."""
        self.plot = self.plot + geom_density(alpha=alpha)
        return self

    def add_boxplot(self, alpha: float = 0.4, outlier_alpha: float = 0.5):
        """Add box plot."""
        self.plot = self.plot + geom_boxplot(alpha=alpha, outlier_alpha=outlier_alpha)
        return self

    def add_line(self, size: float = 1, alpha: float = 1.0):
        """Add line plot."""
        self.plot = self.plot + geom_line(size=size, alpha=alpha)
        return self

    def add_scatter(self, size: float = 3, alpha: float = 0.7):
        """Add scatter plot."""
        self.plot = self.plot + geom_point(size=size, alpha=alpha)
        return self

    def add_dotplot(self, binwidth: float = None, stackdir: str = "up", binaxis: str = "x"):
        """Add dot plot with stacking.
        
        Parameters:
        -----------
        binwidth : float, optional
            The width of the bins. If None, uses a suitable default
        stackdir : str
            Direction of stacking ("up", "down", "center")
        binaxis : str
            The axis to bin along ("x" or "y")
        """
        self.plot = self.plot + geom_dotplot(
            binwidth=binwidth,
            stackdir=stackdir,
            binaxis=binaxis
        )
        return self

    def add_count(self, stat: str = "count", position: str = "stack"):
        """Add count plot.
        
        Parameters:
        -----------
        stat : str
            The statistic to use ("count" or "proportion")
        position : str
            Position adjustment ("stack", "dodge", "fill")
        """
        if stat == "proportion":
            self.plot = self.plot + geom_bar(position=position, mapping=aes(y="..prop..", group=1))
        else:
            self.plot = self.plot + geom_bar(position=position)
        return self

    def add_errorbar(self, ymin: str, ymax: str, width: float = 0.2):
        """Add error bars using explicit min/max values.
        
        Parameters:
        -----------
        ymin : str
            Column name for lower bound
        ymax : str
            Column name for upper bound
        width : float
            Width of the error bars
        """
        self.plot = self.plot + geom_errorbar(
            mapping=aes(ymin=ymin, ymax=ymax),
            width=width
        )
        return self

    def add_hline(self, yintercept: float, linetype: str = "dashed", color: str = "black", alpha: float = 1.0):
        """Add horizontal reference line.
        
        Parameters:
        -----------
        yintercept : float
            Y-axis intercept value
        linetype : str
            Type of line ("solid", "dashed", "dotted", etc.)
        color : str
            Color of the line
        alpha : float
            Transparency of the line
        """
        self.plot = self.plot + geom_hline(
            yintercept=yintercept,
            linetype=linetype,
            color=color,
            alpha=alpha
        )
        return self

    def add_vline(self, xintercept: float, linetype: str = "dashed", color: str = "black", alpha: float = 1.0):
        """Add vertical reference line.
        
        Parameters:
        -----------
        xintercept : float
            X-axis intercept value
        linetype : str
            Type of line ("solid", "dashed", "dotted", etc.)
        color : str
            Color of the line
        alpha : float
            Transparency of the line
        """
        self.plot = self.plot + geom_vline(
            xintercept=xintercept,
            linetype=linetype,
            color=color,
            alpha=alpha
        )
        return self

    def add_text(self, label: str, x: float = None, y: float = None, 
                 ha: str = "center", va: str = "center", size: float = 11):
        """Add text annotation at specific coordinates.
        
        Parameters:
        -----------
        label : str
            Text to display
        x : float, optional
            X coordinate. If None, uses current x value
        y : float, optional
            Y coordinate. If None, uses current y value
        ha : str
            Horizontal alignment ("left", "center", "right")
        va : str
            Vertical alignment ("top", "center", "bottom")
        size : float
            Text size
        """
        if x is None or y is None:
            self.plot = self.plot + geom_text(
                mapping=aes(label=label),
                ha=ha, va=va, size=size
            )
        else:
            self.plot = self.plot + annotate(
                'text',
                x=x, y=y,
                label=label,
                ha=ha, va=va, size=size
            )
        return self

    def add_bar(self, stat: str = 'identity', width: float = 0.7, alpha: float = 0.7):
        """Add bar plot.
        
        Parameters:
        -----------
        stat : str
            Type of bar plot ('identity', 'count', 'sum')
        width : float
            Width of the bars
        alpha : float
            Transparency of the bars
        """
        self.plot = self.plot + geom_bar(stat=stat, width=width, alpha=alpha)
        return self

    def add_density_2d(self, alpha: float = 0.7):
        """Add 2D density estimation contours.
        
        Parameters:
        -----------
        alpha : float
            Transparency of the contours
        """
        self.plot = self.plot + geom_density_2d(alpha=alpha)
        return self

    def add_density_2d_filled(self, alpha: float = 0.7):
        """Add filled 2D density estimation contours.
        
        Parameters:
        -----------
        alpha : float
            Transparency of the filled contours
        """
        self.plot = self.plot + geom_density_2d_filled(alpha=alpha)
        return self

    def add_ribbon(self, ymin: str, ymax: str, alpha: float = 0.3):
        """Add a ribbon (filled area between two lines).
        
        Parameters:
        -----------
        ymin : str
            Column name for lower bound
        ymax : str
            Column name for upper bound
        alpha : float
            Transparency of the ribbon
        """
        self.plot = self.plot + geom_ribbon(
            mapping=aes(ymin=ymin, ymax=ymax),
            alpha=alpha
        )
        return self

    def add_smooth(self, method: str = "lm", se: bool = True, alpha: float = 0.2):
        """Add a smoothed conditional mean with confidence interval.
        
        Parameters:
        -----------
        method : str
            Smoothing method ("lm" for linear model, "loess" for local regression)
        se : bool
            Whether to display confidence interval
        alpha : float
            Transparency of the confidence interval
        """
        self.plot = self.plot + geom_smooth(
            method=method,
            se=se,
            alpha=alpha
        )
        return self

    def add_rug(self, sides: str = "b", alpha: float = 0.5, length: float = 0.03):
        """Add marginal rug plot (1-d visualization of point distribution).
        
        Parameters:
        -----------
        sides : str
            Which sides to draw the rug ("t" top, "b" bottom, "l" left, "r" right)
        alpha : float
            Transparency of the rug lines
        length : float
            Length of the rug lines as proportion of plot size
        """
        self.plot = self.plot + geom_rug(
            sides=sides,
            alpha=alpha,
            length=length
        )
        return self

    def add_quantiles(self, quantiles: list = [0.25, 0.5, 0.75], 
                     alpha: float = 0.5, color: str = "red"):
        """Add horizontal lines at specified quantiles.
        
        Parameters:
        -----------
        quantiles : list
            List of quantiles to show
        alpha : float
            Transparency of the lines
        color : str
            Color of the quantile lines
        """
        y_vals = self.data[self.y].quantile(quantiles)
        for q, y in zip(quantiles, y_vals):
            self.plot = self.plot + geom_hline(
                yintercept=y,
                alpha=alpha,
                color=color,
                linetype='dashed'
            )
        return self

    def add_step(self, direction: str = "hv"):
        """Add step plot.
        
        Parameters:
        -----------
        direction : str
            Direction of steps ("hv" horizontal then vertical, 
            "vh" vertical then horizontal)
        """
        self.plot = self.plot + geom_step(direction=direction)
        return self

    def add_hex(self, bins: int = 20):
        """Add hexagonal binning plot."""
        self.plot = self.plot + stat_bin_2d(bins=[bins, bins]) + scale_x_continuous() + scale_y_continuous()
        return self

    # Add statistical elements
    def add_correlation_text(self, method: str = 'pearson', format: str = '.3f'):
        """Add correlation coefficient text."""
        def calc_corr(data):
            if method == 'pearson':
                r, p = stats.pearsonr(data[self.x], data[self.y])
            else:  # spearman
                r, p = stats.spearmanr(data[self.x], data[self.y])
            return f'r = {r:{format}}\np = {p:{format}}'
        
        self.plot = self.plot + annotate('text', x=-np.inf, y=np.inf,
                                       label=calc_corr(self.data),
                                       ha='left', va='top')
        return self

    def add_regression_line(self, ci: bool = True, alpha: float = 0.2):
        """Add regression line with optional confidence interval."""
        self.plot = self.plot + geom_smooth(method='lm', se=ci, alpha=alpha)
        return self

    def add_test_pvalue(self, test: str = 't', paired: bool = False, 
                       ref_group: Optional[str] = None):
        """Add statistical test p-values.
        
        Parameters:
        -----------
        test : str
            Type of test to perform ('t', 'wilcox', 'anova', 'kruskal')
        paired : bool
            Whether to perform paired tests (only for t-test and wilcoxon)
        ref_group : str, optional
            Reference group for pairwise comparisons
        """
        if not self.color:
            warnings.warn("Statistical tests require groups specified by color")
            return self
            
        groups = self.data[self.color].unique()
        if len(groups) < 2:
            warnings.warn("At least two groups required for statistical testing")
            return self
            
        if test == 't':
            if len(groups) == 2:
                # t-test between two groups
                g1 = self.data[self.data[self.color] == groups[0]][self.y]
                g2 = self.data[self.data[self.color] == groups[1]][self.y]
                t, p = stats.ttest_rel(g1, g2) if paired else stats.ttest_ind(g1, g2)
                label = f't = {t:.2f}\np = {p:.3f}'
            else:
                # One-way ANOVA
                groups_data = [self.data[self.data[self.color] == g][self.y] for g in groups]
                f, p = stats.f_oneway(*groups_data)
                label = f'F = {f:.2f}\np = {p:.3f}'
        
        elif test == 'wilcox':
            if len(groups) == 2:
                # Wilcoxon test between two groups
                g1 = self.data[self.data[self.color] == groups[0]][self.y]
                g2 = self.data[self.data[self.color] == groups[1]][self.y]
                stat, p = stats.wilcoxon(g1, g2) if paired else stats.mannwhitneyu(g1, g2)
                label = f'W = {stat:.2f}\np = {p:.3f}'
            else:
                # Kruskal-Wallis H-test
                groups_data = [self.data[self.data[self.color] == g][self.y] for g in groups]
                h, p = stats.kruskal(*groups_data)
                label = f'H = {h:.2f}\np = {p:.3f}'
        
        # Add the test results to the plot
        self.plot = self.plot + annotate('text', x=-np.inf, y=np.inf,
                                       label=label, ha='left', va='top')
        return self

    # Remove elements
    def remove_grid(self):
        """Remove grid lines."""
        self.plot = self.plot + theme(panel_grid=element_blank())
        return self

    def remove_legend(self):
        """Remove legend."""
        self.plot = self.plot + theme(legend_position='none')
        return self

    def remove_x_axis(self):
        """Remove x-axis completely."""
        self.plot = self.plot + theme(axis_text_x=element_blank(),
                                    axis_ticks_x=element_blank(),
                                    axis_title_x=element_blank())
        return self

    def remove_y_axis(self):
        """Remove y-axis completely."""
        self.plot = self.plot + theme(axis_text_y=element_blank(),
                                    axis_ticks_y=element_blank(),
                                    axis_title_y=element_blank())
        return self

    # Adjust elements
    def adjust_axis_limits(self, xlim: tuple = None, ylim: tuple = None):
        """Adjust axis limits."""
        if xlim:
            self.plot = self.plot + xlim(xlim)
        if ylim:
            self.plot = self.plot + ylim(ylim)
        return self

    def adjust_colors(self, palette: Union[str, list, dict]):
        """Adjust color scheme.
        
        Parameters:
        -----------
        palette : str, list, or dict
            Color palette to use. If str, can be:
            - Sequential: 'Blues', 'Reds', etc.
            - Qualitative: 'Set2', 'Set3', etc.
            - Viridis: 'viridis', 'plasma', 'inferno', 'magma'
        """
        if isinstance(palette, str):
            if palette.lower() in ['viridis', 'plasma', 'inferno', 'magma']:
                self.plot = self.plot + scale_color_gradientn(colors=plt.get_cmap(palette)(np.linspace(0, 1, 256)))
            elif palette in ['Set2', 'Set3']:
                # Use custom color sets for qualitative data
                set2_colors = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffd92f', '#e5c494', '#b3b3b3']
                set3_colors = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69', '#fccde5']
                colors = set2_colors if palette == 'Set2' else set3_colors
                self.plot = self.plot + scale_color_manual(values=colors[:len(self.data[self.color].unique())])
            else:
                self.plot = self.plot + scale_color_brewer(palette=palette)
        elif isinstance(palette, dict):
            self.plot = self.plot + scale_color_manual(values=palette)
        else:
            self.plot = self.plot + scale_color_manual(values=palette)
        return self

    def adjust_theme(self, style: str = 'minimal', base_size: float = 11):
        """Adjust plot theme."""
        themes = {
            'minimal': theme_minimal,
            'classic': theme_classic,
            'bw': theme_bw,
            'dark': theme_dark
        }
        self.plot = self.plot + themes[style](base_size=base_size)
        return self

    def adjust_text_size(self, title: float = 12, axis: float = 10, 
                        legend: float = 9):
        """Adjust text sizes."""
        self.plot = self.plot + theme(
            title=element_text(size=title),
            axis_text=element_text(size=axis),
            legend_text=element_text(size=legend)
        )
        return self

    def adjust_labels(self, title: str = None, x: str = None, y: str = None):
        """Adjust plot labels."""
        self.plot = self.plot + labs(title=title, x=x, y=y)
        return self

    def adjust_axis_text_angle(self, axis: str = "x", angle: float = 45, ha: str = "right"):
        """Adjust the angle of axis text.
        
        Parameters:
        -----------
        axis : str
            Which axis to adjust ("x" or "y")
        angle : float
            Rotation angle in degrees
        ha : str
            Horizontal alignment after rotation
        """
        if axis.lower() == "x":
            self.plot = self.plot + theme(
                axis_text_x=element_text(angle=angle, ha=ha)
            )
        else:
            self.plot = self.plot + theme(
                axis_text_y=element_text(angle=angle, ha=ha)
            )
        return self

    def adjust_legend_position(self, position: str = "right"):
        """Adjust the position of the legend.
        
        Parameters:
        -----------
        position : str
            Legend position ("none", "right", "left", "top", "bottom")
        """
        self.plot = self.plot + theme(
            legend_position=position
        )
        return self

    def scale_y_log10(self):
        """Use log10 scale for y-axis."""
        self.plot = self.plot + scale_y_continuous(trans='log10')
        return self

    def scale_x_log10(self):
        """Use log10 scale for x-axis."""
        self.plot = self.plot + scale_x_continuous(trans='log10')
        return self

    def scale_y_sqrt(self):
        """Use square root scale for y-axis."""
        self.plot = self.plot + scale_y_continuous(trans='sqrt')
        return self

    def scale_x_sqrt(self):
        """Use square root scale for x-axis."""
        self.plot = self.plot + scale_x_continuous(trans='sqrt')
        return self

    def scale_y_reverse(self):
        """Reverse the y-axis."""
        self.plot = self.plot + scale_y_continuous(trans='reverse')
        return self

    def scale_x_reverse(self):
        """Reverse the x-axis."""
        self.plot = self.plot + scale_x_continuous(trans='reverse')
        return self

    def scale_y_limits(self, limits: tuple):
        """Set y-axis limits.
        
        Parameters:
        -----------
        limits : tuple
            (min, max) values for y-axis
        """
        self.plot = self.plot + scale_y_continuous(limits=limits)
        return self

    def scale_x_limits(self, limits: tuple):
        """Set x-axis limits.
        
        Parameters:
        -----------
        limits : tuple
            (min, max) values for x-axis
        """
        self.plot = self.plot + scale_x_continuous(limits=limits)
        return self

    def scale_color_gradient(self, low: str = "blue", high: str = "red"):
        """Create a continuous color gradient.
        
        Parameters:
        -----------
        low : str
            Color for low values
        high : str
            Color for high values
        """
        self.plot = self.plot + scale_color_gradient(low=low, high=high)
        return self

    def scale_color_gradient2(self, low: str = "blue", mid: str = "white", high: str = "red", midpoint: float = 0):
        """Create a diverging color gradient.
        
        Parameters:
        -----------
        low : str
            Color for low values
        mid : str
            Color for middle values
        high : str
            Color for high values
        midpoint : float
            Value at which the midpoint color should be mapped
        """
        self.plot = self.plot + scale_color_gradient2(
            low=low, mid=mid, high=high, midpoint=midpoint
        )
        return self

    def coord_flip(self):
        """Flip the x and y coordinates."""
        self.plot = self.plot + coord_flip()
        return self

    def expand_limits(self, x: tuple = None, y: tuple = None):
        """Expand the plot limits without changing the data.
        
        Parameters:
        -----------
        x : tuple
            (min, max) for x-axis
        y : tuple
            (min, max) for y-axis
        """
        if x is not None:
            self.plot = self.plot + expand_limits(x=x)
        if y is not None:
            self.plot = self.plot + expand_limits(y=y)
        return self

    # Layout modifications
    def split_by(self, variable: str, ncol: int = None):
        """Split plot by variable (faceting)."""
        if ncol:
            self.plot = self.plot + facet_wrap(f'~{variable}', ncol=ncol)
        else:
            self.plot = self.plot + facet_wrap(f'~{variable}')
        return self

    def split_by_grid(self, row: str, col: str):
        """Split plot by two variables in a grid."""
        self.plot = self.plot + facet_grid(f'{row}~{col}')
        return self

    def save(self, filename: str):
        """Save the plot to a file."""
        self.plot.save(filename)

    def show(self):
        """Display the plot and return the plot object."""
        return self.plot

# Helper function to create TidyPlot object
def tidyplot(data: pd.DataFrame, x: str, y: str = None, color: Optional[str] = None) -> TidyPlot:
    """Create a new TidyPlot object."""
    return TidyPlot(data, x, y, color)

# Add method to DataFrame
pd.DataFrame.tidyplot = lambda self, x, y=None, color=None: tidyplot(self, x, y, color)

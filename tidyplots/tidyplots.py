"""A Python library for creating publication-ready plots with a fluent, chainable interface."""

import pandas as pd
import numpy as np
from plotnine import *
from plotnine.stats import stat_bin_2d
from typing import Optional, List, Union, Dict, Any

class TidyPrism:
    """Prism-style themes and statistical annotations."""
    
    @staticmethod
    def theme_prism(base_size: float = 11, base_family: str = "Arial") -> theme:
        """Create a Prism-style theme.
        
        Parameters:
        -----------
        base_size : float
            Base font size
        base_family : str
            Base font family
        """
        return (theme_minimal(base_size=base_size, base_family=base_family) +
                theme(
                    axis_line=element_line(color="black", size=1),
                    axis_text=element_text(color="black"),
                    panel_grid_major=element_blank(),
                    panel_grid_minor=element_blank(),
                    panel_border=element_blank(),
                    panel_background=element_blank(),
                    legend_background=element_blank(),
                    legend_key=element_blank()
                ))
    
    @staticmethod
    def add_pvalue(p: float, x1: float, x2: float, y: float, height: float = 0.02,
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
            'stars' for asterisks, 'numeric' for number
        """
        if format == "stars":
            if p < 0.001:
                label = "***"
            elif p < 0.01:
                label = "**"
            elif p < 0.05:
                label = "*"
            else:
                label = "ns"
        else:
            label = f"p = {p:.3f}"
            
        elements = [
            geom_segment(aes(x=x1, xend=x1, y=y, yend=y+height)),
            geom_segment(aes(x=x2, xend=x2, y=y, yend=y+height)),
            geom_segment(aes(x=x1, xend=x2, y=y+height, yend=y+height)),
            annotate("text", x=(x1+x2)/2, y=y+height*1.2, label=label)
        ]
        return elements

class TidySci:
    """Scientific journal color palettes."""
    
    # Color palettes from scientific journals
    PALETTES: Dict[str, List[str]] = {
        'npg': ['#E64B35', '#4DBBD5', '#00A087', '#3C5488', '#F39B7F', '#8491B4'],
        'aaas': ['#3B4992', '#EE0000', '#008B45', '#631879', '#008280', '#BB0021'],
        'nejm': ['#BC3C29', '#0072B5', '#E18727', '#20854E', '#7876B1', '#6F99AD'],
        'lancet': ['#00468B', '#ED0000', '#42B540', '#0099B4', '#925E9F', '#FDAF91'],
        'jama': ['#374E55', '#DF8F44', '#00A1D5', '#B24745', '#79AF97', '#6A6599'],
        'd3': ['#1F77B4', '#FF7F0E', '#2CA02C', '#D62728', '#9467BD', '#8C564B'],
        'material': ['#F44336', '#2196F3', '#4CAF50', '#FFEB3B', '#9C27B0', '#FF9800'],
        'igv': ['#5050FF', '#CE3D32', '#749B58', '#F0E685', '#466983', '#BA6338']
    }
    
    @classmethod
    def get_palette(cls, name: str = 'npg') -> List[str]:
        """Get a scientific color palette.
        
        Parameters:
        -----------
        name : str
            Name of the palette
        """
        if name not in cls.PALETTES:
            raise ValueError(f"Unknown palette '{name}'. Available palettes: {list(cls.PALETTES.keys())}")
        return cls.PALETTES[name]

@pd.api.extensions.register_dataframe_accessor("tidyplot")
class TidyPlot:
    """A fluent interface for creating publication-ready plots."""
    
    def __init__(self, pandas_obj):
        """Initialize TidyPlot with a pandas DataFrame."""
        self._obj = pandas_obj
        self.plot = None
        self.prism = TidyPrism()
        self.sci = TidySci()
        
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
                    TidyPrism.theme_prism())  # Use Prism theme by default
        
        # Apply NPG colors by default
        colors = TidySci.get_palette('npg')
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
        self.plot = self.plot + stat_bin_2d(bins=bins, geom='tile')
        return self
    
    def add_errorbar(self, ymin: str, ymax: str, alpha: float = 0.8, width: float = 0.2):
        """Add error bars with explicit min/max values."""
        self.plot = self.plot + geom_errorbar(
            aes(ymin=ymin, ymax=ymax), 
            alpha=alpha, 
            width=width
        )
        return self
    
    def add_data_points_jitter(self, width: float = 0.2, height: float = 0, alpha: float = 0.5):
        """Add jittered points to the plot."""
        self.plot = self.plot + geom_jitter(width=width, height=height, alpha=alpha)
        return self

    def add_mean_bar(self, alpha: float = 0.4, width: float = 0.7):
        """Add bars showing mean values."""
        self.plot = self.plot + stat_summary(fun_y=np.mean, geom='bar', alpha=alpha, width=width)
        return self

    def add_sem_errorbar(self, width: float = 0.2):
        """Add error bars showing standard error of the mean."""
        self.plot = self.plot + stat_summary(fun_data='mean_se', geom='errorbar', width=width)
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

    def adjust_labels(self, title: str = None, x: str = None, y: str = None):
        """Adjust plot labels."""
        self.plot = self.plot + labs(title=title, x=x, y=y)
        return self
    
    def adjust_colors(self, palette: str = 'npg'):
        """Change color palette using scientific journal styles.
        
        Parameters:
        -----------
        palette : str
            Name of the scientific color palette to use
        """
        colors = TidySci.get_palette(palette)
        if 'y' not in self.plot.mapping:
            self.plot = self.plot + scale_fill_manual(values=colors)
        else:
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

    def scale_x_log10(self):
        """Apply log10 scale to x-axis."""
        self.plot = self.plot + scale_x_log10()
        return self

    def scale_y_log10(self):
        """Apply log10 scale to y-axis."""
        self.plot = self.plot + scale_y_log10()
        return self
    
    def scale_color_gradient(self, low: str = 'lightblue', high: str = 'darkblue'):
        """Set continuous color gradient."""
        self.plot = self.plot + scale_color_gradient(low=low, high=high)
        return self
    
    def add_pvalue(self, p: float, x1: float, x2: float, y: float, height: float = 0.02,
                   format: str = "stars"):
        """Add p-value annotation with bracket."""
        elements = TidyPrism.add_pvalue(p, x1, x2, y, height, format)
        for element in elements:
            self.plot = self.plot + element
        return self
    
    def add_data_points(self, alpha: float = 0.3, width: float = 0.2):
        """Add jittered data points to categorical plots."""
        self.plot = self.plot + geom_jitter(alpha=alpha, width=width)
        return self
    
    def add_hex(self, bins: int = 20):
        """Add hexagonal binning."""
        self.plot = self.plot + geom_hex(bins=bins)
        return self
    
    def add_errorbar(self, ymin: pd.Series, ymax: pd.Series, width: float = 0.2):
        """Add error bars to the plot."""
        self.plot = self.plot + geom_errorbar(
            aes(ymin=ymin, ymax=ymax),
            width=width
        )
        return self
    
    def add_smooth(self, method: str = 'lm', se: bool = True):
        """Add a smoothed conditional mean."""
        self.plot = self.plot + stat_smooth(method=method, se=se)
        return self
    
    def add_correlation_text(self, x: float = None, y: float = None):
        """Add correlation coefficient to the plot."""
        if 'x' not in self.plot.mapping or 'y' not in self.plot.mapping:
            raise ValueError("Both x and y must be specified for correlation")
            
        x_data = self._obj[self.plot.mapping['x']]
        y_data = self._obj[self.plot.mapping['y']]
        
        corr = np.corrcoef(x_data, y_data)[0, 1]
        if x is None:
            x = x_data.mean()
        if y is None:
            y = y_data.max()
            
        self.plot = self.plot + annotate(
            'text',
            x=x, y=y,
            label=f'r = {corr:.2f}'
        )
        return self
    
    def add_density_2d(self, alpha: float = 0.6):
        """Add 2D density contours."""
        self.plot = self.plot + stat_density_2d(geom='polygon', alpha=alpha)
        return self
    
    def add_bar(self, alpha: float = 0.8):
        """Add bar plot."""
        self.plot = self.plot + geom_bar(stat='identity', alpha=alpha)
        return self
    
    def show(self):
        """Display the plot."""
        return self.plot
    
    def save(self, filename: str, **kwargs):
        """Save the plot to a file.
        
        Parameters:
        -----------
        filename : str
            Path to save the plot to
        **kwargs : dict
            Additional arguments to pass to ggsave
        """
        self.plot.save(filename, **kwargs)
        return self

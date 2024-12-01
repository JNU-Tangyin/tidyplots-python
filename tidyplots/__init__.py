"""
tidyplots is a Python library for creating publication-ready plots with a fluent, chainable interface.
"""

from .tidyplots import TidyPlot
from . import palettes
from . import themes

# Add tidyplot method to pandas DataFrame
import pandas as pd

@pd.api.extensions.register_dataframe_accessor("tidyplot")
class TidyPlotAccessor:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj
        self._plot = TidyPlot(pandas_obj)
        # Apply default theme
        self.prism = themes.TidyPrism()
        self._default_theme = self.prism.theme_prism()
        if hasattr(self._plot, 'plot') and self._plot.plot is not None:
            self._plot.plot = self._plot.plot + self._default_theme

    def __call__(self, x: str = None, y: str = None, 
                color: str = None, 
                fill: str = None,
                shape: str = None,
                size: str = None,
                linetype: str = None,
                split_by: str = None,
                **kwargs):
        if x is not None:
            plot = self._plot(x=x, y=y, color=color, fill=fill, shape=shape, 
                          size=size, linetype=linetype, split_by=split_by, **kwargs)
            # Apply default theme
            if hasattr(plot, 'plot') and plot.plot is not None:
                plot.plot = plot.plot + self._default_theme
            return plot
        return self._plot

    def __getattr__(self, name):
        """Forward attribute access to TidyPlot instance."""
        return getattr(self._plot, name)

# Create tidyplot function for direct import
def tidyplot(data):
    """Create a TidyPlot object from a pandas DataFrame.
    
    This function is provided for backward compatibility and direct usage.
    The recommended way is to use the DataFrame accessor: df.tidyplot()
    """
    plot = TidyPlot(data)
    # Apply default theme
    plot.prism = themes.TidyPrism()
    plot._default_theme = plot.prism.theme_prism()
    if hasattr(plot, 'plot') and plot.plot is not None:
        plot.plot = plot.plot + plot._default_theme
    return plot

__version__ = '0.1.0'
__all__ = ['TidyPlot', 'palettes', 'themes', 'tidyplot']

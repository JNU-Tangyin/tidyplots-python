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
        self._plot = None

    def __call__(self, x: str, y: str = None, 
                color: str = None, 
                fill: str = None,
                shape: str = None,
                size: str = None,
                linetype: str = None,
                split_by: str = None,
                **kwargs):
        plot = TidyPlot(self._obj)
        return plot(x=x, y=y, color=color, fill=fill, shape=shape, 
                   size=size, linetype=linetype, split_by=split_by, **kwargs)

__version__ = '0.1.0'
__all__ = ['TidyPlot', 'palettes', 'themes']

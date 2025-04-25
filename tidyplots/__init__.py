"""
TidyPlots: A Python library for creating beautiful and customizable plots.
"""

from .tidyplots import TidyPlot
from .plotnine import geom_pie, geom_rose

__version__ = '0.1.0'
__all__ = [
    'TidyPlot',
    'tidyplot',
    'geom_pie',
    'geom_rose'
]

# Create tidyplot function for direct import
def tidyplot(data):
    """Create a TidyPlot object from data."""
    return TidyPlot(data)

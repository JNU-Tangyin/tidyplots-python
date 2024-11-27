import pandas as pd
from tidyplot import TidyPlot

# Monkey patching
if not hasattr(pd.DataFrame, 'tidyplot'):
    pd.DataFrame.tidyplot = lambda self: TidyPlot(self)
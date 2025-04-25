import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

try:
    from tidyplots import TidyPlot
    print("Successfully imported tidyplots!")
except ImportError as e:
    print(f"Failed to import tidyplots: {e}")

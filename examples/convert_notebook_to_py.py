import nbformat
import re

def process_code_cell(cell_source, section_number=''):
    # Replace .show() with .save() with appropriate filename
    lines = cell_source.split('\n')
    processed_lines = []
    
    # Extract plot type from the code
    plot_type = None
    for pt in ['scatter', 'line', 'bar', 'box', 'violin', 'density', 'step', 'dot', 
              'mean_bar', 'count', 'histogram', 'area', 'pie', 'heatmap']:
        if f'add_{pt}' in cell_source:
            plot_type = pt
            break
    
    for line in lines:
        if '.show()' in line:
            # Try to extract title first
            title_match = re.search(r"title='([^']*)'", line)
            
            if title_match:
                # Use the title to generate filename
                title = title_match.group(1).lower()
                # Remove special characters and spaces
                title = re.sub(r'[^a-z0-9_]', '_', title)
                title = re.sub(r'_+', '_', title)  # Replace multiple underscores with single
                title = title.strip('_')  # Remove leading/trailing underscores
                filename = f"figures/{section_number}_{title}.png"
            else:
                # Use plot type if available, otherwise use a generic name
                if plot_type:
                    filename = f"figures/{section_number}_{plot_type}.png"
                else:
                    filename = f"figures/{section_number}_plot.png"
            
            # Replace .show() with .save()
            line = line.replace('.show()', f".save('{filename}')")
        processed_lines.append(line)
    return '\n'.join(processed_lines)

# Read the notebook
with open('seaborn_examples.ipynb', 'r') as f:
    nb = nbformat.read(f, as_version=4)

# Start with imports and setup
py_code = '''"""
Comprehensive test of ALL functions in TidyPlots API using seaborn datasets.
This script tests every single function documented in api.md.
"""
import pandas as pd
import seaborn as sns
import os
import numpy as np
import tidyplots  # Import the package which will monkey-patch pandas

# Create figures directory if it doesn't exist
os.makedirs("figures", exist_ok=True)

# Load all available seaborn datasets
iris = sns.load_dataset("iris")
tips = sns.load_dataset("tips")
titanic = sns.load_dataset("titanic")
planets = sns.load_dataset("planets")
diamonds = sns.load_dataset("diamonds")
flights = sns.load_dataset("flights")

'''

current_section = ''
for cell in nb.cells:
    if cell.cell_type == 'markdown':
        # Process section headers
        if cell.source.startswith('# '):
            header = cell.source.strip()
            # Extract section number if it exists
            section_match = re.match(r'#+ (\d+\.?\d*)', header)
            if section_match:
                current_section = section_match.group(1).rstrip('.')
            py_code += f"\n{header}\n"
    elif cell.cell_type == 'code':
        # Skip the pip install cell
        if 'pip install' in cell.source:
            continue
        # Skip the initial imports if we already have them
        if 'import pandas' in cell.source or 'import seaborn' in cell.source:
            continue
            
        # Process code cells
        if cell.source.strip():
            processed_code = process_code_cell(cell.source, current_section)
            py_code += f"\n{processed_code}\n"

# Add final message
py_code += '\nprint("\\nAll examples have been generated in the \'figures\' directory.")\n'

# Write the Python file
with open('seaborn_examples.py', 'w') as f:
    f.write(py_code)

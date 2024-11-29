import nbformat as nbf
import re

# Read the original Python script
with open('seaborn_examples.py', 'r') as f:
    py_script = f.read()

# Create a new notebook
nb = nbf.v4.new_notebook()

# Add title markdown cell
nb.cells.append(nbf.v4.new_markdown_cell("""# TidyPlots API Examples

Comprehensive test of ALL functions in TidyPlots API using seaborn datasets."""))

# Add pip install cell
nb.cells.append(nbf.v4.new_code_cell('pip install -e ../'))

# Function to process a code block
def process_code_block(code):
    # Replace .save() with .show(), removing any parameters
    code = re.sub(r"\.save\([^)]+\)", '.show()', code)
    return code

# Split the script into sections
sections = []
current_section = []
lines = py_script.split('\n')

for line in lines:
    if line.startswith('# ') or line.startswith('## '):
        if current_section:
            sections.append(current_section)
            current_section = []
    current_section.append(line)

if current_section:
    sections.append(current_section)

# Add the initial imports and setup
imports_code = '''import pandas as pd
import seaborn as sns
import numpy as np
import os
import tidyplots  # Import the package which will monkey-patch pandas

# Create figures directory if it doesn't exist
os.makedirs("figures", exist_ok=True)

# Load all available seaborn datasets
iris = sns.load_dataset("iris")
tips = sns.load_dataset("tips")
titanic = sns.load_dataset("titanic")
planets = sns.load_dataset("planets")
diamonds = sns.load_dataset("diamonds")
flights = sns.load_dataset("flights")'''

nb.cells.append(nbf.v4.new_code_cell(imports_code))

# Process each section
for section in sections:
    section_text = '\n'.join(section)
    
    # Skip the initial imports and setup sections
    if any(text in section_text for text in ['import ', 'Create figures', 'Load all available']):
        continue
    
    # Process section header
    header_line = section[0].strip()
    if header_line.startswith('# ') or header_line.startswith('## '):
        header_text = header_line.lstrip('#').strip()
        header_level = 1 if header_line.startswith('# ') else 2
        nb.cells.append(nbf.v4.new_markdown_cell(f"{'#' * header_level} {header_text}"))
    
    # Process code content
    code_lines = []
    for line in section[1:]:
        if line.strip() and not line.startswith('"""'):
            code_lines.append(line)
    
    if code_lines:
        code = '\n'.join(code_lines).strip()
        if code:
            code = process_code_block(code)
            nb.cells.append(nbf.v4.new_code_cell(code))

# Write the notebook
with open('seaborn_examples.ipynb', 'w') as f:
    nbf.write(nb, f)

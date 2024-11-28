"""
Color palettes for TidyPlots.

This module provides a collection of color palettes from:
1. Scientific journals and organizations (from ggsci)
2. Matplotlib colormaps
3. Custom palettes

Each palette is represented as a list of hex color codes.
"""

import matplotlib.pyplot as plt
import numpy as np

def _create_cmap_colors(cmap_name, n_colors=8):
    """Convert a matplotlib colormap to a list of hex colors."""
    cmap = plt.get_cmap(cmap_name)
    colors = cmap(np.linspace(0, 1, n_colors))
    return [plt.matplotlib.colors.rgb2hex(c) for c in colors]

# Scientific Journal and Organization Color Palettes (from ggsci)
PALETTES = {
    # NPG (Nature Publishing Group)
    'npg': ['#E64B35', '#4DBBD5', '#00A087', '#3C5488', '#F39B7F', '#8491B4', '#91D1C2', '#DC0000', '#7E6148', '#B09C85'],
    
    # AAAS (Science)
    'aaas': ['#3B4992', '#EE0000', '#008B45', '#631879', '#008280', '#BB0021', '#5F559B', '#A20056', '#808180', '#1B1919'],
    
    # NEJM (New England Journal of Medicine)
    'nejm': ['#BC3C29', '#0072B5', '#E18727', '#20854E', '#7876B1', '#6F99AD', '#FFDC91', '#EE4C97'],
    
    # Lancet
    'lancet': ['#00468B', '#ED0000', '#42B540', '#0099B4', '#925E9F', '#FDAF91', '#AD002A', '#ADB6B6'],
    
    # JAMA (Journal of the American Medical Association)
    'jama': ['#374E55', '#DF8F44', '#00A1D5', '#B24745', '#79AF97', '#6A6599', '#80796B'],
    
    # JCO (Journal of Clinical Oncology)
    'jco': ['#0073C2', '#EFC000', '#868686', '#CD534C', '#7AA6DC', '#003C67', '#8F7700', '#3B3B3B'],
    
    # UCSCGB (UCSC Genome Browser)
    'ucscgb': ['#FF0000', '#FF9900', '#00FF00', '#6600FF', '#0000FF', '#FFCC00', '#FF00CC', '#00FF00', '#FF6600'],
    
    # D3.js
    'd3': ['#1F77B4', '#FF7F0E', '#2CA02C', '#D62728', '#9467BD', '#8C564B', '#E377C2', '#7F7F7F', '#BCBD22', '#17BECF'],
    
    # Material Design
    'material': ['#2196F3', '#F44336', '#4CAF50', '#FFC107', '#9C27B0', '#FF9800', '#795548', '#607D8B'],
    
    # IGV (Integrative Genomics Viewer)
    'igv': ['#5050FF', '#CE3D32', '#749B58', '#F0B015', '#6783B0', '#B86A92', '#C1B02C', '#7F7F7F'],
    
    # Dark2 (ColorBrewer)
    'dark2': ['#1B9E77', '#D95F02', '#7570B3', '#E7298A', '#66A61E', '#E6AB02', '#A6761D', '#666666'],
    
    # Set1 (ColorBrewer)
    'set1': ['#E41A1C', '#377EB8', '#4DAF4A', '#984EA3', '#FF7F00', '#FFFF33', '#A65628', '#F781BF'],
    
    # Set2 (ColorBrewer)
    'set2': ['#66C2A5', '#FC8D62', '#8DA0CB', '#E78AC3', '#A6D854', '#FFD92F', '#E5C494', '#B3B3B3'],
    
    # Set3 (ColorBrewer)
    'set3': ['#8DD3C7', '#FFFFB3', '#BEBADA', '#FB8072', '#80B1D3', '#FDB462', '#B3DE69', '#FCCDE5'],
}

# Add Matplotlib Sequential Colormaps
SEQUENTIAL_CMAPS = [
    'viridis', 'plasma', 'inferno', 'magma', 'cividis',
    'Blues', 'Greens', 'Oranges', 'Reds', 'Purples',
    'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu',
]

# Add Matplotlib Diverging Colormaps
DIVERGING_CMAPS = [
    'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
    'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr',
]

# Add Matplotlib Qualitative Colormaps
QUALITATIVE_CMAPS = [
    'Pastel1', 'Pastel2', 'Paired', 'Accent',
    'tab10', 'tab20', 'tab20b', 'tab20c',
]

# Add all matplotlib colormaps to the PALETTES dictionary
for cmap_name in SEQUENTIAL_CMAPS + DIVERGING_CMAPS + QUALITATIVE_CMAPS:
    PALETTES[cmap_name] = _create_cmap_colors(cmap_name)

def get_palette(name, n_colors=None):
    """
    Get a color palette by name.
    
    Parameters
    ----------
    name : str
        Name of the palette
    n_colors : int, optional
        Number of colors to return. If None, returns the full palette.
        If n_colors is greater than the palette size, colors will be recycled.
    
    Returns
    -------
    list
        List of hex color codes
    
    Raises
    ------
    ValueError
        If the palette name is not found
    """
    if name not in PALETTES:
        raise ValueError(f"Unknown palette '{name}'. Available palettes: {sorted(PALETTES.keys())}")
    
    palette = PALETTES[name]
    if n_colors is None:
        return palette
    
    # If n_colors is specified, cycle through the palette
    return [palette[i % len(palette)] for i in range(n_colors)]

def list_palettes():
    """List all available palette names."""
    return sorted(PALETTES.keys())

def preview_palette(name, n_colors=None):
    """
    Preview a color palette by displaying colored rectangles.
    
    Parameters
    ----------
    name : str
        Name of the palette
    n_colors : int, optional
        Number of colors to display
    """
    colors = get_palette(name, n_colors)
    n = len(colors)
    
    fig, ax = plt.subplots(figsize=(n, 1))
    for i, color in enumerate(colors):
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color))
    
    ax.set_xlim(0, n)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"Palette: {name}")
    plt.show()

def preview_all_palettes(n_colors=8):
    """
    Preview all available palettes.
    
    Parameters
    ----------
    n_colors : int, optional
        Number of colors to display for each palette
    """
    names = list_palettes()
    n_palettes = len(names)
    
    fig, axes = plt.subplots(n_palettes, 1, figsize=(12, n_palettes * 0.5))
    fig.suptitle("Available Color Palettes")
    
    for ax, name in zip(axes, names):
        colors = get_palette(name, n_colors)
        for i, color in enumerate(colors):
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color))
        ax.set_xlim(0, n_colors)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_ylabel(name, rotation=0, ha='right', va='center')
    
    plt.tight_layout()
    plt.show()

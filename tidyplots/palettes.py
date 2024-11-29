"""
Color palettes for TidyPlots.

This module provides a collection of color palettes from:
1. Scientific journals and organizations (from ggsci)
2. Matplotlib colormaps
3. Custom palettes

Each palette is represented as a list of hex color codes.
"""

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from typing import List, Tuple, Optional, Union, Literal

def _hex_to_rgb(hex_color: str) -> Tuple[float, float, float]:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16)/255 for i in (0, 2, 4))

def _rgb_to_hex(rgb: Tuple[float, float, float]) -> str:
    """Convert RGB tuple to hex color."""
    return '#{:02x}{:02x}{:02x}'.format(
        int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)
    )

def _interpolate_colors(color1: str, color2: str, n: int) -> List[str]:
    """Interpolate between two colors to create a gradient."""
    rgb1 = _hex_to_rgb(color1)
    rgb2 = _hex_to_rgb(color2)
    
    r = np.linspace(rgb1[0], rgb2[0], n)
    g = np.linspace(rgb1[1], rgb2[1], n)
    b = np.linspace(rgb1[2], rgb2[2], n)
    
    return [_rgb_to_hex((r[i], g[i], b[i])) for i in range(n)]

def _create_sequential_gradient(color: str, n: int) -> List[str]:
    """Create a sequential gradient from white to a color."""
    white = '#FFFFFF'
    return _interpolate_colors(white, color, n)

def _create_diverging_gradient(color1: str, color2: str, n: int) -> List[str]:
    """Create a diverging gradient between two colors through white."""
    white = '#FFFFFF'
    n_half = n // 2
    n_odd = n % 2
    
    gradient1 = _interpolate_colors(color1, white, n_half + n_odd)
    gradient2 = _interpolate_colors(white, color2, n_half + 1)[1:]
    
    return gradient1 + gradient2

def _get_palette_type(name: str) -> Literal['sequential', 'diverging', 'qualitative']:
    """
    Determine the type of a palette.
    
    Parameters
    ----------
    name : str
        Name of the palette
        
    Returns
    -------
    str
        'sequential', 'diverging', or 'qualitative'
    """
    if name in SEQUENTIAL_CMAPS:
        return 'sequential'
    elif name in DIVERGING_CMAPS:
        return 'diverging'
    else:
        return 'qualitative'

def _discretize_continuous(name: str, n: int) -> List[str]:
    """Convert a continuous palette to discrete colors."""
    return _create_cmap_colors(name, n)

def _continuize_discrete(palette: List[str], n: int, palette_type: str) -> List[str]:
    """
    Convert a discrete palette to continuous colors.
    
    Parameters
    ----------
    palette : List[str]
        Input discrete palette
    n : int
        Number of colors to generate
    palette_type : str
        Type of palette ('sequential', 'diverging', or 'qualitative')
    
    Returns
    -------
    List[str]
        Continuous color palette
    """
    if palette_type == 'sequential':
        # 从白色到第一个颜色的渐变
        return _create_sequential_gradient(palette[0], n)
    elif palette_type == 'diverging':
        # 从第一个颜色通过白色到最后一个颜色的渐变
        return _create_diverging_gradient(palette[0], palette[-1], n)
    else:  # qualitative
        # 保持离散颜色或循环
        if n <= len(palette):
            return palette[:n]
        return [palette[i % len(palette)] for i in range(n)]

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
    
    # # Set1 (ColorBrewer)
    # 'Set1': ['#E41A1C', '#377EB8', '#4DAF4A', '#984EA3', '#FF7F00', '#FFFF33', '#A65628', '#F781BF'],
    
    # # Set2 (ColorBrewer)
    # 'Set2': ['#66C2A5', '#FC8D62', '#8DA0CB', '#E78AC3', '#A6D854', '#FFD92F', '#E5C494', '#B3B3B3'],
    
    # # Set3 (ColorBrewer)
    # 'Set3': ['#8DD3C7', '#FFFFB3', '#BEBADA', '#FB8072', '#80B1D3', '#FDB462', '#B3DE69', '#FCCDE5'],
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
    'Set1', 'Set2', 'Set3'
]

# Add all matplotlib colormaps to the PALETTES dictionary
for cmap_name in SEQUENTIAL_CMAPS + DIVERGING_CMAPS + QUALITATIVE_CMAPS:
    PALETTES[cmap_name] = _create_cmap_colors(cmap_name)

def get_palette(name: str, 
              n: int = 9,
              i: int = 0,
              type: Optional[Literal['sequential', 'diverging', 'qualitative']] = 'qualitative') -> List[str]:
    """
    Get a color palette by name with automatic conversion between discrete and continuous.
    
    Parameters
    ----------
    name : str
        Name of the palette
    n : int, default=9
        Number of colors to return:
        - For continuous palettes: divide continuous colors into n parts
        - For discrete palettes: return at most first n colors
    i : int, default=0
        For sequential: index of color to use
        For diverging: start color index
    type : {'sequential', 'diverging', 'qualitative'}, default='qualitative'
        Palette type:
        - 'sequential': Create gradient from white to deepest color i
        - 'diverging': Create gradient between colors i and j through white
        - 'qualitative': Keep discrete colors
    
    Returns
    -------
    list
        List of hex color codes
    """
    if name not in PALETTES:
        raise ValueError(f"Unknown palette '{name}'. Available palettes: {sorted(PALETTES.keys())}")
    
    palette = PALETTES[name].copy()
    
    # 检查索引是否有效
    if i >= len(palette):
        raise ValueError(f"Color index {i} out of range for palette with {len(palette)} colors")
    if j is not None and j >= len(palette):
        raise ValueError(f"Color index {j} out of range for palette with {len(palette)} colors")
    
    if type == 'sequential':
        # 从白色到第i个颜色的最深同类颜色
        return _create_sequential_gradient(palette[i], n)
        
    elif type == 'diverging':
        # 如果没有指定j，使用i+1（循环到开头）
        if j is None:
            j = (i + 1) % len(palette)
        return _create_diverging_gradient(palette[i], palette[j], n)
        
    else:  # qualitative
        # 返回最多前n个颜色
        if n <= len(palette):
            return palette[:n]
        # 如果需要更多颜色，循环使用
        return [palette[k % len(palette)] for k in range(n)]

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

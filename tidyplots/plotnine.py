"""
Plotnine-specific geoms and stats for TidyPlots.
"""

import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from plotnine.geoms.geom import geom
from plotnine.layer import Layers, layer
from plotnine.positions.position import position
from plotnine.themes.theme import theme
from plotnine.themes.elements import element_blank


class geom_pie(geom):
    """
    Create a pie chart using polar coordinates.
    
    Args:
        show_labels (bool): Whether to show labels
        label_type (str): Type of labels ('value', 'percent', 'both')
        label_radius (float): Position of labels as fraction of radius
        label_size (float): Font size for labels
        sort (bool): Whether to sort slices by value
        start_angle (float): Starting angle in degrees
        inner_radius (float): Inner radius for donut chart
        explode (list): List of offset values for each slice
        **kwargs: Additional arguments passed to geom
    """
    DEFAULT_AES = {'alpha': 1, 'color': None, 'fill': 'gray', 'size': 0.1}
    REQUIRED_AES = {'x', 'y'}
    DEFAULT_PARAMS = {
        'na_rm': False,
        'show_labels': True,
        'label_type': 'value',
        'label_radius': 0.7,
        'label_size': 8,
        'sort': False,
        'start_angle': 90,
        'inner_radius': 0.0,
        'explode': None,
        'stat': 'identity',
        'position': 'identity'
    }

    def setup_data(self, data):
        if self.params['sort']:
            data = data.sort_values('y', ascending=False)
        
        # Convert values to angles
        total = data['y'].sum()
        data['angle'] = data['y'] / total * 2 * np.pi
        data['cumsum'] = data['angle'].cumsum()
        data['percent'] = data['y'] / total * 100
        
        # Calculate start and end angles
        start_angle_rad = np.radians(self.params['start_angle'])
        data['start'] = data['cumsum'].shift(1, fill_value=0) - start_angle_rad
        data['end'] = data['cumsum'] - start_angle_rad
        
        return data

    @staticmethod
    def draw_group(data, panel_params, coord, ax, **params):
        # Create polar subplot
        if not isinstance(ax.axes, plt.matplotlib.projections.polar.PolarAxes):
            # Get the current figure
            fig = ax.figure
            # Clear the current axes
            fig.clear()
            # Create new polar axes
            ax = fig.add_subplot(111, projection='polar')
        
        # Extract parameters
        show_labels = params.get('show_labels', True)
        label_type = params.get('label_type', 'value')
        label_radius = params.get('label_radius', 0.7)
        label_size = params.get('label_size', 8)
        inner_radius = params.get('inner_radius', 0.0)
        
        # Get explode values if provided
        explode = params.get('explode')
        if explode is None:
            explode = [0] * len(data)
        elif len(explode) < len(data):
            explode = explode + [0] * (len(data) - len(explode))
        
        # Draw wedges
        for i, row in data.iterrows():
            # Calculate center offset for exploded wedges
            angle = (row['start'] + row['end']) / 2
            center = (
                explode[i] * np.cos(angle),
                explode[i] * np.sin(angle)
            )
            
            wedge = mpatches.Wedge(
                center, 1.0,
                np.degrees(row['start']), np.degrees(row['end']),
                width=1.0 - inner_radius,
                facecolor=row['fill'],
                edgecolor=row['color'] if row['color'] else 'white',
                linewidth=row['size'],
                alpha=row['alpha']
            )
            ax.add_patch(wedge)
            
            # Add labels if requested
            if show_labels:
                # Calculate label position with explode offset
                x = center[0] + label_radius * np.cos(angle)
                y = center[1] + label_radius * np.sin(angle)
                
                # Format label based on type
                if label_type == 'value':
                    label = f"{row['y']:.1f}"
                elif label_type == 'percent':
                    label = f"{row['percent']:.1f}%"
                else:  # 'both'
                    label = f"{row['y']:.1f}\n({row['percent']:.1f}%)"
                
                # Add text with white outline for better visibility
                text = ax.text(
                    x, y, label,
                    ha='center', va='center',
                    size=label_size,
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1)
                )
                
        # Set axis limits and aspect
        ax.set_xlim(-1.5, 1.5)  # Wider limits to accommodate exploded wedges
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        
        return ax


class geom_rose(geom):
    """
    Create a Nightingale Rose Chart (also known as a polar area diagram).
    
    Args:
        show_labels (bool): Whether to show labels
        label_type (str): Type of labels ('value', 'percent', 'both')
        label_radius (float): Position of labels as fraction of radius
        label_size (float): Font size for labels
        sort (bool): Whether to sort slices by value
        start_angle (float): Starting angle in degrees
        **kwargs: Additional arguments passed to geom
    """
    DEFAULT_AES = {'alpha': 1, 'color': None, 'fill': 'gray', 'size': 0.1}
    REQUIRED_AES = {'x', 'y'}
    DEFAULT_PARAMS = {
        'na_rm': False,
        'show_labels': True,
        'label_type': 'value',
        'label_radius': 0.7,
        'label_size': 8,
        'sort': False,
        'start_angle': 90,
        'stat': 'identity',
        'position': 'identity'
    }

    def setup_data(self, data):
        if self.params['sort']:
            data = data.sort_values('y', ascending=False)
        
        # Convert values to angles
        n = len(data)
        angle = 2 * np.pi / n
        data['angle'] = angle
        data['start'] = np.arange(n) * angle - np.radians(self.params['start_angle'])
        data['end'] = data['start'] + angle
        
        # Calculate percentages
        total = data['y'].sum()
        data['percent'] = data['y'] / total * 100
        
        return data

    @staticmethod
    def draw_group(data, panel_params, coord, ax, **params):
        # Create polar subplot
        if not isinstance(ax.axes, plt.matplotlib.projections.polar.PolarAxes):
            # Get the current figure
            fig = ax.figure
            # Clear the current axes
            fig.clear()
            # Create new polar axes
            ax = fig.add_subplot(111, projection='polar')
        
        # Extract parameters
        show_labels = params.get('show_labels', True)
        label_type = params.get('label_type', 'value')
        label_radius = params.get('label_radius', 0.7)
        label_size = params.get('label_size', 8)
        
        # Draw wedges
        for _, row in data.iterrows():
            # Calculate radius based on value
            radius = np.sqrt(row['y'])
            
            wedge = mpatches.Wedge(
                (0, 0), radius,
                np.degrees(row['start']), np.degrees(row['end']),
                facecolor=row['fill'],
                edgecolor=row['color'] if row['color'] else 'white',
                linewidth=row['size'],
                alpha=row['alpha']
            )
            ax.add_patch(wedge)
            
            # Add labels if requested
            if show_labels:
                # Calculate label position
                angle = (row['start'] + row['end']) / 2
                x = label_radius * radius * np.cos(angle)
                y = label_radius * radius * np.sin(angle)
                
                # Format label based on type
                if label_type == 'value':
                    label = f"{row['y']:.1f}"
                elif label_type == 'percent':
                    label = f"{row['percent']:.1f}%"
                else:  # 'both'
                    label = f"{row['y']:.1f}\n({row['percent']:.1f}%)"
                
                # Add text with white outline for better visibility
                text = ax.text(
                    x, y, label,
                    ha='center', va='center',
                    size=label_size,
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1)
                )
        
        # Draw grid lines (concentric circles)
        max_radius = np.sqrt(data['y'].max())
        for r in np.linspace(0, max_radius, 5)[1:]:
            circle = plt.Circle((0, 0), r, fill=False, linestyle='--', alpha=0.3)
            ax.add_patch(circle)
        
        # Set axis limits and aspect
        ax.set_xlim(-max_radius * 1.2, max_radius * 1.2)
        ax.set_ylim(-max_radius * 1.2, max_radius * 1.2)
        ax.set_aspect('equal')
        
        return ax

"""Themes and statistical annotations for TidyPlots."""

from plotnine import *
from typing import List, Any

class TidyPrism:
    """Prism-style themes and statistical annotations."""
    
    @staticmethod
    def theme_prism(base_size: float = 11, base_family: str = "Arial") -> theme:
        """Create a Prism-style theme.
        
        Parameters:
        -----------
        base_size : float
            Base font size
        base_family : str
            Base font family
            
        Returns:
        --------
        theme : plotnine.theme
            A Prism-style theme for plots
        """
        return (theme_minimal(base_size=base_size, base_family=base_family) +
                theme(
                    axis_line=element_line(color="black", size=1),
                    axis_text=element_text(color="black"),
                    panel_grid_major=element_blank(),
                    panel_grid_minor=element_blank(),
                    panel_border=element_blank(),
                    panel_background=element_blank(),
                    legend_background=element_blank(),
                    legend_key=element_blank()
                ))
    
    @staticmethod
    def add_pvalue(p: float, x1: float, x2: float, y: float, height: float = 0.02,
                  format: str = "stars") -> List[Any]:
        """Add p-value annotation with bracket.
        
        Parameters:
        -----------
        p : float
            P-value to display
        x1, x2 : float
            x-coordinates for bracket ends
        y : float
            y-coordinate for bracket
        height : float
            Height of the bracket
        format : str
            'stars' for asterisks, 'numeric' for number
            
        Returns:
        --------
        list
            List of plotnine elements for the annotation
        """
        if format == "stars":
            if p < 0.001:
                label = "***"
            elif p < 0.01:
                label = "**"
            elif p < 0.05:
                label = "*"
            else:
                label = "ns"
        else:
            label = f"p = {p:.3f}"
            
        elements = [
            geom_segment(aes(x=x1, xend=x1, y=y, yend=y+height)),
            geom_segment(aes(x=x2, xend=x2, y=y, yend=y+height)),
            geom_segment(aes(x=x1, xend=x2, y=y+height, yend=y+height)),
            annotate("text", x=(x1+x2)/2, y=y+height*1.2, label=label)
        ]
        return elements

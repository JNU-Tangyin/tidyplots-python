"""Themes and statistical annotations for TidyPlots."""

from plotnine import *
from typing import List, Any

class TidyPrism:
    """Prism-style themes and statistical annotations."""
    
    @staticmethod
    def theme_prism(base_size: float = 11, base_family: str = "Arial",
                   base_line_size: float = 0.5, base_rect_size: float = 0.5,
                   axis_text_angle: float = 0) -> theme:
        """Create a basic Prism-style theme.
        
        Parameters:
        -----------
        base_size : float
            Base font size
        base_family : str
            Base font family
        base_line_size : float
            Base line size for axis lines
        base_rect_size : float
            Base rectangle size for borders
        axis_text_angle : float
            Angle for axis text rotation
            
        Returns:
        --------
        theme : plotnine.theme
            A Prism-style theme for plots
        """
        return (theme_minimal(base_size=base_size, base_family=base_family) +
                theme(
                    axis_line=element_line(color="black", size=base_line_size),
                    axis_text=element_text(color="black", angle=axis_text_angle),
                    panel_grid_major=element_blank(),
                    panel_grid_minor=element_blank(),
                    panel_border=element_blank(),
                    panel_background=element_blank(),
                    legend_background=element_blank(),
                    legend_key=element_blank()
                ))
    
    @staticmethod
    def theme_prism_min(base_size: float = 11, base_family: str = "Arial") -> theme:
        """Create a minimal Prism-style theme."""
        return (TidyPrism.theme_prism(base_size=base_size, base_family=base_family) +
                theme(
                    axis_line=element_blank(),
                    axis_ticks=element_blank()
                ))

    @staticmethod
    def theme_prism_npg(base_size: float = 11, base_family: str = "Arial") -> theme:
        """Nature Publishing Group style theme."""
        return (TidyPrism.theme_prism(base_size=base_size, base_family=base_family) +
                theme(
                    axis_line=element_line(color="#000000"),
                    text=element_text(color="#000000")
                ))

    @staticmethod
    def theme_prism_aaas(base_size: float = 11, base_family: str = "Arial") -> theme:
        """Science/AAAS style theme."""
        return (TidyPrism.theme_prism(base_size=base_size, base_family=base_family) +
                theme(
                    axis_line=element_line(color="#000000"),
                    text=element_text(color="#000000")
                ))

    @staticmethod
    def theme_prism_nejm(base_size: float = 11, base_family: str = "Arial") -> theme:
        """New England Journal of Medicine style theme."""
        return (TidyPrism.theme_prism(base_size=base_size, base_family=base_family) +
                theme(
                    axis_line=element_line(color="#000000"),
                    text=element_text(color="#000000")
                ))

    @staticmethod
    def theme_prism_lancet(base_size: float = 11, base_family: str = "Arial") -> theme:
        """The Lancet style theme."""
        return (TidyPrism.theme_prism(base_size=base_size, base_family=base_family) +
                theme(
                    axis_line=element_line(color="#000000"),
                    text=element_text(color="#000000")
                ))

    @staticmethod
    def theme_prism_jama(base_size: float = 11, base_family: str = "Arial") -> theme:
        """Journal of the American Medical Association style theme."""
        return (TidyPrism.theme_prism(base_size=base_size, base_family=base_family) +
                theme(
                    axis_line=element_line(color="#000000"),
                    text=element_text(color="#000000")
                ))

    @staticmethod
    def theme_prism_dark(base_size: float = 11, base_family: str = "Arial") -> theme:
        """Dark Prism theme."""
        return (TidyPrism.theme_prism(base_size=base_size, base_family=base_family) +
                theme(
                    axis_line=element_line(color="#FFFFFF"),
                    axis_text=element_text(color="#FFFFFF"),
                    text=element_text(color="#FFFFFF"),
                    panel_background=element_rect(fill="#000000"),
                    plot_background=element_rect(fill="#000000")
                ))

    @staticmethod
    def theme_prism_light(base_size: float = 11, base_family: str = "Arial") -> theme:
        """Light Prism theme."""
        return (TidyPrism.theme_prism(base_size=base_size, base_family=base_family) +
                theme(
                    axis_line=element_line(color="#000000", size=0.5),
                    panel_background=element_rect(fill="#FFFFFF")
                ))

    @staticmethod
    def theme_jnu(base_size: float = 11, base_family: str = "Arial", **kw) -> theme:
        """Jinan University (JNU) style theme.
        
        A professional theme designed for Jinan University publications,
        featuring the university's signature colors and clean, academic style.
        
        Parameters:
        -----------
        base_size : float
            Base font size
        base_family : str
            Base font family
        **kw : dict
            Additional keyword arguments to override default theme settings
            
        Returns:
        --------
        theme : plotnine.theme
            A JNU-style theme for plots
        """
        # JNU colors
        jnu_red = "#A71930"     # 暨南大学红
        jnu_gold = "#D4AF37"    # 金色点缀
        jnu_grey = "#4A4A4A"    # 专业灰色

        base_theme = theme(
            # 图形大小
            figure_size=[6, 5],
            
            # 坐标轴文本
            axis_text=element_text(
                size=9, 
                family="Arial",
                color="black", 
                face="bold"
            ),
            
            # 坐标轴标题
            axis_title_x=element_text(
                size=12,
                family="Arial",
                color="black", 
                face="bold"
            ),
            axis_title_y=element_text(
                size=12,
                family="Arial",
                color="black", 
                face="bold"
            ),
            
            # 图标题
            plot_title=element_text(
                margin={'b': 1, 'r': 0, 'units': 'pt'},
                size=16,
                family="Arial",
                color="black",
                hjust=0.5
            ),
            
            # 背景设置
            panel_background=element_blank(),
            panel_grid_major=element_line(
                size=0.3, 
                alpha=0.0,
                color='black'
            ),
            panel_grid_minor=element_line(
                size=0.3, 
                alpha=0.0,
                color='black'
            ),
            panel_border=element_rect(
                color='black', 
                size=1
            ),
            
            # 图例设置
            legend_title=element_text(
                size=6,
                alpha=0
            ),
            legend_text=element_text(
                size=8
            ),
            legend_background=element_rect(
                size=1,
                alpha=0.0
            ),
            legend_position="right",
            legend_key_size=8
        )
        
        # 合并用户自定义设置
        if kw:
            base_theme = base_theme + theme(**kw)
            
        return base_theme
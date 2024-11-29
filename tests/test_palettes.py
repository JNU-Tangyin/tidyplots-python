"""Test color palettes functionality."""

import pytest
import matplotlib.pyplot as plt
from tidyplots.palettes import (
    get_palette, 
    list_palettes, 
    preview_palette,
    preview_all_palettes,
    PALETTES,
    _hex_to_rgb,
    _rgb_to_hex,
    _create_sequential_gradient,
    _create_diverging_gradient,
    _get_palette_type
)

def test_get_palette():
    """Test get_palette function."""
    # Test getting a known palette
    npg_palette = get_palette('npg')
    assert isinstance(npg_palette, list)
    assert len(npg_palette) > 0
    assert all(isinstance(color, str) for color in npg_palette)
    assert all(color.startswith('#') for color in npg_palette)

    # Test getting n colors from a palette
    n_colors = 5
    colors = get_palette('npg', n_colors)
    assert len(colors) == n_colors

    # Test cycling colors when n_colors > palette length
    long_colors = get_palette('npg', 20)
    assert len(long_colors) == 20

    # Test invalid palette name
    with pytest.raises(ValueError):
        get_palette('invalid_palette')

def test_list_palettes():
    """Test list_palettes function."""
    palettes = list_palettes()
    assert isinstance(palettes, list)
    assert len(palettes) > 0
    assert 'npg' in palettes
    assert all(isinstance(name, str) for name in palettes)

def test_preview_functions():
    """Test preview functions."""
    # Test that preview functions don't raise errors
    preview_palette('npg', 5)
    plt.close()

    preview_all_palettes(5)
    plt.close()

def test_color_conversions():
    """Test color conversion functions."""
    # Test hex to rgb and back
    hex_color = '#FF0000'
    rgb = _hex_to_rgb(hex_color)
    assert rgb == (1.0, 0.0, 0.0)
    assert _rgb_to_hex(rgb) == hex_color.lower()

def test_gradient_generation():
    """Test gradient generation functions."""
    # Test sequential gradient
    seq_gradient = _create_sequential_gradient('#FF0000', 5)
    assert len(seq_gradient) == 5
    assert seq_gradient[0] == '#ffffff'  # Start with white
    assert seq_gradient[-1].lower() == '#ff0000'  # End with target color
    
    # Test diverging gradient
    div_gradient = _create_diverging_gradient('#FF0000', '#0000FF', 5)
    assert len(div_gradient) == 5
    assert div_gradient[0].lower() == '#ff0000'  # Start color
    assert div_gradient[2].lower() == '#ffffff'  # Middle white
    assert div_gradient[-1].lower() == '#0000ff'  # End color

def test_palette_type_detection():
    """Test palette type detection."""
    # Test sequential colormap
    assert _get_palette_type('Blues') == 'sequential'
    
    # Test diverging colormap
    assert _get_palette_type('RdBu') == 'diverging'
    
    # Test qualitative palette
    assert _get_palette_type('npg') == 'qualitative'
    assert _get_palette_type('Set1') == 'qualitative'

def test_palette_behavior():
    """Test palette behavior for different types."""
    # 测试默认行为
    npg = get_palette('npg')  # 默认type='qualitative', n=9
    assert len(npg) == 9
    assert all(c.startswith('#') for c in npg)
    
    # 测试离散调色板的n参数
    npg_5 = get_palette('npg', n=5)  # 返回前5个颜色
    assert len(npg_5) == 5
    assert npg_5 == PALETTES['npg'][:5]
    
    npg_15 = get_palette('npg', n=15)  # 循环使用颜色
    assert len(npg_15) == 15
    assert npg_15[:len(PALETTES['npg'])] == PALETTES['npg']
    assert npg_15[len(PALETTES['npg']):] == PALETTES['npg'][:5]  # 循环使用前5个颜色
    
    # 测试sequential类型
    seq = get_palette('npg', n=5, type='sequential')  # 默认i=0
    assert len(seq) == 5
    assert seq[0] == '#ffffff'  # 开始是白色
    
    seq_2 = get_palette('npg', n=5, type='sequential', i=1)  # 使用第二个颜色
    assert seq_2[0] == '#ffffff'
    assert seq_2[-1] != seq[-1]  # 不同的目标颜色
    
    # 测试diverging类型
    div = get_palette('npg', n=5, type='diverging')  # 默认i=0, j=1
    assert len(div) == 5
    assert div[len(div)//2] == '#ffffff'  # 中间是白色
    
    div_2 = get_palette('npg', n=5, type='diverging', i=0, j=2)  # 指定两端颜色
    assert len(div_2) == 5
    assert div_2[len(div_2)//2] == '#ffffff'
    assert div_2[-1] != div[-1]  # 不同的结束颜色
    
    # 测试循环索引
    div_cycle = get_palette('npg', n=5, type='diverging', i=len(PALETTES['npg'])-1)  # i是最后一个，j应该循环到第一个
    assert len(div_cycle) == 5
    assert div_cycle[len(div_cycle)//2] == '#ffffff'
    
    # 测试错误处理
    with pytest.raises(ValueError):
        get_palette('npg', i=100)  # 索引超出范围
    
    with pytest.raises(ValueError):
        get_palette('npg', j=100)  # 索引超出范围

if __name__ == '__main__':
    print("Testing get_palette...")
    test_get_palette()
    
    print("\nTesting list_palettes...")
    test_list_palettes()
    
    print("\nTesting preview functions...")
    test_preview_functions()
    
    print("\nTesting color conversions...")
    test_color_conversions()
    
    print("\nTesting gradient generation...")
    test_gradient_generation()
    
    print("\nTesting palette type detection...")
    test_palette_type_detection()
    
    print("\nTesting palette behavior...")
    test_palette_behavior()
    
    print("\nAll tests passed!")
    
    # Preview all palettes with a smaller number of colors
    print("\nPreviewing all palettes...")
    preview_all_palettes(n_colors=5)

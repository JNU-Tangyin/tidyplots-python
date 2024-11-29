"""
Tests for tidyplots package.
"""
import numpy as np
import pandas as pd
import pytest
from tidyplots import tidyplot

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    np.random.seed(42)
    n = 100
    tidyplot.FIGURE_DIR = 'figures/'
    data = pd.DataFrame({
        'x': np.random.normal(0, 1, n),
        'y': np.random.normal(0, 1, n),
        'group': np.random.choice(['A', 'B'], n),
        'value': np.random.uniform(0, 10, n)
    })
    return data

def test_basic_plot(sample_data):
    """Test basic plot creation."""
    plot = tidyplot(sample_data, 'x', 'y')
    assert plot is not None
    
def test_scatter_plot(sample_data):
    """Test scatter plot creation."""
    plot = tidyplot(sample_data, 'x', 'y').add_scatter()
    assert plot is not None

def test_line_plot(sample_data):
    """Test line plot creation."""
    plot = tidyplot(sample_data, 'x', 'y').add_line()
    assert plot is not None

def test_boxplot(sample_data):
    """Test box plot creation."""
    plot = tidyplot(sample_data, 'group', 'value').add_boxplot()
    assert plot is not None

def test_violin_plot(sample_data):
    """Test violin plot creation."""
    plot = tidyplot(sample_data, 'group', 'value').add_violin()
    assert plot is not None

def test_density_plot(sample_data):
    """Test density plot creation."""
    plot = tidyplot(sample_data, 'x').add_density()
    assert plot is not None

def test_color_mapping(sample_data):
    """Test color mapping."""
    plot = tidyplot(sample_data, 'x', 'y', color='group').add_scatter()
    assert plot is not None

def test_labels(sample_data):
    """Test label customization."""
    plot = (tidyplot(sample_data, 'x', 'y')
            .adjust_labels(title='Test Plot', x='X Label', y='Y Label'))
    assert plot is not None

def test_scale_transformations(sample_data):
    """Test scale transformations."""
    plot = (tidyplot(sample_data, 'x', 'y')
            .scale_x_log10()
            .scale_y_log10())
    assert plot is not None

def test_error_bars(sample_data):
    """Test error bar addition."""
    plot = (tidyplot(sample_data, 'group', 'value')
            .add_mean_bar()
            .add_sem_errorbar())
    assert plot is not None

def test_statistical_elements(sample_data):
    """Test statistical elements."""
    plot = (tidyplot(sample_data, 'x', 'y')
            .add_correlation_text())
    assert plot is not None

def test_appearance_customization(sample_data):
    """Test appearance customization."""
    plot = (tidyplot(sample_data, 'x', 'y')
            .adjust_colors('Set1')
            .adjust_legend_position('right'))
    assert plot is not None

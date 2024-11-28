import pandas as pd
import numpy as np
from scipy import stats
from scipy.ndimage import gaussian_filter1d
import tidyplot  # This adds the .tidyplot() method to pd.DataFrame

# Set random seed for reproducibility
np.random.seed(42)

# Create various test datasets
def create_test_data():
    # Basic statistical test data
    stats_data = pd.DataFrame({
        'group': np.repeat(['Control', 'Treatment A', 'Treatment B'], 20),
        'value': np.concatenate([
            np.random.normal(10, 2, 20),  # Control group
            np.random.normal(12, 2, 20),  # Treatment A
            np.random.normal(11, 2, 20)   # Treatment B
        ]),
        'error': np.random.uniform(0.5, 1.5, 60)
    })
    stats_data['value_min'] = stats_data['value'] - stats_data['error']
    stats_data['value_max'] = stats_data['value'] + stats_data['error']

    # Time series data with confidence intervals
    x = np.linspace(0, 10, 100)
    y = 3 * np.sin(x) + np.random.normal(0, 0.5, 100)
    time_data = pd.DataFrame({
        'x': x.astype(float),
        'y': y.astype(float),
        'y_smooth': gaussian_filter1d(y, sigma=2).astype(float),
        'y_lower': (y - 1).astype(float),
        'y_upper': (y + 1).astype(float)
    })

    # 2D density data
    n_points = 1000
    x = np.random.multivariate_normal([0, 0], [[1, .5], [.5, 1]], n_points)
    density_data = pd.DataFrame({
        'x': x[:, 0].astype(float),
        'y': x[:, 1].astype(float),
        'density': np.random.uniform(0, 1, n_points).astype(float),  # Continuous color value
        'category': np.repeat(['A', 'B'], n_points//2)  # Discrete color value
    })

    # Count data
    count_data = pd.DataFrame({
        'category': np.random.choice(['Cat', 'Dog', 'Bird', 'Fish'], 100),
        'size': np.random.choice(['Small', 'Medium', 'Large'], 100)
    })

    return stats_data, time_data, density_data, count_data

def test_basic_plots():
    """Test basic statistical plots with error bars."""
    stats_data, _, _, _ = create_test_data()
    
    print("Creating statistical test plot...")
    (stats_data.tidyplot(x='group', y='value', color='group')
        .add_boxplot()
        .add_data_points_jitter()
        .add_errorbar(ymin='value_min', ymax='value_max')
        .adjust_colors('Set2')
        .adjust_labels(title='Statistical Test Example', x='Group', y='Value')
        .add_test_pvalue(test='t')
        .add_hline(yintercept=11, linetype='dashed', color='red', alpha=0.5)
        .show()
    ).save('test_stats.png')

def test_time_series():
    """Test time series plots with ribbons and smoothing."""
    _, time_data, _, _ = create_test_data()
    
    print("Creating time series plot...")
    (time_data.tidyplot(x='x', y='y')
        .add_line(alpha=0.3)
        .add_ribbon(ymin='y_lower', ymax='y_upper')
        .add_smooth(method='loess', se=True)
        .adjust_colors('viridis')
        .adjust_labels(title='Time Series with Confidence Interval', 
                      x='Time', y='Value')
        .show()
    ).save('test_timeseries.png')

def test_density_plots():
    """Test 2D density plots and hex bins."""
    _, _, density_data, _ = create_test_data()
    
    print("Creating 2D density plot...")
    (density_data.tidyplot(x='x', y='y', color='density')  # Use continuous color
        .add_scatter(alpha=0.3)
        .add_density_2d()
        .add_rug()
        .scale_color_gradient2(low='blue', mid='white', high='red')
        .adjust_labels(title='2D Density Plot', x='X', y='Y')
        .show()
    ).save('test_density.png')

    print("Creating hex bin plot...")
    (density_data.tidyplot(x='x', y='y')
        .add_hex(bins=20)
        .scale_color_gradient(low='lightblue', high='darkblue')
        .adjust_labels(title='Hexagonal Binning', x='X', y='Y')
        .show()
    ).save('test_hex.png')

def test_count_plots():
    """Test count plots with proportions."""
    _, _, _, count_data = create_test_data()
    
    print("Creating count plot...")
    (count_data.tidyplot(x='category', y=None, color='size')
        .add_count(stat='proportion', position='dodge')
        .adjust_colors('Set3')
        .adjust_labels(title='Pet Distribution by Size', x='Pet Type', y='Proportion')
        .adjust_axis_text_angle(angle=45)
        .add_text(label='n=100', x=0, y=1)
        .show()
    ).save('test_count.png')

def test_advanced_features():
    """Test advanced features like step plots and quantiles."""
    _, time_data, _, _ = create_test_data()
    
    print("Creating advanced features plot...")
    (time_data.tidyplot(x='x', y='y_smooth')
        .add_step()
        .add_quantiles([0.25, 0.5, 0.75])
        .adjust_labels(title='Step Plot with Quantiles', 
                      x='Time', y='Value')
        .show()
    ).save('test_advanced.png')

if __name__ == '__main__':
    print("Running tidyplot test suite...")
    test_basic_plots()
    test_time_series()
    test_density_plots()
    test_count_plots()
    test_advanced_features()
    print("\nTest plots have been saved as:")
    print("- test_stats.png (boxplot with error bars)")
    print("- test_timeseries.png (time series with ribbon)")
    print("- test_density.png (2D density plot)")
    print("- test_hex.png (hexagonal binning)")
    print("- test_count.png (count plot)")
    print("- test_advanced.png (step plot with quantiles)")

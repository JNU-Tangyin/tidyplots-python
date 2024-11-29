import pandas as pd
import numpy as np
from tidyplots.themes import TidyPrism
from plotnine import *

# 创建示例数据
np.random.seed(42)
n = 100
data = pd.DataFrame({
    'x': np.random.normal(0, 1, n),
    'y': np.random.normal(0, 1, n),
    'group': np.random.choice(['A', 'B', 'C'], n)
})

# 创建基础图形
p = (ggplot(data, aes('x', 'y', color='group'))
     + geom_point()
     + labs(title='JNU Theme Test',
            x='X Axis',
            y='Y Axis'))

# 应用 JNU 主题
p_jnu = p + TidyPrism.theme_jnu()

# 保存图形
p_jnu.save('test_jnu_theme.png', dpi=300)

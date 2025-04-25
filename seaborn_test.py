import pandas as pd
import numpy as np
import seaborn as sns

print("Successfully imported pandas, numpy, and seaborn!")

# Load a sample dataset
iris = sns.load_dataset("iris")
print("Iris dataset loaded, first 5 rows:")
print(iris.head())

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='tidyplots-python',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.0.0',
        'plotnine>=0.10.0',
        'numpy>=1.18.0',
        'scipy>=1.4.0',
        'scikit-misc>=0.1.4',
        'statsmodels>=0.13.0'
    ],
    description='A Python implementation of R\'s tidyplots for creating publication-ready plots',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Tangyin',
    author_email='tangyin@jnu.edu.cn',
    url='https://github.com/JNU-Tangyin/tidyplots-python',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.8',
    keywords='data visualization, plotting, statistics, ggplot, tidyverse',
    project_urls={
        'Bug Reports': 'https://github.com/JNU-Tangyin/tidyplots-python/issues',
        'Source': 'https://github.com/JNU-Tangyin/tidyplots-python',
        'Documentation': 'https://github.com/JNU-Tangyin/tidyplots-python#readme',
    },
)

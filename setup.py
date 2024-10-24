from setuptools import setup, find_packages

setup(
    name="city_walker",  # Your package name
    version="0.1.0",  # Initial version
    author="Jacob Walters",
    author_email="prog-city-walker@jacobwalte.rs",
    description="A tool for tracking city street walks and generating optimal routes",
    long_description=open("README.md").read(),  # Ensure README.md exists
    long_description_content_type="text/markdown",  # If you're using Markdown for README
    url="https://github.com/jacobjwalters/city-walker",  # Optional, if you have a repo
    packages=find_packages(),  # Automatically find and include all packages in the directory
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Define minimum Python version
    install_requires=[  # List of dependencies, matching your requirements.txt
        "gpxpy",
        "osmnx",
        "shapely",
        "geopandas",
        "rtree"
    ],
    entry_points={  # Optionally add CLI entry points
        'console_scripts': [
            'city-walker=city_walker.main:main',
        ],
    },
    include_package_data=True,  # Ensures non-Python files (e.g., data files) are included
)


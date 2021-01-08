import setuptools

setuptools.setup(
    name="pull_fb",
    version="0.0.1",
    author="Hamish Gibbs",
    author_email="Hamish.Gibbs@lshtm.ac.uk",
    description="CLI for downloading data from Facebook data for good.",
    url="https://github.com/hamishgibbs/pull_facebook_data_for_good",
    packages=setuptools.find_packages(),
    install_requires=[
        "Click",
        "requests",
        "pandas",
        "progress"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points="""
        [console_scripts]
        pull_fb=pull_fb.pull_fb:cli
    """,
)

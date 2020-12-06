import setuptools

setuptools.setup(
    name="pull_fb",
    version="0.0.1",
    author="Hamish Gibbs",
    author_email="Hamish.Gibbs@lshtm.ac.uk",
    description="CLI for downloading data from FB data for good.",
    url="https://github.com/hamishgibbs/pull_facebook_data_for_good",
    py_modules=['pull_fb', 'utils', 'url', 'driver', 'credentials', 'clean_up'],
    install_requires=[
        'Click',
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points='''
        [console_scripts]
        pull_fb=pull_fb:cli
    ''',
)

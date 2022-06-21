from setuptools import setup

setup(
    name="reddit_downloader",
    version="0.0.2",
    description="download reddit data",
    maintainer="Bartosz Włodarczyk",
    maintainer_email="s25762@pjwstk.edu.pl",
    packages=["reddit_downloader"],
    install_requires=["requests"],
    classifiers=[],
    include_package_data = True,
    package_data={"reddit_downloader":["./reddit-downloader/*"]}
)

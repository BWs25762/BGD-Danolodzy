from setuptools import setup

setup(
    name="reddit-downloader",
    version="0.0.1",
    description="download reddit data",
    maintainer="Bartosz Włodarczyk",
    maintainer_email="s25762@pjwstk.edu.pl",
    packages=["reddit-downloader"],
    install_requires=["requests"],
    classifiers=[],
    include_package_data = True,
    package_data={"reddit-downloader":["./reddit-downloader/*"]}
)

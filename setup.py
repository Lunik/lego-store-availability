import setuptools

setuptools.setup(
    name="lego-store-availability",
    install_requires=[
        "beautifulsoup4",
        "httpx",
        "tenacity",
    ],
    extras_require={
        "dev": [
            "black",
            "pylint",
            "pytest",
        ],
    },
)
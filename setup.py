import setuptools

setuptools.setup(
    name="lego-store-availability",
    install_requires=[
        "beautifulsoup4",
        "requests",
        "requests-cache",
        "PyYAML"
    ],
    extras_require = {
        'cache_s3':  ["boto3"]
    }
)
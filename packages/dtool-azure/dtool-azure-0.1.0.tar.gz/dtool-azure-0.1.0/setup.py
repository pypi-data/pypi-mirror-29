from setuptools import setup

url = "https://github.com/jic-dtool/dtool-azure"
version = "0.1.0"
readme = open('README.rst').read()

setup(
    name="dtool-azure",
    packages=["dtool_azure"],
    version=version,
    description="Add Azure dataset support to dtool",
    long_description=readme,
    include_package_data=True,
    author="Matthew Hartley",
    author_email="Matthew.Hartley@jic.ac.uk",
    url=url,
    install_requires=[
        "dtoolcore>=3.0",
        "azure-storage"
    ],
    entry_points={
        "dtool.storage_brokers": [
            "AzureStorageBroker=dtool_azure.storagebroker:AzureStorageBroker",
        ],
    },
    download_url="{}/tarball/{}".format(url, version),
    license="MIT"
)

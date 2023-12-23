from setuptools import setup, find_packages

setup(
    name="rdaensemble",
    version="1.0.5",
    description="Redistricting ensembles",
    url="https://github.com/rdatools/rdaensemble",
    author="alecramsay",
    author_email="a73cram5ay@gmail.com",
    license="MIT",
    packages=[
        "rdaensemble",
        "rdaensemble.recom",
        "rdaensemble.rmfrsp",
        "rdaensemble.rmfrst",
        "rdaensemble.smc",
        "rdaensemble.ust",
    ],
    install_requires=["rdabase", "rdascore"],
    zip_safe=False,
)

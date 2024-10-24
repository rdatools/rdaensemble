from setuptools import setup, find_packages

# from Cython.Build import cythonize

# python setup.py build_ext --inplace

cython_files = [
    "scripts/score_fast.pyx",
    # Add more .py or .pyx files as needed
]

setup(
    name="rdaensemble",
    version="2.0.0",
    description="Redistricting ensembles",
    url="https://github.com/rdatools/rdaensemble",
    author="alecramsay",
    author_email="a73cram5ay@gmail.com",
    license="MIT",
    packages=[
        "rdaensemble",
        "rdaensemble.general",
        "rdaensemble.mcmc",
        "rdaensemble.rmfrsp",
        "rdaensemble.rmfrst",
        "rdaensemble.smc",
        "rdaensemble.ust",
    ],
    # ext_modules=cythonize(cython_files, compiler_directives={"language_level": "3"}),
    install_requires=["rdabase", "rdascore", "rdadccvt", "gerrychain", "cython"],
    zip_safe=False,
)

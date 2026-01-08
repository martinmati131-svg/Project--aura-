from setuptools import setup, find_packages

setup(
    name="aura-intelligence",
    version="1.0.0",
    description="The S2R Sentinel Brain for Isaac Sim Robotics",
    author="Aura Intelligence",
    # This automatically finds the 'aura' folder with the __init__.py
    packages=find_packages(), 
    install_requires=[
        "numpy",
        # Note: 'pxr-usd' and 'omni' are usually provided by Isaac Sim
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Robotics",
    ],
)

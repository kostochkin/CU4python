from setuptools import setup, find_packages

setup(
    name='CU4lib',
    version=0.1,
    author='Konstantin Gorshkov',
    author_email='k.n.gorshkov@gmail.com',
    project_urls={
        "Documentation": "https://github.com/kostochkin/cu4python",
        "Bug Tracker": "https://github.com/kostochkin/cu4python/issues",
        "Source Code": "https://github.com/kostochkin/cu4python",
    },
    packages=find_packages(include=["CU4lib", "CU4lib.*"]),
    platforms='All',
    python_requires='>=2.7',
    license='MIT',
    description='A Python library for Control Unit 4 by Scontel',
#    long_description='',
#    long_description_content_type='text/markdown',
    install_requires=[],
    extras_require={
    },
#    test_suite='',
    classifiers=[
    ]
)

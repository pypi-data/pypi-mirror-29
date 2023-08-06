from setuptools import find_packages, setup

setup(
    name="htmlfetcher",
    version="0.0.6",
    description="No pain HTML fetching library.",
    author="Jiuli Gao",
    author_email="gaojiuli@gmail.com",
    url='https://github.com/gaojiuli/htmlfetcher',
    py_modules=['htmlfetcher'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'selenium'
    ],
    include_package_data=True,
    zip_safe=False,
)

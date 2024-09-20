from setuptools import setup, find_packages

setup(
    name='py1p',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/alexzunega/py1p',
    license='MIT',
    author='Alex Zunega',
    author_email='alex@zunega.com',
    description='A Python package for integrating with 1Password.',
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.12'
)

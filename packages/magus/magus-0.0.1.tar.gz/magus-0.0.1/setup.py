from setuptools import setup


def readme():
    with open("README.rst") as f:
        return f.read()


exec(open('magus/version.py', 'r').read())


setup(name='magus',
      version=__version__,
      description="Utilities for code inspection and transformation",
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3 :: Only'
      ],
      author='Alex Carney',
      author_email="alcarneyme@gmail.com",
      license='MIT',
      packages=['magus'],
      setup_requires=['pytest-runner'],
      test_suite='tests',
      tests_require=['pytest'],
      python_requires='>=3.0',
      include_package_data=True,
      zip_safe=False)

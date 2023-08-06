from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='excel_to_json',
      version='0.1',
      description='excel to json',
      long_description=readme(),
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing',
      ],
      keywords='excel to json',
      url='http://github.com/wang37921/excel_to_json',
      author='Wang Cong',
      author_email='wang37921@163.com',
      license='MIT',
      packages=['excel_to_json'],
      install_requires=[
          'openpyxl',
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      entry_points={
          'console_scripts': ['excel-to-json=excel_to_json.command_line:excel_to_json'],
      },
      include_package_data=True,
      zip_safe=False)
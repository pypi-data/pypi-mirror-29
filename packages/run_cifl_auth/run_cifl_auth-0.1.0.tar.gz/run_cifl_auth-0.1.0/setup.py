import setuptools

setuptools.setup(name='run_cifl_auth',
      version='0.1.0',
      description='Authentication module for Google APIs',
      long_description='',
      classifiers=[
      ],
      keywords='',
      url='https://github.com/coding-is-for-losers/singer-taps-and-targets-v1.1/tree/master/run_cifl_auth',
      author='CIFL',
      author_email='',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=[
          'cifl-auth-wrapper',
      ],
      entry_points='''
          [console_scripts]
          run-cifl-auth=run_cifl_auth:main
      ''',
      include_package_data=True,
      zip_safe=False)

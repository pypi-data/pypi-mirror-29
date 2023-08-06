import setuptools

setuptools.setup(name='cifl_target_gsheets',
      version='0.1.0',
      description='Singer.oi CIFL Target for Google Sheets',
      long_description='',
      classifiers=[
      ],
      keywords='',
      url='',
      author='CIFL',
      author_email='',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=[
          'cifl-google-wrapper',
      ],
      entry_points='''
          [console_scripts]
          cifl-target-gsheets=cifl_target_gsheets:main
      ''',
      include_package_data=True,
      zip_safe=False)

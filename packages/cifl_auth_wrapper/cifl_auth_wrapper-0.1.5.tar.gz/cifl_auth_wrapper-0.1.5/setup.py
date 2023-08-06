import setuptools

setuptools.setup(name='cifl_auth_wrapper',
      version='0.1.5',
      description='A wrapper for CIFL taps and targets',
      long_description='',
      classifiers=[
      ],
      keywords='',
      url='https://github.com/coding-is-for-losers/singer-taps-and-targets-v1.1/tree/master/cifl_google_wrapper',
      author='CIFL',
      author_email='',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=[
          'google-auth-oauthlib',
          'oauth2client',
          'apiclient',
          'singer-python',
      ],
      include_package_data=True,
      zip_safe=False)
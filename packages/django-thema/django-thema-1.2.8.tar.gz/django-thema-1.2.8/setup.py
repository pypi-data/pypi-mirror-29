from setuptools import setup, find_packages

setup(
  name='django-thema',
  packages=find_packages(exclude=['test_project']),
  include_package_data=True,
  package_data={},
  version='1.2.8',
  description='Application that provides EDItEUR Thema categories, '
              'and translations for the headers.',
  long_description=open('README.rst', 'rt').read(),
  license='BSD License 2.0',
  author='Saxo Publish',
  author_email='publish@saxo.com',
  url='https://saxo.githost.io/publish/django-thema',
  keywords=['django', 'thema', 'EDItEUR'],
  zip_safe=False,
  install_requires=[
      'django',
      'mock',
      'polib',
      'xlrd',
  ],
  classifiers=[
    'Framework :: Django',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3'
  ],
)

from setuptools import setup, find_packages

setup(name='SiLens',
      version='0.1',
      description='First version of Machine Learning Interpretation tool by SIngulariti',
      url='http://github.com/singularitiai/SiLens/archive/v0.1.tar.gz',
      author='Kanishka Sharma',
      author_email='kanishka.sharma@singulariti.ai',
      license='BSD',
      packages= ['SiLens'],
      install_requires=[
          'lime',
          'numpy',
          'pandas',
          'scipy',
          'scikit-learn>=0.18',
          'scikit-image>=0.12'
      ],
      include_package_data=True,
      zip_safe=False)

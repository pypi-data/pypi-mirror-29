from setuptools import setup, find_packages

setup(name='dxl-pygate',
      version='0.12.2',
      description='A simplified python interface for Gate.',
      url='https://github.com/Hong-Xiang/pygate',
      author='Hong Xiang',
      author_email='hx.hongxiang@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['fs', 'click', 'pyyaml',
                        'rx', 'jinja2', 'dxl-dxpy>=0.5',
                        'dxl-fs', 'dxl-cluster'],
      entry_points='''
            [console_scripts]
            pygate=pygate.cli:cli
      ''',
      include_package_data=True,
      zip_safe=False)

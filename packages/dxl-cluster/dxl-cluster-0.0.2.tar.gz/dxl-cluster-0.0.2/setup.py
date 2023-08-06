from setuptools import setup, find_packages
setup(name='dxl-cluster',
      version='0.0.2',
      description='Cluster utility library.',
      url='https://github.com/Hong-Xiang/dxcluster',
      author='Hong Xiang',
      author_email='hx.hongxiang@gmail.com',
      license='MIT',
      packages=['dxl.cluster', 'dxl.cluster.backend'],
      package_dir={'': 'src/python'},
      install_requires=[
          'click',
          'rx',
      ],
      scripts=[],
      zip_safe=False)

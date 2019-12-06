from setuptools import setup, find_packages

setup(name='foundations-auth-proxy',
      version='0.0.1',
      description='Foundations Authentication Proxy',
      packages=find_packages(exclude=('tests', 'docs')),
      install_requires=['Flask-Cors==3.0.6', 'python-dotenv==0.10.3', 'PyYAML==5.1.2'],
      zip_safe=False)
from setuptools import setup
setup(name='my-test-hello-library',
      version='0.1',
      description='sum two numbers',
      url='https://github.com/username/repo',
      author='Sebastian Garcia Valencia',
      author_email='sebasgverde@gmail.com',
      license='MIT',
      packages=['my-test-hello-library'],
      install_requires=['numpy>=1.11',
                        'matplotlib>=1.5'])
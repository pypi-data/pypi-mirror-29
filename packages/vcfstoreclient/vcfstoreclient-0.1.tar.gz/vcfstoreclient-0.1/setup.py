from setuptools import setup

setup(name='vcfstoreclient',
      version='0.1',
      description='Client for AWS vcfstore',
      url='https://genomeinfo.github.io/',
      author='Conrad Leonard',
      author_email='conrad.leonard@qimrberghofer.edu.au',
      license='MIT',
      install_requires=[
          'aws_requests_auth',
          'boto3',
          'filecache',
          'python_jsonschema_objects',
          'requests'
          ],
      scripts=['bin/vcfstoreclient'],
      packages=['vcfstoreclient'],
      zip_safe=False)

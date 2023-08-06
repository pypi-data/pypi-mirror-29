from distutils.core import setup
setup(
    name='sqs_event',
    version='0.0.1',
    packages=[
        'sqs_event',
    ],
    install_requires=['ergaleia'],
    description='Simple AWS SQS-based event queue handler',
    long_description="""
Documentation
-------------
    You can see the project and documentation at the `GitHub repo <https://github.com/robertchase/sqs_event>`_
    """,
    author='Bob Chase',
    url='https://github.com/robertchase/sqs_event',
    license='MIT',
)

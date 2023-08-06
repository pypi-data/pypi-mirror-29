from distutils.core import setup

setup(
    name='YellowPushSMS',
    version='0.5',
    packages=['yellowPushSMS'],
    url='https://github.com/IdentidadIoT/YellowPushSMSPythonPackage',
    #download_url='https://github.com/jalejocs/identidad_sms_api_python/tarball/0.11',
    license='',
    author='YellowPushSMS',
    author_email='alejo@4dev.co',
    description='Python Helper Library makes it easy to interact with the YellowPushSMS API from your Python application',
    keywords = ['SMS', 'BulkSMS'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Telephony",
    ],
    install_requires=[
          'requests>=2.0.1', 'requests_toolbelt',
      ],
    long_description="""\
       Python YellowPushSMS Helper Library
       ----------------------------
       DESCRIPTION
       The YellowPushSMS REST API simplifies the process of send sms using the YellowPushSMS REST API"""
)

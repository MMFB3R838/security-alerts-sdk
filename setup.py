"""
Setup script for Security Alerts SDK
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8') if (this_directory / "README.md").exists() else ""

setup(
    name='security-alerts-sdk',
    version='1.0.0',
    author='David Chen',
    author_email='david.chen.sec@protonmail.com',
    description='Monitor your digital assets for security leaks and breaches',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/davidchen-sec/security-alerts-sdk',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Security',
        'Topic :: System :: Monitoring',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[
        'requests>=2.31.0',
    ],
    keywords='security monitoring breach detection haveibeenpwned github secrets',
    project_urls={
        'Bug Reports': 'https://github.com/davidchen-sec/security-alerts-sdk/issues',
        'Source': 'https://github.com/davidchen-sec/security-alerts-sdk',
        'Documentation': 'https://github.com/davidchen-sec/security-alerts-sdk#readme',
    },
)

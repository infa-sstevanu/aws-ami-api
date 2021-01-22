from setuptools import find_packages, setup

setup(
    name='ami_api',
    version='0.11.2',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'boto3',
        'flask',
        'gunicorn',
        'prometheus_client'
    ],
)

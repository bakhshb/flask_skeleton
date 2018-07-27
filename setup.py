from setuptools import find_packages, setup

setup(
    name='flask_skeleton',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask','flask_admin','flask-security', 'flask-sqlalchemy','oauth2client','flask_assets', 'sqlalchemy_continuum','pyYaml','Flask-SSLify'
    ],
)

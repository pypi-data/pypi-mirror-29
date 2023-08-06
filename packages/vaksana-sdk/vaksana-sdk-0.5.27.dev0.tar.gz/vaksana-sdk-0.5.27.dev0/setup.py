from setuptools import setup, find_packages

#http://python-packaging.readthedocs.io/en/latest/minimal.html
#https://stackoverflow.com/questions/45207128/failed-to-upload-packages-to-pypi-410-gone

setup(
	name='vaksana-sdk',
	version='0.5.27dev',
        packages = find_packages(),
        package_data={'': ['market_proto/*.proto', '*.py']},
        include_package_data=True,

        setup_requires=[ "setuptools_git >= 0.3", ],

        install_requires=[
            'pycrypto',
            'pykafka',
            'pyopenssl',
            'vaksana-proto',
            'grpcio',
            'grpcio-tools',
            ],

        author = "Pankaj Garg",
        author_email = "garg.pankaj83@gmail.com",
        description = "SDK to connect to Vaksana Marketplace",
        long_description=open('README.md').read(),
        license = "PSF",
        keywords = "Vaksana",
        url = "http://vaksana.com/sdk#python"
)

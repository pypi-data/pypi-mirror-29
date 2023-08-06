from setuptools import find_packages, setup

setup(
name = 'transfersh',
version = '0.1',
packages = find_packages(),
package_dir = {
'transfersh': 'transfersh'
},
author = 'Ammad Khalid',
author_email = 'Ammadkhalid12@gmail.com',
install_requires = ['requests'],
url = 'https://github.com/Ammadkhalid/transfersh'
)

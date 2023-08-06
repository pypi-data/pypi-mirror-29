from setuptools import setup, find_packages

# We cannot declare __init__.py files in our package because they conflict
# with Ansible's. This disables setuptools package detection. Specify all
# files to be included in the package here.
py_files = [
    "ansible/module_utils/dotdiff"
]

setup(
    name='ansible-dotdiff',
    version=open('VERSION', 'r').read(),
    description='Nested structure diff library with dot-path notation for Ansible',
    long_description=open('README.rst', 'r').read(),
    author='Timo Beckers',
    author_email='timo.beckers@klarrio.com',
    url='https://github.com/Klarrio/ansible-dotdiff',
    py_modules=py_files,
    install_requires = [
        'ansible>=2.1.0'
    ],
)

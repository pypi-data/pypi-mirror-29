import re
from setuptools import setup

def get_latest_version(changelog):
    """Retrieve latest version of package from changelog file."""
    # Match strings like "### [1.2.3] - 2017-02-02"
    regex = r"^##\s*\[(\d+.\d+.\d+)\]\s*-\s*\d{4}-\d{2}-\d{2}$"
    with open(changelog, "r") as changelog:
        content = changelog.read()
    return re.search(regex, content, re.MULTILINE).group(1)

setup(
    name='sphinxcontrib-cloudformationyaml',
    url='https://github.com/monk-ee/sphinxcontrib-cloudformationyaml',
    author='Lyndon Swan',
    author_email='magic.monkee.magic@gmail.com',
    license='MIT',
    description='Sphinx extension to generate docs from cloudformation descriptions and comments',
    platforms='any',
    version=get_latest_version('CHANGELOG'),
    packages=['sphinxcontrib.cloudformationyaml'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Topic :: Documentation'
    ],
    install_requires=[
        'Sphinx',
        'ruamel.yaml'
    ],
    test_suite='tests.test_cloudformationyaml.TestCloudformationYAML',
    tests_require=[
        'sphinx-testing'
    ],
)

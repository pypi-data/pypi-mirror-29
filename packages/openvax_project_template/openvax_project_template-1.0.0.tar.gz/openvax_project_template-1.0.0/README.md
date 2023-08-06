<a href="https://travis-ci.org/openvax/openvax_project_template">
    <img src="https://travis-ci.org/openvax/openvax_project_template.svg?branch=master" alt="Build Status" />
</a>
<a href="https://coveralls.io/github/openvax/openvax_project_template?branch=master">
    <img src="https://coveralls.io/repos/openvax/openvax_project_template/badge.svg?branch=master&service=github" alt="Coverage Status" />
</a>
<a href="https://pypi.python.org/pypi/openvax_project_template/">
    <img src="https://img.shields.io/pypi/v/openvax_project_template.svg?maxAge=1000" alt="PyPI" />
</a>

# openvax-project-template

Template for a new OpenVax Python project

## README

Every README file should contain the following badges:

* Travis build status
* Coverage
* Current library version on PyPI


## Travis configuration

Every travis build should, in addition to a project's unit test, also run the [openvax-integration-tests](https://github.com/openvax/openvax-integration-tests).

## Deploying to PyPI

Projects should auto-deploy to PyPI from Travis. Each project has to re-encrypt the `openvax` PyPI using the `travis encrypt` command. The text of the README must be converted from Markdown to RST in the `setup.py` file using `pypandoc`, which also requires that `pandoc` is installed on Travis.

## Version

The project's version should be stored in the top-most `__init__.py` file in a filed named `__version__`.


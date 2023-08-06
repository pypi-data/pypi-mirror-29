[pypi-version-badge]: https://img.shields.io/pypi/v/pygalle.core.base.klass.svg
[pypi-version-url]: https://pypi.org/project/pygalle.core.base.klass
[pypi-downloads-badge]: https://img.shields.io/pypi/dt/pygalle.core.base.klass.svg
[pypi-downloads-url]: https://pypi.org/project/pygalle.core.base.klass
[travis-badge]: https://img.shields.io/travis/pygalle-io/pygalle.core.base.klass/master.svg?label=TravisCI
[travis-badge-url]: https://travis-ci.org/pygalle-io/pygalle.core.base.klass
[circle-badge]: https://circleci.com/gh/pygalle-io/pygalle.core.base.klass/tree/master.svg?style=svg&circle-token=
[circle-badge-url]: https://circleci.com/gh/pygalle-io/pygalle.core.base.klass/tree/master
[coveralls-badge]: https://coveralls.io/repos/github/pygalle-io/pygalle.core.base.klass/badge.svg?branch=master
[coveralls-badge-url]: https://coveralls.io/github/pygalle-io/pygalle.core.base.klass?branch=master
[codeclimate-badge]: https://img.shields.io/codeclimate/github/pygalle-io/pygalle.core.base.klass.svg
[codeclimate-badge-url]: https://codeclimate.com/github/pygalle-io/pygalle.core.base.klass
[ember-observer-badge]: http://emberobserver.com/badges/pygalle.core.base.klass.svg
[ember-observer-badge-url]: http://emberobserver.com/addons/pygalle.core.base.klass
[license-badge]: https://img.shields.io/pypi/l/pygalle.core.base.klass.svg
[license-badge-url]: LICENSE.md
[documentation-badge]: https://readthedocs.org/projects/pygallecorebaseklass/badge/?version=latest
[documentation-badge-url]: http://pygallecorebaseklass.readthedocs.io/en/latest/?badge=latest

# pygalle.core.base.klass




---
&#x1F34E; <span style="color:red">**__Warning !__ Work in progress...**</span>
---


[![PyPI Version][pypi-version-badge]][pypi-version-url]
[![PyPI Downloads][pypi-downloads-badge]][pypi-downloads-url]
[![TravisCI Build Status][travis-badge]][travis-badge-url]
[![Test Coverage][coveralls-badge]][coveralls-badge-url]
[![Code Climate][codeclimate-badge]][codeclimate-badge-url]
[![Documentation Status][documentation-badge]][documentation-badge-url]
[![License][license-badge]][license-badge-url]


## Table of Contents

* [Synopsis](#synopsis)
* [Usage](#usage)
* [Installation](#installation)
* [API Reference](#api-reference)
* [Tests](#tests)
  * [Run unit tests](#tests_run-unit-tests)
* [Build](#build)
  * [Documentation](#generate-documentation)
    * [Generate README](#generate-documentation-readme)
    * [Generation API reference](#generate-documentation-api)
* [Compatibility](#compatibility)
  * [Node](#compatibility_python)
  * [Browser](#compatibility_browser)
* [Issues](#issues)
* [Contributing](#contributing)
* [Credits](#credits)
* [History](#history)
* [License](#license)

## <a name="synopsis"> Synopsis


## <a name="usage"> Usage

``` python

from pygalle.core.base.klass import PygalleBaseClass

# Extends the PygalleBaseClass
class CustomClass(PygalleBaseClass):

    def __init__(self, *args, **kwargs)
      super().__init__(*args, **kwargs)


```
## <a name="installation"> Installation

```
pip install pygalle.core.base.klass
```
## <a name="api-reference"> API Reference

Please refer to [API documentation](https://pygallecorebaseklass.readthedocs.io) hosted by [Read the Docs](https://readthedocs.org/).
## <a name="test"> Tests

### <a name="tests_run-unit-tests"> Run unit tests

Install package pytest:

```
pip install pytest
```

Then run:

```
pytest
``` 
## <a name="build"> Build

### <a name="generate-documentation"> Documentation

#### <a name="generate-documentation-readme"> Generate README

**Be careful!** [README](README.md) is generated using templates. 

Please **only** modify documentation from related [templates](./.templates).

Install packages Jinja2 and pynt :

```
pip install jinja2 pynt
```


Then you can generate documentation using the following command:

```
pynt -t .tasks/build.py docs
```

#### <a name="generate-documentation-api"> Generate API documentation

The [API documentation](https://pygallecorebaseklass.readthedocs.io) is automatically generated using [Read the Docs](https://readthedocs.org).
## <a name="compatibility"> Compatibility

### <a name="compatibility_python"> Python


* Tested using [Python 3.5](https://docs.python.org/3.5/).
* Tested using [Python 3.6](https://docs.python.org/3.6/).
## <a name="issues"> Issues

Feel free to [submit issues](pygalle-io/pygalle.core.base.klass/issues) and enhancement requests.
## <a name="contributing"> Contributing

Please refer to project's style guidelines and guidelines for submitting patches and additions. In general, we follow the "fork-and-pull" Git workflow.

 1. **Fork** the repo on GitHub
 2. **Clone** the project to your own machine
 3. **Commit** changes to your own branch
 4. **Push** your work back up to your fork
 5. Submit a **Pull request** so that we can review your changes

**NOTE**: Be sure to merge the latest from "upstream" before making a pull request!

## <a name="credits"> Credits

### Thanks to the developers of the very useful dependencies...

* [shortid](https://github.com/corpix/shortid) by [corpix](https://github.com/corpix/).



## <a name="history"> History

Please refer to [the changelog file](docs/CHANGELOG.md).

## <a name="license"> License

>
> [The MIT License](https://opensource.org/licenses/MIT)
>
> Copyright (c) 2018 [SAS 9 Février](https://9fevrier.com/)
>
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all
> copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
>AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.
>

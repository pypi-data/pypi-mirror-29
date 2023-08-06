# export-elements

[![code-climate-image]][code-climate]
[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![gemnasium-image]][gemnasium]

**Wrapper around govuk elements for use in Directory apps in Department for International Trade.**

---

## Installation

```shell
pip install -e git+https://git@github.com/uktrade/export-elements.git@v1.0.0#egg=export-elements
```

## Development

    $ git clone https://github.com/uktrade/export-elements
    $ cd export-elements
    $ make

## Publish to PyPI

The package should be published to PyPI on merge to master. If you need to do it locally then get the credentials from rattic and add the environment variables to your host machine:

| Setting                     |
| --------------------------- |
| DIRECTORY_PYPI_USERNAME     |
| DIRECTORY_PYPI_PASSWORD     |


Then run the following command:

    make publish


[code-climate-image]: https://codeclimate.com/github/uktrade/export-elements/badges/issue_count.svg
[code-climate]: https://codeclimate.com/github/uktrade/export-elements

[circle-ci-image]: https://circleci.com/gh/uktrade/export-elements/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/export-elements/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/export-elements/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/export-elements

[gemnasium-image]: https://gemnasium.com/badges/github.com/uktrade/export-elements.svg
[gemnasium]: https://gemnasium.com/github.com/uktrade/export-elements



# directory-cms-client

[![code-climate-image]][code-climate]
[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![gemnasium-image]][gemnasium]

**Directory CMS client.**

Client for the Directory Content Management read-only API.
---

## Requirements

## Installation

```shell
pip install -e git+https://git@github.com/uktrade/directory-cms-client.git@0.0.2#egg=directory-cms-client
```

## Usage

```python
from directory_cms_client import DirectoryCMSClient

cms_client = DirectoryCMSClient(
    base_url="https://directory-cms-dev.herokuapp.com",
    api_key=api_key
)
```


## Development

    $ git clone https://github.com/uktrade/directory-cms-client
    $ cd directory-cms-client

## Publish to PyPI

The package should be published to PyPI on merge to master. If you need to do it locally then get the credentials from rattic and add the environment variables to your host machine:

| Setting                     |
| --------------------------- |
| DIRECTORY_PYPI_USERNAME     |
| DIRECTORY_PYPI_PASSWORD     |


Then run the following command:

    make publish


[code-climate-image]: https://codeclimate.com/github/uktrade/directory-cms-client/badges/issue_count.svg
[code-climate]: https://codeclimate.com/github/uktrade/directory-cms-client

[circle-ci-image]: https://circleci.com/gh/uktrade/directory-cms-client/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/directory-cms-client/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/directory-cms-client/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/directory-cms-client

[gemnasium-image]: https://gemnasium.com/badges/github.com/uktrade/directory-cms-client.svg
[gemnasium]: https://gemnasium.com/github.com/uktrade/directory-cms-client



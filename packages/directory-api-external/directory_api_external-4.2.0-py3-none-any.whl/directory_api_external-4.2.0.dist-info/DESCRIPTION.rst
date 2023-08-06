# directory-api-client-external

[![code-climate-image]][code-climate]
[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![gemnasium-image]][gemnasium]

**Export Directory external API client.**

---

## Installation

```shell
pip install directory-api-client-external
```

## Usage

```python
from directory_api_external.client import DirectoryAPIClient

directory_client = DirectoryAPIClient(
    base_url="https://find-a-buyer.export.great.gov.uk/api",
    api_key=api_key
)
```

## Development

    $ git clone https://github.com/uktrade/directory-api-client-external
    $ cd directory-api-client-external

## Publish to PyPI

The package should be published to PyPI on merge to master. If you need to do it locally then get the credentials from rattic and add the environment variables to your host machine:

| Setting                     |
| --------------------------- |
| DIRECTORY_PYPI_USERNAME     |
| DIRECTORY_PYPI_PASSWORD     |


Then run the following command:

    make publish


[code-climate-image]: https://codeclimate.com/github/uktrade/directory-api-client-external/badges/issue_count.svg
[code-climate]: https://codeclimate.com/github/uktrade/directory-api-client-external

[circle-ci-image]: https://circleci.com/gh/uktrade/directory-api-client-external/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/directory-api-client-external/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/directory-api-client-external/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/directory-api-client-external

[gemnasium-image]: https://gemnasium.com/badges/github.com/uktrade/directory-api-client-external.svg
[gemnasium]: https://gemnasium.com/github.com/uktrade/directory-api-client-external



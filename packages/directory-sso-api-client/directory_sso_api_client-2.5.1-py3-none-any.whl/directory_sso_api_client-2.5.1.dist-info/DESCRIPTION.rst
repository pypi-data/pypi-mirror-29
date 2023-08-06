# directory-sso-api-client

[![code-climate-image]][code-climate]
[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![gemnasium-image]][gemnasium]

**[Export Directory SSO API client](https://www.directory.exportingisgreat.gov.uk/)**

---

## Requirements

## Installation

```shell
pip install -e git+https://github.com/uktrade/directory-sso-api-client.git@v2.2.0#egg=directory-sso-api-client
```

### Can't import package in PyCharm
In case `PyCharm` compains about missing `directory-sso-api-client` requirements after installing it to your virtualenv, then you have to re-install it but without `-e` parameter.
```shell
pip uninstall directory-sso-api-client
pip install git+https://github.com/uktrade/directory-sso-api-client.git@v2.2.0#egg=directory-sso-api-client
```


## Usage

```python
from directory_sso_api_client.client import DirectorySSOAPIClient

directory_sso_client = DirectorySSOAPIClient(
    base_url="https://account.trade.great.gov.uk/api",
    api_key=api_key
)
```

### Get user by session ID

```python
directory_sso_client.user.get(
    session_id=session_id
)
```

## Development

    $ git clone https://github.com/uktrade/directory-sso-api-client
    $ cd directory-ui
    $ make

## Publish to PyPI

The package should be published to PyPI on merge to master. If you need to do it locally then get the credentials from rattic and add the environment variables to your host machine:

| Setting                     |
| --------------------------- |
| DIRECTORY_PYPI_USERNAME     |
| DIRECTORY_PYPI_PASSWORD     |

Then run the following command:

    make publish


[code-climate-image]: https://codeclimate.com/github/uktrade/directory-sso-api-client/badges/issue_count.svg
[code-climate]: https://codeclimate.com/github/uktrade/directory-sso-api-client

[circle-ci-image]: https://circleci.com/gh/uktrade/directory-sso-api-client/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/directory-sso-api-client/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/directory-sso-api-client/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/directory-sso-api-client

[gemnasium-image]: https://gemnasium.com/badges/github.com/uktrade/directory-sso-api-client.svg
[gemnasium]: https://gemnasium.com/github.com/uktrade/directory-sso-api-client



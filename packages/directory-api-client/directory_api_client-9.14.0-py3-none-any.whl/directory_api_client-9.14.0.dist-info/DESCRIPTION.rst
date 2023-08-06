# directory-api-client

[![code-climate-image]][code-climate]
[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![gemnasium-image]][gemnasium]

**Export Directory internal API client.**

---

## Requirements

## Installation

```shell
pip install -e git+https://git@github.com/uktrade/directory-api-client.git@0.0.2#egg=directory-api-client
```

## Usage

```python
from directory_api_client.client import DirectoryAPIClient

directory_client = DirectoryAPIClient(
    base_url="https://api.directory.exportingisgreat.gov.uk",
    api_key=api_key
)
```

### Send registration form

```python
directory_client.enrolment.send_form(
    form_data=form_data
)
```

### Confirm registration email

```python
directory_client.registration.confirm_email(
    confirmation_code=confirmation_code,
)
```

## Development

    $ git clone https://github.com/uktrade/directory-api-client
    $ cd directory-api-client

## Publish to PyPI

The package should be published to PyPI on merge to master. If you need to do it locally then get the credentials from rattic and add the environment variables to your host machine:

| Setting                     |
| --------------------------- |
| DIRECTORY_PYPI_USERNAME     |
| DIRECTORY_PYPI_PASSWORD     |


Then run the following command:

    make publish


[code-climate-image]: https://codeclimate.com/github/uktrade/directory-api-client/badges/issue_count.svg
[code-climate]: https://codeclimate.com/github/uktrade/directory-api-client

[circle-ci-image]: https://circleci.com/gh/uktrade/directory-api-client/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/directory-api-client/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/directory-api-client/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/directory-api-client

[gemnasium-image]: https://gemnasium.com/badges/github.com/uktrade/directory-api-client.svg
[gemnasium]: https://gemnasium.com/github.com/uktrade/directory-api-client



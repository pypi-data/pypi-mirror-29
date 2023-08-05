Pytest Falcon Client
===
Pytest `client` fixture for the [Falcon Framework](https://github.com/falconry/falcon).

[![Build Status](https://travis-ci.org/cryptomaniac512/pytest-falcon-client.svg?branch=master)](https://travis-ci.org/cryptomaniac512/pytest-falcon-client)
[![Coverage Status](https://coveralls.io/repos/github/cryptomaniac512/pytest-falcon-client/badge.svg?branch=master)](https://coveralls.io/github/cryptomaniac512/pytest-falcon-client?branch=master)
![Python versions](https://img.shields.io/badge/python-3.4,%203.5,%203.6-blue.svg)
[![PyPi](https://img.shields.io/badge/PyPi-0.1.0-yellow.svg)](https://pypi.python.org/pypi/pytest-falcon-client)

## Installation

``` shell
pip install pytest-falcon-client
```

Before using it you must define `api` fixture that returns instance of your `falcon.API`

``` python
import pytest

from yout_application import create_api

@pytest.fixture
def api():
    return create_api()
```

## Usage

``` python
def test_something(client):
    got = client.get('/your_url/42/')  # returns json of response and automatically check response status code
	assert got == {'awesome': 'response'}

	response = client.get('/your_url/100500/')  # returns testing response object and skip status code check
	assert response.status_code == 400
	assert response.json = 'Invalid id'
```

You can define callback function to make global assertions in your api tests.

For example, you can test cors headers like this globally
``` python
import pytest


def cors_callback(client, response):
    assert response.headers['Access-Control-Allow-Origin'] == '*'


pytestmark = pytest.mark.client(callback=cors_callback)


def test_something_else(client):
    got = client.get('/some_url/100500/')
	assert got == {'awesome': 100500}
```

Look at more examples in `tests`.

# Backoffice client

[![Build Status](https://travis-ci.org/gdml/backoffice-client.svg?branch=master)](https://travis-ci.org/gdml/backoffice-client)
[![codecov](https://codecov.io/gh/gdml/backoffice-client/branch/master/graph/badge.svg)](https://codecov.io/gh/gdml/backoffice-client)
[![PyPI version](https://badge.fury.io/py/gm-backoffice-client.svg)](https://badge.fury.io/py/gm-backoffice-client)

This is a simple client for our v1 order API.

This client incapsulates all low-level logic, like makeing HTTP-queries or order schema validation.

## Install

The project is available in pypi, so

```bash
# install from pip
$ pip install backoffice-client
```

## Usage

```python
from backoffice import backofficeClient

client = BackofficeClient(
    url='https://app.gdml.ru/api/v1',
    token='your-auth-token',
)

order = {
    'customer': {
        'name': 'Константин Львович Череззаборногузадерищенко',
        'phone': '+7 901 001-02-03',
        'email': 'putthelegoverthegrid@work.com',
    },
    'delivery': {
        'address': 'г. Магадан, ул. 3-я Спортивная, д. 15 кв. 22',
        'desired_date': '12.01.2023',
    },
}
items = [
    {
        'site_id': 2194,
        'name': 'Жердь для забора чугуниевая, 3.14 метра',
        'quantity': 15,
        'price': 200, # per single unit
    },
    {
        'name': 'Подборка для чугуниевой жерди, полтонны',  # the minimal item
    },
]

client.validate_order(order)  # also called during send()
client.validate_items(items)  # and this one either

client.send(order)
```

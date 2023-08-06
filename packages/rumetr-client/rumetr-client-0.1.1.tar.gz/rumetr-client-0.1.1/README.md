# rumetr-client

[![Build Status](https://travis-ci.org/f213/rumetr-client.svg?branch=master)](https://travis-ci.org/f213/rumetr-client)
[![codecov](https://codecov.io/gh/f213/rumetr-client/branch/master/graph/badge.svg)](https://codecov.io/gh/f213/rumetr-client)

Python client and scrapy workflow for rumetr.com API.

## Usage

Install it with pip
```
pip install rumetr-client
```

Add this to your `scrapy/settings.py`:

```python

ITEM_PIPELINES = {
    'rumetr.scrapy.UploadPipeline': 300,
}

RUMETR_API_HOST = 'https://sandbox.rumetr.com/api/v11'
RUMETR_TOKEN = '<YOUR TOKEN>'
RUMETR_DEVELOPER = '<PARTICULAR DEVELOPER CODE>'

```

Now your parser should yield our pre-formatted
item per each found appartment:

```python
# developer/developerspider.py

from rumetr.scrapy import ApptItem as Item

def your_scrapy_callback(response):

      for appt in response.css('.your-appt[selector]):
         yield Item(
            complex_name=response.meta['complex_name'],
            complex_id=response.meta['complex_id'],
            complex_url=URL + response.meta['complex_url'] + '/',
            addr=response.meta['complex_addr'],

            house_id=appt['house_id'],
            house_name=appt['house_name'],
            house_url=URL + response.meta['complex_url'],

            id=appt['id'],
            floor=floor_number,
            room_count=appt['roomQuantity'] if appt['roomQuantity'] not in ['С', 'C'] else 1,
            is_studio=appt['roomQuantity'] in ['С', 'C'],
            square=appt['wholeAreaBti'],
            price=appt['wholePrice'],
         )

```

# Abiquo API Python Client

[![Build Status](https://travis-ci.org/abiquo/api-python-client.svg?branch=master)](https://travis-ci.org/abiquo/api-python-client)

This is a Python client for the Abiquo API. It allows to consume the API
in a dynamic way and to navigate its resources using its built-in linking
features.

The project depends on [requests](http://docs.python-requests.org/en/latest/)
and optionally on [requests_oauthlib](https://requests-oauthlib.readthedocs.org/en/latest/),
if you prefer to use OAuth instead of Basic Authentication.

## Installation

You can easily install the module with:

```bash
pip install abiquo-api
```

## Usage

Using the client is pretty straightforward. Here are some examples:

### Using HTTP Basic Authentication

This example shows how to get the list of existing datacenters and how to
navigate its links to create a rack in each of them:

```python
import json
from abiquo.client import Abiquo
from abiquo.client import check_response

api = Abiquo(API_URL, auth=(username, password))
code, datacenters = api.admin.datacenters.get(
    headers={'Accept':'application/vnd.abiquo.datacenters+json'})

print "Response code is: %s" % code
for dc in datacenters:
    print "Creating rack in datacenter %s [%s]" % (dc.name, dc.location)
    code, rack = dc.follow('racks').post(
            data=json.dumps({'name': 'New rack'}),
            headers={'accept':'application/vnd.abiquo.rack+json',
                     'content-type':'application/vnd.abiquo.rack+json'})
    check_response(201, code, rack)
    print "Response code is: %s" % code
    print "Created Rack: %s" % rack.name
```

Note that you don't need to care about pagination, the client handles it internally for you.

### Using an OpenID Bearer access token

If your platform uses OpenID and you have a Bearer access token, you can configure the client
as follows:

```python
import json
from abiquo.client import Abiquo
from abiquo.auth import BearerTokenAuth 

api = Abiquo(API_URL, auth=BearerTokenAuth(token))
```

### Using OAuth

To use OAuth first you have to register your client application in the Abiquo API. To do that, you can
use the `register.py` script as follows, and it will register the application and generate the access
tokens:

```bash
$ python register.py 
Abiquo API endpoint: http://localhost/api
Username or OpenID access_token (prefixed with "openid:"): your-username
Password: your-password
Application name: My Cool App

App key: 54e00f27-6995-40e8-aefe-75f76f514d89
App secret: eayP6ll3G02ypBhQBmg0398HYBldkf3B5Jqti73Z
Access token: c9c9bd44-6812-4ddf-b39d-a27f86bf03da
Access token secret: MifYOffkoPkhk33ZTiGOYnIg8irRjw7BlUCR2GUh7IQKv4omfENlMi/tr+gUdt5L8eRCSYKFQVhI4Npga6mXIVl1tCMHqTldYfqUJZdHr0c=
```

If your Abiquo platform uses OpenID, then you can register your application using the Access Token as follows:

```bash
$ python register.py 
Abiquo API endpoint: http://localhost/api       
Username or OpenID access_token (prefixed with "openid:"): openid:bac4564c-4522-450e-985b-5f880f02a3dd
Application name: My Cool App

App key: 685df603-cb51-4ffa-bd7e-8b0235f5ac70
App secret: HtoICXYr2WENp5D1g7UjbifNizTFh1I3AW3ylEjm
Access token: b1b2856e-5098-4a54-ae3c-d99b739f6770
Access token secret: pBioSC7SNv/0lPRQWBiOr9uSXf8bIs6D2jVVAy2WkBq3Vr37efMKv3mTugk9+TlTAtrWPsPoPdHDGjEtbb5PBHKb2JKWUC9y+OZ44I4v9kk=
```

Once you have the tokens, you just have to create the authentication object and pass it to the
Abiquo client as follows:

```python
from requests_oauthlib import OAuth1
from abiquo.client import Abiquo

APP_KEY = '54e00f27-6995-40e8-aefe-75f76f514d89'
APP_SECRET = 'eayP6ll3G02ypBhQBmg0398HYBldkf3B5Jqti73Z'
ACCESS_TOKEN = 'c9c9bd44-6812-4ddf-b39d-a27f86bf03da'
ACCESS_TOKEN_SECRET = 'MifYOffkoPkhk33ZTiGOYnIg8irRjw7BlUCR2GUh7IQKv4omfENlMi/tr+gUdt5L8eRCSYKFQVhI4Npga6mXIVl1tCMHqTldYfqUJZdHr0c='

oauth=OAuth1(APP_KEY,
        client_secret=APP_SECRET,
        resource_owner_key=ACCESS_TOKEN,
        resource_owner_secret=ACCESS_TOKEN_SECRET)

api = Abiquo(API_URL, auth=oauth)
```

And that's it! Now you can use the Abiquo client as shown in the Basic Authentication examples.

## Running the tests

You can run the unit tests as follows:

```bash
pip install requests requests_oauthlib httpretty
python -m unittest discover -v
```

## Contributing

This project is still in an early development stage and is still incomplete. All
contributions are welcome, so feel free to [raise a pull request](https://help.github.com/articles/using-pull-requests/).

## License

The Abiquo API Java Client is licensed under the Apache License version 2. For
further details, see the [LICENSE](LICENSE) file.

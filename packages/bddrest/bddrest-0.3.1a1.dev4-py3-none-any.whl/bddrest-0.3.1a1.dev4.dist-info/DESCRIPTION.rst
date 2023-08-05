# bddrest

Toolchain to define and verify REST API in BDD.


## Quick start


```python

from bddrest import given, when, then, and_, response


with given(
        wsgi_application,
        title='Quickstart!',
        url='/books/id: 1',
        as_='visitor'):

    then(response.status == '200 OK')
    and_('foo' in response.json)
    and_(response.json['foo'] == 'bar')

    when(
        'Trying invalid book id',
        url_parameters={'id': None}
    )

    then(response.status_code == 404)


```



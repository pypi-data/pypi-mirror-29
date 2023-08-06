Collection resources (entities)
-------------------------------

.. code-block:: python

    >>> resp = client.get('/author/',
    ...                   headers={'accept': 'application/json'})
    >>> print(resp)  # doctest: +ELLIPSIS
    Response: 200 OK
    Allow: GET, POST
    Content-Type: application/json
    Link: </>; rel="up", </author/schema>; rel="describedby"; type="application/schema+json"
    [
        {
            "id": "...",
            "type": "author",
            "title": "Ernest Hemingway"
        }
    ]

Notice the ``Allow: POST`` header, meaning the server would accept the
creation of entity of type ``Author`` at the ``/author`` endpoint.
So let's add some ``Author`` entities:

.. code-block:: python

    >>> resp = client.post_json('/author/', {'name': 'Victor Hugo'},
    ...                         headers={'Accept': 'application/json'})
    >>> print(resp)  # doctest: +ELLIPSIS
    Response: 201 Created
    Content-Type: application/json
    Location: https://localhost:80/author/.../
    {
        "name": "Victor Hugo"
    }
    >>> resp = client.post_json('/author/', {'name': 'Aldous Huxley'},
    ...                         headers={'Accept': 'application/json'})
    >>> print(resp)  # doctest: +ELLIPSIS
    Response: 201 Created
    Content-Type: application/json
    Location: https://localhost:80/author/.../
    {
        "name": "Aldous Huxley"
    }

Now we have something in the author collection:

.. code-block:: python

    >>> resp = client.get('/author/',
    ...                   headers={'accept': 'application/json'})
    >>> print(resp)  # doctest: +ELLIPSIS
    Response: 200 OK
    Allow: GET, POST
    Content-Type: application/json
    Link: </>; rel="up", </author/schema>; rel="describedby"; type="application/schema+json"
    [
        {
            "type": "author",
            "id": "...",
            "title": "Aldous Huxley"
        },
        {
            "type": "author",
            "id": "...",
            "title": "Victor Hugo"
        },
        {
            "type": "author",
            "id": "...",
            "title": "Ernest Hemingway"
        }
    ]

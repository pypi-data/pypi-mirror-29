Entity workflow
---------------

Entities' workflow can be handled through the JSON API from the
`/<etype>/<eid>/workflow-transitions/` endpoint. It is possible to both get
already passed workflow transitions and to add new transition to an entity.

To illustrate, this we'll work with a `UserAccount` entity for which the
workflow consists of `activate` and `deactivate` transitions.

First, let's create such an entity:

.. code-block:: python

    >>> r = client.post_json('/useraccount/', {'username': 'tommy'},
    ...                      headers={'Accept': 'application/json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 201 Created
    Content-Type: application/json
    Location: https://localhost:80/useraccount/.../
    {
      "username": "tommy",
      "in_state": "created"
    }

We can get the workflow transitions for the entity (there's none currently) as
follows:

.. code-block:: python

    >>> r = client.get('/useraccount/tommy/workflow-transitions',
    ...                headers={'Accept': 'application/json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 200 OK
    Content-Type: application/json
    Link: </useraccount/.../workflow-transitions/schema>; rel="describedby"; type="application/schema+json"
    []

To add a new transition (i.e. change the workflow state), we `POST` to the
*workflow-transitions* route the *name* of the transition and optionally a
*comment*:

.. code-block:: python

    >>> r = client.post_json('/useraccount/tommy/workflow-transitions',
    ...                      {'name': 'activate', 'comment': 'Tommy is in'},
    ...                      headers={'Accept': 'application/json'})
    >>> print(r)
    Response: 204 No Content

Finally, we can get back the list of transitions:

.. code-block:: python

    >>> r = client.get('/useraccount/tommy/workflow-transitions',
    ...                headers={'Accept': 'application/json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 200 OK
    Content-Type: application/json
    Link: </useraccount/.../workflow-transitions/schema>; rel="describedby"; type="application/schema+json"
    [
      {
        "id": "...",
        "title": "Tommy is in",
        "type": "trinfo"
      }
    ]

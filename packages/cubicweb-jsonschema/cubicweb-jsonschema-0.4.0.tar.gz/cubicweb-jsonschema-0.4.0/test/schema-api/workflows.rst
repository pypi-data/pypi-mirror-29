Entity workflow schema
----------------------

Workflowable entity types expose the schema of their workflow transitions at
the `/<etype>/<eid>/workflow-transitions/schema` endpoint. We'll work on a
``UserAccount`` entity type which has a simple `created` → `activated` →
`deactivated` workflow.

First, let's create a ``UserAccount`` entity by looking at what the creation
schema describes:

.. code-block:: python

    >>> r = client.get('/useraccount/schema?role=creation',
    ...                headers={'Accept': 'application/schema+json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 200 OK
    Content-Type: application/json
    Link: </useraccount/>; rel="describes"; type="application/json"
    {
      "$schema": "http://json-schema.org/draft-06/schema#",
      "additionalProperties": false,
      "properties": {
        "username": {
          "title": "username",
          "type": "string"
        }
      },
      "required": [
        "username"
      ],
      "title": "UserAccount",
      "type": "object"
    }
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

Notice the ``"in_state"`` property that appears in the JSON instance along
with respective schema as shown below.

From our entity's JSON Hyper Schema, we can find a link with a custom relation
type ``tag:cubicweb.org,2017:workflow-transitions`` (following the `Tag URI
<https://tools.ietf.org/html/rfc4151>`_ scheme) as advised by JSON Hyper
Schema specification:

.. code-block:: python

    >>> r = client.get('/useraccount/tommy/schema',
    ...                headers={'Accept': 'application/schema+json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 200 OK
    Content-Type: application/json
    {
      "$schema": "http://json-schema.org/draft-06/schema#",
      "additionalProperties": false,
      "links": [
        {
          "href": "/useraccount/",
          "rel": "collection",
          "targetSchema": {
            "$ref": "/useraccount/schema"
          },
          "title": "UserAccount_plural"
        },
        {
          "href": "/useraccount/tommy/",
          "rel": "self",
          "submissionSchema": {
            "$ref": "/useraccount/tommy/schema?role=edition"
          },
          "targetSchema": {
            "$ref": "/useraccount/tommy/schema?role=view"
          },
          "title": "UserAccount #..."
        },
        {
          "href": "/useraccount/tommy/workflow-transitions/",
          "rel": "tag:cubicweb.org,2017:workflow-transitions",
          "title": "workflow history"
        }
      ],
      "properties": {
        "username": {
          "title": "username",
          "type": "string"
        },
        "in_state": {
          "title": "state",
          "type": "string",
          "readOnly": true
        }
      },
      "title": "UserAccount",
      "type": "object"
    }


This link endpoint is of course described by a JSON Schema to be found by
looking at ``rel="describedby"`` `Link` header:

.. code-block:: python

    >>> r = client.head('/useraccount/tommy/workflow-transitions/',
    ...                 headers={'Accept': 'application/json'})
    >>> print(r)
    Response: 200 OK
    Content-Type: application/json
    Link: </useraccount/tommy/>; rel="up"; title="tommy", </useraccount/tommy/workflow-transitions/schema>; rel="describedby"; type="application/schema+json"


.. code-block:: python

    >>> r = client.get('/useraccount/tommy/workflow-transitions/schema',
    ...                headers={'Accept': 'application/schema+json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 200 OK
    Content-Type: application/json
    Link: </useraccount/.../workflow-transitions/>; rel="describes"; type="application/json"
    {
      "$schema": "http://json-schema.org/draft-06/schema#",
      "items": {
        "links": [
          {
            "anchor": "#",
            "href": "/useraccount/.../workflow-transitions/{id}",
            "rel": "item"
          }
        ],
        "properties": {
          "id": {
            "type": "string"
          },
          "title": {
            "type": "string"
          },
          "type": {
            "type": "string"
          }
        },
        "type": "object"
      },
      "links": [
        {
          "href": "/useraccount/.../workflow-transitions/",
          "rel": "self",
          "submissionSchema": {
            "$ref": "/useraccount/.../workflow-transitions/schema?role=creation"
          },
          "targetSchema": {
            "$ref": "/useraccount/.../workflow-transitions/schema"
          },
          "title": "TrInfo_plural"
        }
      ],
      "title": "TrInfo_plural",
      "type": "array"
    }

This Hyper-Schema is an array of items (which will be `TrInfo` objects here).
The ``submissionSchema`` documents how to *submit* a new workflow transition:

.. code-block:: python

    >>> r = client.get('/useraccount/tommy/workflow-transitions/schema?role=creation',
    ...                headers={'Accept': 'application/schema+json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 200 OK
    Content-Type: application/json
    Link: </useraccount/.../workflow-transitions/>; rel="describes"; type="application/json"
    {
      "$schema": "http://json-schema.org/draft-06/schema#",
      "properties": {
        "comment": {
          "type": "string"
        },
        "name": {
          "oneOf": [
            {
              "enum": [
                "activate"
              ],
              "title": "activate"
            }
          ],
          "type": "string"
        }
      },
      "required": [
        "name"
      ],
      "title": "TrInfo",
      "type": "object"
    }

We see that we should send a JSON document with a required ``name`` property
and an optional ``comment``. Values for ``name`` are restricted to possible
transitions on the entity as can be seen in the ``oneOf`` array above.

Now if we change the state of the entity:

.. code-block:: python

    >>> r = client.post_json('/useraccount/tommy/workflow-transitions',
    ...                      {'name': 'activate'},
    ...                      headers={'Accept': 'application/json'})

and fetch back the previous JSON Schema:

.. code-block:: python

    >>> r = client.get('/useraccount/tommy/workflow-transitions/schema?role=creation',
    ...                headers={'Accept': 'application/schema+json'})
    >>> print(r)  # doctest: +ELLIPSIS
    Response: 200 OK
    Content-Type: application/json
    Link: </useraccount/.../workflow-transitions/>; rel="describes"; type="application/json"
    {
      "$schema": "http://json-schema.org/draft-06/schema#",
      "properties": {
        "comment": {
          "type": "string"
        },
        "name": {
          "oneOf": [
            {
              "enum": [
                "deactivate"
              ],
              "title": "deactivate"
            }
          ],
          "type": "string"
        }
      },
      "required": [
        "name"
      ],
      "title": "TrInfo",
      "type": "object"
    }


Messages sent by the client
===========================

Messages sent by the client must be JSON-encoded objects with at least the
"type" and "id" keys, both of which must have string values.

The "type" identifies the type of request, whilst the "id" is echoed back in
replies sent by the server.

The request messages are detailed below.


select
------
```json
{
    "type": "select",
    "id": "opaque string",
    "relation": "demonstration_table",

    "schema": "wspg",
    "query-rules": {...},
    "returning-columns": ["id", "name", "address"],
    "order": [
        {"column": "name"},
        {"column": "age", "direction": "descending"},
        {"column": "address", "nulls": "first"}],
    "limit": 3
}
```

 * "schema" is optional - the default value is no schema
 * "query-rules" is optional - the default value is no filtering
 * "returning-columns" is optional - the defalt value is all columns
 * "order" is optional - the default is unordered
 * "limit" is optional - the default is no limit

If successful, the result object will be:
```json
[
    {"id": 13, "name": "Alan Turing", "address": "123 Fake Street"},
    {"id": 12, "name": "Grace Hopper", "address": "62 West Wallaby Street"},
    {"id": 14, "name": "Jon Postel", "address": "17 Cherry Tree Lane"}
]
```
(or null if "returning-columns" was an empty list)


insert
------
```json
{
    "type": "insert",
    "id": "opaque string",
    "relation": "demonstration_table",
    "rows": [
        {"name": "Radia Perlman", "subscribed": true},
        {"name": "Carl Sassenrath", "postcode": "WG7 7FU"}
    ],

    "schema": "wspg",
    "returning-columns": ["id", "name"]
}
```

 * "schema" is optional - the default value is no schema
 * "returning-columns" is optional - the default value is all columns

If successful, the result object will be:
```json
[
    {"id": 15, "name": "Radia Perlman"},
    {"id": 16, "name": "Carl Sassenrath"}
]
```
(or null if "returning-columns" was an empty list)


update
------
```json
{
    "type": "update",
    "id": "opaque string",
    "relation": "demonstration_table",
    "updates": {"address": "62 West Wallaby Street", "postcode": "WG7 7FU"},

    "schema": "wspg",
    "query-rules": {...},
    "returning-columns": ["id", "name"]
}
```

 * "schema" is optional - the default value is no schema
 * "query-rules" is optional - the default value is no filtering
 * "returning-columns" is optional - the default value is all columns

If successful, the result object will be:
```json
[
    {"id": 12, "name": "Grace Hopper"},
    {"id": 13, "name": "Alan Turing"},
    {"id": 14, "name": "Jon Postel"},
    {"id": 15, "name": "Radia Perlman"},
    {"id": 16, "name": "Carl Sassenrath"}
]
```
(or null if "returning-columns" was an empty list)


delete
------
```json
{
    "type": "delete",
    "id": "opaque string",
    "relation": "demonstration_table",

    "schema": "wspg",
    "query-rules": {...}
}
```

 * "schema" is optional - the default value is no schema
 * "query-rules" is optional - the default value is no filtering

If successful, the result object will be null.


listen
------
```json
{
    "type": "listen",
    "id": "opaque string",
    "channel": "task_list_updated"
}
```

If successful, the result object will be null.


unlisten
------
```json
{
    "type": "unlisten",
    "id": "opaque string",
    "channel": "task_list_updated"
}
```

If successful, the result object will be null.


apply-jwt
---------
```json
{
    "type": "apply-jwt",
    "id": "opaque string",
    "issuer": "weblogin",

    "token": "eyJh[...]7HgQ"
}
```

 * token is optional - the default value is null.

A null token will clear any existing claims set for the issuer.

If successful, the result object will be null and any existing claims set for
the issuer will be replaced.

If unsuccessful, any existing claims set for the issuer is left unchanged.


Messages sent by the server
===========================

Messages sent by the server are JSON-encoded objects with a "type" key having a
string value.

The server messages are detailed below:


failed
------
```json
{
    "type": "failed",
    "id": "opaque string",
    "reason": "Human-readable text"
}
```

This indicates that the server was unable to successfully process the request.


succeeded
---------
```json
{
    "type": "succeeded",
    "id": "opaque string",
    "result": ...
}
```

This indicates that the server successfully processed the request.  The "result"
object is specific to the type of request and is described in the previous
section.


database-readiness
------------------
```json
{
    "type": "database-readiness",
    "ready": true
}
```

This indicates whether the server believes the backend database is ready.

This is sent immediately after the client connects and whenever the readiness
state changes.


notification
------------
```json
{
    "type": "notification",
    "channel": "task_list_updated",
    "payload": "Row 123 changed"
}
```


Note about concurrency
======================

Multiple requests made by the client are processed concurrently by the server,
so it is possible for results to arrive out of order - use the "id" key to
relate results to their request.


Note about database readiness
=============================

When a backend database becomes unavailable, the client will receive a
"database-readiness" message with "ready" set to false.  Once the server
has resynchronised with the backend database, the client will receive a
"database-readiness" message with "ready" set to true.  The server will have
resubscribed to channels as requested by the client before sending
"ready": true, however some notifications may be missed whilst the server
was reconnecting to the backend database.


Note about query-rules
======================

"query-rules" is a [jQuery QueryBuilder](http://querybuilder.js.org/) ruleset.

A simple example object is:
```json
{
    "condition": "AND",
    "rules": [
        {
            "field": "address",
            "operator": "string_like",
            "value": "%Street"
        },
        {
            "condition": "OR",
            "rules": [
                {
                    "field": "name",
                    "operator": "string_case_insensitive_equal_to",
                    "value": "ALAN turing"
                },
                {
                    "field": "id",
                    "operator": "greater_than_or_equal_to",
                    "value": "12"
                }
            ]
        }
    ]
}
```

For details of the available operators, see the QueryRulesRuleSetParser class.

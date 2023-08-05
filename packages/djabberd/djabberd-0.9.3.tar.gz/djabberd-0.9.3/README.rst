Generic application to handle https://ejabberd-saas.com/ Remote Data API calls

==========
 djabberd
==========

For each specific tasks a handler function must be implemented.

Install
-------
::

   pip install djabberd

Quick start
-----------

1. Include the django-ejabberd URLconf in your project urls.py like this::
::

   url(r'', include('djabberd.urls'),

::

   # For Django==1.8
   url(r'', include('djabberd.urls'), namespace='djabberd')

2. Setup the handler in your Django settings::
::

    DJABBERD_API_HANDLERS='your.module.path'

Based on ejabberd-saas's documentation those endpoints are required(01-Feb-2016):

1. User management:

   1. Authentication ('/auth')
   2. User exists ('/user')

2. Roster management:

   1. Retrieve user roster ('/roster')

3. Archive:

   1. Store ('/archive')
   2. Get ('/archive')

There must be one function for each endpoint that should be implemented like this:

* user_authentication(username, password):

  - Returns `True` if authentication is valid
  - Returns `False` if authentication is *not* valid

* user_exists(username):

  - Returns `True` if user exists
  - Returns `False` if not(or if it is not active)

* retrieve_user_roster(username):

  - Returns the roster in JSON format
  - Returns `False` if user does not exist

* archive_store(payload)

  - Returns `True` if message has been stored
  - Returns a string containing an error message if message has *not* been stored

* archive_get(username[, peer, after, before, limit, type])

  - Returns the message history in JSON format
  - Returns `False` in any other case

Formats
-------

* retrieve_user_roster::

   {"roster": [
       {"username": "CONTACT", 
        "subscription": "both", 
        "nick": "NICK"}, 
        ...
     ]}

* archive_store::

     {"username": "USERNAME1",
      "peer": "USERNAME2",
      "xml": "MESSAGE_STANZA",
      "body": "TEXT",
      "timestamp": "TIMESTAMP",
      "direction": "DIRECTION"}

* archive_get::

     {"archive": [{"username": "USERNAME1", 
                   "peer": "USERNAME2", 
                   "xml": "MESAGE_STANZA", 
                   "body": "TEXT", 
                   "timestamp": "TIMESTAMP", 
                   "direction": "DIRECTION"}, ...]
                   "count" : MESSAGES_NUMBER
     }


Considerations
--------------

Based on ejabberd-saas's documentation:

- If XMPP JID is "userid@xmppdomain", just pass "userid"
- If XMPP JID of USER is "userid@xmppdomain", just pass "xmppdomain"
- If an exception is raised from your handler it would be treated as a server error
- Return HTTP 200 for the successful case
- Return HTTP 401 if authentication fails
- Return HTTP 401 if it's not the successful case
- Return HTTP 500 for server errors, this is the Django's default behavior

Running Tests
=============
::

   python setup.py develop
   python runtests.py [tests.<tests_module>[.<TestClass>[.<test_method>]]]

Obsession
=========

Fast WSGI sessions. Zero dependencies. Python 3 ready.

Basic usage::

    import obsession

    application = obsession.SessionMiddleware(application)


Advanced usage::

    # Customize all the options
    application = obsession.SessionMiddleware(
        application,
        id_persister=obsession.CookieIdPersistence(cookie_name='mysession',
                                                   max_age=86400,
                                                   path='/my-site',
                                                   domain='mysite.example.org'
                                                   secure=True),
        backend=obsession.FileBackend(directory='/tmp/session-store',
                                      prefix='session_')
    )


Your application will now have a session object available in
``environ['ob.session']``.

The session object acts like a regular dictionary::

    session = environ['ob.session']
    session['foo'] = 'bar'
    session['bar'] = [1, 2, 3]

The session will be saved automatically whenever you mutate the
session object itself - for example by assigning a new key, or reassigning an
existing key. However if you change an already stored value then
you should call ``session.save()`` to ensure your changes are saved.

There are some useful extra properties and methods::

    # Persist the session to the backend
    session.save()

    # What's my session id?
    my_session_id = session.id

    # Cycle the session id.
    # This generates a new session id and invalidates the old one.
    session.cycle()

    # Load a session with a known id.
    # Useful if you need to pass the session through another service that
    # does not have access to the cookie.
    s = environ['ob.session']
    s.load_id('my_session_id')

    # Delete the session.
    # This removes all data from the backend storage and deletes the client's
    # session cookie
    session.delete()

0.2 (released 2018-03-12)
-------------------------

* Added JSON serializer
* Bugfix: session ids ending in periods are no longer silently dropped
* Only set a session id cookie when new session are created or when the id has
  changed, avoiding unnecessary Set-Cookie headers being sent.

0.1
----

* Initial release


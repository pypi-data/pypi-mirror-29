# Copyright 2015 Oliver Cope
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import defaultdict
from functools import partial
import io
try:
    from http.cookies import BaseCookie
except ImportError:
    from Cookie import BaseCookie
from wsgiref.util import setup_testing_defaults
from wsgiref.validate import validator

from obsession import (SessionMiddleware, CookieIdPersistence, Session,
                       MemoryBackend)
from obsession import JSONSerializer


class Response(object):

    def __init__(self, app, environ={}, **kwargs):
        environ = dict(environ, **kwargs)
        environ.setdefault('QUERY_STRING', '')
        setup_testing_defaults(environ)
        app = validator(app)
        self.environ = environ
        self.headers = []
        self.status = None
        self.exc_info = None
        self.content_iter = app(environ, self.start_response)
        self.content = list(self.content_iter)
        self.body_bytes = b''.join(self.content)
        self.body = self.body_bytes.decode('UTF-8')
        getattr(self.content_iter, 'close', lambda: None)()

    def start_response(self, status, headers, exc_info=None):
        self.status = status
        self.headers = headers
        self.header_mapping = defaultdict(list)

        for k, v in headers:
            self.header_mapping[k.lower()].append(v)
        self.status_code = int(status.split()[0])

    @property
    def session(self):
        return self.environ['ob.session']

    def __getitem__(self, name):
        try:
            return self.get_list(name)[0]
        except IndexError:
            raise KeyError(name)

    def get_list(self, name):
        return self.header_mapping[name.lower()]

    @property
    def cookies(self):
        cookies = BaseCookie()
        for c in self.get_list('set-cookie'):
            cookies.load(c)
        return cookies


def app(*side_effects):

    def app(environ, start_response):

        for func in side_effects:
            func(environ['ob.session'])

        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'<html>whoa nelly!</html>']
    return app


def reads_a_session_key(session):
    return 'foo' in session


def sets_a_session_key(session):
    session['foo'] = 'bar'


def increments_a_session_value(session):
    session['foo'] = session.get('foo', 0) + 1


def deletes_a_session_value(session):
    del session['foo']


def deletes_the_session(session):
    session.delete()


class TestSessionMiddleware(object):

    def test_it_doesnt_set_a_cookie_if_unused(self):
        r = Response(SessionMiddleware(app()))
        assert r.get_list('set-cookie') == []

        r = Response(SessionMiddleware(app(reads_a_session_key)))
        assert r.get_list('set-cookie') == []

    def test_it_doesnt_set_a_cookie_if_id_unchanged(self):
        r = Response(SessionMiddleware(app(sets_a_session_key)))
        session_key = r.cookies['_obs'].coded_value

        r = Response(SessionMiddleware(app(sets_a_session_key)),
                     HTTP_COOKIE='_obs=' + session_key)
        assert r.get_list('set-cookie') == []

    def test_it_sets_a_cookie_if_session_created(self):
        r = Response(SessionMiddleware(app(sets_a_session_key)))
        assert '_obs=' in r['set-cookie']

    def test_it_persists_the_session(self):
        a = SessionMiddleware(app(increments_a_session_value))
        r = Response(a)
        assert r.session['foo'] == 1
        r2 = Response(a, HTTP_COOKIE='_obs=' + r.cookies['_obs'].coded_value)
        assert r2.session['foo'] == 2

    def test_it_deletes_the_session(self):
        backend = MemoryBackend()
        a = SessionMiddleware(app(sets_a_session_key), backend=backend)
        r = Response(a)
        assert len(backend.keys()) == 1

        a = SessionMiddleware(app(deletes_the_session), backend=backend)
        r = Response(a, HTTP_COOKIE='_obs=' + r.cookies['_obs'].coded_value)
        assert len(backend.keys()) == 0
        assert len(r.cookies) == 0

    def test_sessions_are_independent(self):
        a = SessionMiddleware(app(increments_a_session_value))
        assert Response(a).session['foo'] == 1
        assert Response(a).session['foo'] == 1

    def test_it_randomizes_ids(self):

        values = set()
        for i in range(100):
            r = Response(SessionMiddleware(app(sets_a_session_key)))
            values.add(r['set-cookie'])
        assert len(values) == 100

    def test_it_cycles_the_id_if_backend_fails(self):
        backend = MemoryBackend()
        a = SessionMiddleware(app(increments_a_session_value), backend=backend)
        r = Response(a)
        assert r.session['foo'] == 1
        backend.delete(r.cookies['_obs'].value)
        r2 = Response(a, HTTP_COOKIE='_obs=' + r.cookies['_obs'].coded_value)
        assert r2.session['foo'] == 1
        assert r2.cookies['_obs'].value != r.cookies['_obs'].value


class TestSession(object):

    def test_it_loads_a_given_id(self):
        backend = MemoryBackend()
        backend.save('1', {'foo': 'bar'})
        backend.save('2', {'oof': 'zab'})
        s = Session({}, backend, lambda e: '3')
        s.set_id('1')
        assert s.id == s.orig_id == '1'
        assert list(s.items()) == [('foo', 'bar')]
        s.set_id('2')
        assert s.id == s.orig_id == '2'
        assert list(s.items()) == [('oof', 'zab')]


class TestCookieIdPersistence(object):

    def test_it_integrates(self):
        middleware = partial(SessionMiddleware,
                             id_persister=CookieIdPersistence(
                                 max_age=60,
                                 path='/wibble',
                                 domain='www.example.org',
                                 secure=True))

        r = Response(middleware(app(sets_a_session_key)))
        crumbs = r['set-cookie'].split(';')
        assert 'Max-Age=60' in crumbs
        assert 'Path=/wibble' in crumbs
        assert 'Domain=www.example.org' in crumbs
        assert 'Secure' in crumbs
        assert 'HttpOnly' in crumbs

    def test_it_customizes_the_cookie_name(self):
        s = 'x' * 40
        cip = CookieIdPersistence(cookie_name='fred')
        assert cip.get_id({'HTTP_COOKIE': 'fred=' + s}) == s

        session = Session({}, MemoryBackend(), lambda e: None)
        session.load()
        session.save()
        headers = []

        def app(environ, start_response):
            start_response('200 OK', headers)
            return []

        cip.set_id_middleware(session, app, {}, (lambda *args: None))
        assert headers[0][1].startswith('fred=')

    def test_it_reads_cookies_with_periods(self):
        cip = CookieIdPersistence()
        id = '.12345678901234567890123456789012345678.'
        assert cip.get_id({'HTTP_COOKIE': '_obs=' + id}) == id


class TestMemoryBackend(object):

    def test_it_expires_old_items(self):
        mb = MemoryBackend(size=5)
        data = {'a': 'b'}
        for i in range(5):
            mb.save(i, data)
        mb.save(6, data)
        assert set(mb.keys()) == {1, 2, 3, 4, 6}

    def test_accessing_items_moves_them_to_the_top(self):
        mb = MemoryBackend(size=5)
        data = {'a': 'b'}
        for i in range(5):
            mb.save(i, data)
        mb.load(0)
        mb.save(6, data)
        assert set(mb.keys()) == {0, 2, 3, 4, 6}


class TestJSONSerializer:

    def test_it_loads(self):
        buf = io.BytesIO(b'{"foo": "bar"}')
        serializer = JSONSerializer()
        assert serializer.load(buf) == {'foo': 'bar'}

    def test_it_dumps(self):
        buf = io.BytesIO()
        serializer = JSONSerializer()
        serializer.dump({'foo': 'bar'}, buf)
        assert buf.getvalue() == b'{"foo":"bar"}'

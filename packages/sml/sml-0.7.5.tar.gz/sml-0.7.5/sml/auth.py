"""Authenticate with SherlockML."""

# Copyright 2016-2018 ASI Data Science
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import time
import uuid

import click
import requests
import sml.config
import sml.version

import six.moves.configparser


class CredentialsError(Exception):
    """Exception for errors reading credentials."""

    pass


class AuthenticationError(Exception):
    """Exception for authentication errors."""

    pass


def _get_credentials_from_environ():
    """Get a SherlockML client ID and client secret from the environment."""
    try:
        client_id = os.environ['SHERLOCKML_CLIENT_ID']
    except KeyError:
        raise CredentialsError(
            'Missing SHERLOCKML_CLIENT_ID environment variable')
    try:
        client_secret = os.environ['SHERLOCKML_CLIENT_SECRET']
    except KeyError:
        raise CredentialsError(
            'Missing SHERLOCKML_CLIENT_SECRET environment variable')
    return client_id, client_secret


def _get_credential_option(parser, section, option):
    """Get a credential option from a ConfigParser."""
    try:
        return parser.get(section, option)
    except six.moves.configparser.NoSectionError:
        tpl = 'No section named "{}" found in credentials file'
        raise CredentialsError(tpl.format(section))
    except six.moves.configparser.NoOptionError:
        tpl = 'No "{}" key found in "{}" section of credentials file'
        raise CredentialsError(tpl.format(option, section))


def _credentials_file_path(directory):
    """Return the path to a credentials file."""
    xdg_config_home = os.environ.get('XDG_CONFIG_HOME')

    if not xdg_config_home:
        xdg_config_home = os.path.expanduser('~/.config')

    return os.path.join(xdg_config_home, directory, 'credentials')


def _get_credentials_from_config():
    """Read credentials from config file, warning on deprecated path."""
    deprecated_path = _credentials_file_path('sherlock')
    credentials_path = _credentials_file_path('sherlockml')

    if (os.path.exists(deprecated_path) and
            not os.path.exists(credentials_path)):
        template = ('The {} file is deprecated and will be ignored in '
                    'future.\n'
                    'You should move your credentials file to {}.\n')
        click.secho(template.format(deprecated_path, credentials_path),
                    err=True, fg='yellow')
        return _get_credentials_from_file(deprecated_path)

    return _get_credentials_from_file(credentials_path)


def _get_credentials_from_file(filename):
    """Get a SherlockML client ID and client secret from the config file."""
    parser = six.moves.configparser.SafeConfigParser()

    if not parser.read(filename):
        raise CredentialsError('No credentials file found at {}'.format(
            filename))

    section = 'default'
    if parser.has_section(sml.config.SHERLOCKML_ENV):
        section = sml.config.SHERLOCKML_ENV

    client_id = _get_credential_option(parser, section, 'client_id')
    client_secret = _get_credential_option(parser, section, 'client_secret')

    return client_id, client_secret


def _token_cache_path():
    """Return the path to a credentials file."""
    xdg_cache_dir = os.environ.get('XDG_CACHE_DIR')

    if not xdg_cache_dir:
        xdg_cache_dir = os.path.expanduser('~/.cache')

    return os.path.join(xdg_cache_dir, 'sherlockml', 'token-cache.json')


def get_credentials():
    """Get a SherlockML client ID and client secret."""
    try:
        return _get_credentials_from_environ()
    except CredentialsError:
        return _get_credentials_from_config()


def _raise_on_hudson_error(response, valid_status_codes=[200]):
    """Retrieve a description of a Hudson error."""
    if response.status_code not in valid_status_codes:
        try:
            json_response = response.json()
            error = json_response.get('error', '')
            error_description = json_response.get('error_description', '')
        except Exception:  # pylint: disable=broad-except
            error = ''
            error_description = ''
        raise AuthenticationError(
            'Failed to authenticate with SherlockML: {} {}'.format(
                error, error_description))


class TokenCache(object):
    """Disk-persisted cache for SherlockML access tokens."""

    def __init__(self):
        self._cache_path = _token_cache_path()
        self.load()

    def load(self):
        """Load the cache from disk."""
        try:
            with open(self._cache_path, 'r') as fp:
                self._store = json.load(fp)
        except Exception:  # pylint: disable=broad-except
            self._store = {}

    def commit(self):
        """Commit the cache to disk."""
        try:
            os.makedirs(os.path.dirname(self._cache_path), mode=0o700)
        except OSError:
            pass
        try:
            with open(self._cache_path, 'w') as fp:
                json.dump(self._store, fp, separators=(',', ':'))
        except Exception:  # pylint: disable=broad-except
            pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.commit()

    def add(self, client_id, token, expires_at):
        if sml.config.SHERLOCKML_ENV not in self._store:
            self._store[sml.config.SHERLOCKML_ENV] = {}
        self._store[sml.config.SHERLOCKML_ENV][client_id] = (token, expires_at)

    def get(self, client_id):
        try:
            token, expires_at = self._store[
                sml.config.SHERLOCKML_ENV][client_id]
            if expires_at is None or expires_at < time.time():
                return None
            else:
                return token
        except KeyError:
            return None


class Session(object):
    """Session with the SherlockML authentication service."""

    def __init__(self, url, client_id, client_secret):
        self._session = requests.Session()
        self.url = url
        self.client_id = client_id
        self.client_secret = client_secret
        self._user_id = None

    def _get_token(self):
        url = self.url + '/access_token'
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }
        resp = self._session.post(url, data=payload)
        _raise_on_hudson_error(resp)
        body = resp.json()
        token = body['access_token']
        expires_at = time.time() + float(body['expires_in'])
        return token, expires_at

    @property
    def token(self):
        """Get an authentication token."""
        with TokenCache() as cache:
            token = cache.get(self.client_id)
            if token is None:
                token, expires_at = self._get_token()
                cache.add(self.client_id, token, expires_at)
        return token

    def auth_headers(self):
        """Return HTTP Authorization headers."""
        return {'Authorization': 'Bearer {}'.format(self.token)}

    def _get_user_id(self):
        url = self.url + '/authenticate'
        headers = {'User-Agent': sml.version.user_agent()}
        headers.update(self.auth_headers())
        resp = self._session.get(url, headers=headers)
        _raise_on_hudson_error(resp)
        body = resp.json()
        self._user_id = uuid.UUID(body['account']['userId'])

    @property
    def user_id(self):
        """Return ID of authenticated user."""
        if self._user_id is None:
            self._get_user_id()
        return self._user_id


_hudson_session = None


def _get_session():
    global _hudson_session
    if _hudson_session is None:
        url = sml.config.hudson_url()
        client_id, client_secret = get_credentials()
        _hudson_session = Session(url, client_id, client_secret)
    return _hudson_session


def token():
    """Get authentication token."""
    session = _get_session()
    return session.token


def auth_headers():
    """Get authentication headers."""
    session = _get_session()
    return session.auth_headers()


def user_id():
    """Get session user ID."""
    session = _get_session()
    return session.user_id


def credentials_valid(client_id, client_secret):
    """Determine if the given credentials are valid."""
    url = sml.config.hudson_url()
    session = Session(url, client_id, client_secret)
    try:
        session.token
    except sml.auth.AuthenticationError:
        return False
    return True

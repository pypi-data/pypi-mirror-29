"""SMA WebConnect library for Python.

See: http://www.sma.de/en/products/monitoring-control/webconnect.html

Source: http://www.github.com/kellerza/pysma
"""
import asyncio
import json
import logging

import async_timeout

_LOGGER = logging.getLogger(__name__)

GROUP_USER = 'usr'
GROUP_INSTALLER = 'istl'

KEY_CURRENT_POWER_W = '6100_40263F00'
KEY_CURRENT_CONSUMPTION_W = '6100_00543100'
KEY_TOTAL_YIELD_KWH = '6400_00260100'
KEY_TOTAL_CONSUMPTION_KWH = '6400_00543A00'


URL_LOGIN = "{}/dyn/login.json"
URL_LOGOUT = "{}/dyn/logout.json"
URL_VALUES = "{}/dyn/getValues.json"


class SMA:
    """Class to connect to the SMA webconnect module and read parameters."""

    def __init__(self, session, url, password, group=GROUP_USER):
        """Init SMA connection."""
        self._new_session_data = {
            'right': group, 'pass': password}
        self._url = url.rstrip('/')
        if not url.startswith('http'):
            self._url = "http://" + self._url
        self._aio_session = session
        self._sma_sid = None
        self._401_error_count = 0

    @asyncio.coroutine
    def _fetch_json(self, url, payload, params=None):
        """Fetch json data for requests."""
        headers = {'content-type': 'application/json'}
        with async_timeout.timeout(3):
            res = yield from self._aio_session.post(
                url, data=json.dumps(payload), headers=headers, params=params)
            return (yield from res.json())

    @asyncio.coroutine
    def new_session(self):
        """Establish a new session."""
        try:
            res = yield from self._fetch_json(
                URL_LOGIN.format(self._url), self._new_session_data)
            self._sma_sid = res['result']['sid']
            return True
        except asyncio.TimeoutError:
            _LOGGER.error("Could not connect to SMA at %s", self._url)
        except KeyError:
            self._sma_sid = None
            if str(res.get('err', '')) == '503':
                _LOGGER.error("Max amount of sesions reached")
            else:
                _LOGGER.error("Session ID expected ['result']['sid'], got %s",
                              res)
            return False

    @asyncio.coroutine
    def close_session(self):
        """Close the session login."""
        if self._sma_sid is None:
            return
        yield from self._fetch_json(
            URL_LOGOUT.format(self._url), {}, params={'sid': self._sma_sid})
        self._sma_sid = None

    @asyncio.coroutine
    def read(self, keys):
        """Read a set of keys."""
        payload = {'destDev': [], 'keys': keys}
        if self._sma_sid is None:
            yield from self.new_session()
            if self._sma_sid is None:
                return None
        try:
            res = yield from self._fetch_json(
                URL_VALUES.format(self._url), payload=payload,
                params={'sid': self._sma_sid})
        except asyncio.TimeoutError:
            return None

        # On the first 401 error we close the session which will re-login
        if res.get('err') == 401 and self._401_error_count == 0:
            _LOGGER.warning("401 error detected, closing session to force " +
                            "another login attempt")
            self.close_session()
            self._401_error_count += 1
            return None

        try:
            _, res = res['result'].popitem()  # Only use first value
            result = []
            for key in keys:
                result.append(res[key])
        except (KeyError, TypeError) as err:
            _LOGGER.error("Unexpected return: %s - %s", res, err)
            return None

        for idx, val in enumerate(result):
            try:
                # First list item indicates result length,
                # Results are the second item in list.
                result[idx] = val.popitem()[1]
                # Extract all ['val'] values
                result[idx] = [value['val'] for value in result[idx]]
                # If only 1 item in list, remove list
                if len(result[idx]) == 1:
                    result[idx] = result[idx][0]
            except (KeyError, TypeError) as err:
                _LOGGER.error(err)

        # reset 401 error count
        self._401_error_count = 0

        return result

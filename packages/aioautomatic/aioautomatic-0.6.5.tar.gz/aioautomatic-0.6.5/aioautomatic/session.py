"""Session interface for aioautomatic."""

import asyncio
import logging

from aioautomatic import base
from aioautomatic import const
from aioautomatic import data
from aioautomatic import validation

_LOGGER = logging.getLogger(__name__)


def gen_query_string(params):
    """Generate a query string from the parameter dict."""
    return '&'.join('{}={}'.format(k, v) for k, v in params.items())


class Session(base.BaseApiObject):
    """Session object to manage access to a users information."""

    def __init__(self, client, **kwargs):
        """Create a session object."""
        super().__init__(client)
        self._client = client
        self._renew_handle = None
        self._load_token_data(**kwargs)

    def _load_token_data(self, access_token, refresh_token, expires_in, scope,
                         **kwargs):
        """Store the data from the access token response."""
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._scope = scope
        self._request_kwargs.update({
            'headers': {
                'Authorization': 'Bearer {}'.format(self._access_token),
            },
        })

        # Renew one hour before expiration
        renew_time = self.loop.time() + expires_in - 3600
        if self._renew_handle is not None:
            self._renew_handle.cancel()
        self._renew_handle = self.loop.call_at(
            renew_time, lambda: self.loop.create_task(self.refresh()))

    @asyncio.coroutine
    def refresh(self):
        """Use the refresh token to request a new access token."""
        _LOGGER.info("Refreshing the session access token.")
        auth_payload = {
            'client_id': self._client.client_id,
            'client_secret': self._client.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': self._refresh_token,
        }
        resp = yield from self._post(const.AUTH_URL, auth_payload)
        resp = validation.AUTH_TOKEN(resp)
        self._load_token_data(**resp)

    @asyncio.coroutine
    def get_vehicle(self, vehicle_id):
        """Get a single vehicle associated with this user account.

        :param vehicle_id: Vehicle ID to fetch
        """
        _LOGGER.info("Fetching vehicle.")
        resp = yield from self._get(const.VEHICLE_URL.format(vehicle_id))
        return data.Vehicle(resp)

    @asyncio.coroutine
    def get_vehicles(self, **kwargs):
        """Get all vehicles associated with this user account.

        :param created_at__lte: Maximum start time filter
        :param created_at__gte: Minimum start time filter
        :param updated_at__lte: Maximum end time filter
        :param updated_at__gte: Minimum end time filter
        :param vin: Vin filter
        :param page: Page number of paginated result to return
        :param limit: Number of results per page
        """
        query = gen_query_string(validation.VEHICLES_REQUEST(kwargs))

        _LOGGER.info("Fetching vehicles.")
        resp = yield from self._get('?'.join((const.VEHICLES_URL, query)))
        return base.ResultList(self, resp, data.Vehicle)

    @asyncio.coroutine
    def get_trip(self, trip_id):
        """Get a single trip associated with this user account.

        :param trip_id: Trip ID to fetch
        """
        _LOGGER.info("Fetching trip.")
        resp = yield from self._get(const.TRIP_URL.format(trip_id))
        return data.Trip(resp)

    @asyncio.coroutine
    def get_trips(self, **kwargs):
        """Get all vehicles associated with this user account.

        :param started_at__lte: Maximum start time filter
        :param started_at__gte: Minimum start time filter
        :param ended_at__lte: Maximum end time filter
        :param ended_at__gte: Minimum end time filter
        :param vehicle: Vehicle Filter
        :param tags__in: Tags Filter
        :param page: Page number of paginated result to return
        :param limit: Number of results per page
        """
        query = gen_query_string(validation.TRIPS_REQUEST(kwargs))

        _LOGGER.info("Fetching trips.")
        resp = yield from self._get('?'.join((const.TRIPS_URL, query)))
        return base.ResultList(self, resp, data.Trip)

    @asyncio.coroutine
    def get_device(self, device_id):
        """Get a single device associated with this user account.

        :param device_id: Device ID to fetch
        """
        _LOGGER.info("Fetching device.")
        resp = yield from self._get(const.DEVICE_URL.format(device_id))
        return data.Device(resp)

    @asyncio.coroutine
    def get_devices(self, **kwargs):
        """Get all devices associated with this user account.

        :param device__serial_number: Device serial number
        :param page: Page number of paginated result to return
        :param limit: Number of results per page
        """
        query = gen_query_string(validation.DEVICES_REQUEST(kwargs))

        _LOGGER.info("Fetching devices.")
        resp = yield from self._get('?'.join((const.DEVICES_URL, query)))
        return base.ResultList(self, resp, data.Device)

    @asyncio.coroutine
    def get_user(self, **kwargs):
        """Fetch information for the specified user.

        If no user is specified, fetch information for the authorized
        user.

        :param id: User id to fetch
        """
        user_id = validation.USER_REQUEST(kwargs).get("id", "me")

        _LOGGER.info("Fetching devices.")
        resp = yield from self._get(const.USER_URL.format(user_id))
        return data.User(self, resp)

    @property
    def refresh_token(self):
        """The refresh token used to authorize a new session."""
        return self._refresh_token

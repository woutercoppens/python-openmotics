"""Asynchronous Python client for OpenMotics."""
from __future__ import annotations
from cached_property import cached_property
from typing import TYPE_CHECKING, Any, Dict, Optional
import asyncio

if TYPE_CHECKING:
    from ...client import Api  # pylint: disable=R0401

from ...util import feature_used

from .groupactions import Groupactions
from .inputs import Inputs
from .lights import Lights
from .outputs import Outputs
from .sensors import Sensors
from .shutters import Shutters


class Installations:
    """Object holding information of the OpenMotics installation.
    {
    "id": <id>,
    "name": "<name>",
    "version": "<version>",
    "user_role": {
        "role": "ADMIN|NORMAL|APPLICATION|SUPER",
        "user_id": <user id>
    }
    "features": {
            "<feature>": {
                "available": <true|false>,
                "metadata": <optional data structure>,
                "used": <true|false>
            },
            ...
        },
        "flags": {
            "<flag>": <optional metadata structure>,
            ...
        },
        "gateway_features": [
            "<gateway feature>",
            ...
        ],
        "gateway_model": "<openmotics|overkiz>",
        "network": {
            "local_ip_address": "<ip address>"
        },
        "registration_key": "<registration key>"
    }
    """

    id: Optional[str] = None
    name: Optional[str] = None
    version: Optional[str] = None
    user_role: Optional[list[str]] = None
    features: Optional[list[str]] = None

    def __init__(self, api_client: Api = None):
        self.api_client = api_client

    @cached_property
    def groupactions(self):
        return Groupactions(api_client=self.api_client)

    @cached_property
    def inputs(self):
        return Inputs(api_client=self.api_client)

    @cached_property
    def lights(self):
        return Lights(api_client=self.api_client)

    @cached_property
    def outputs(self):
        return Outputs(api_client=self.api_client)

    @cached_property
    def sensors(self):
        return Sensors(api_client=self.api_client)

    @cached_property
    def shutters(self):
        return Shutters(api_client=self.api_client)

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Installation:
        """Return an Agreement object from a data dictionary."""
        return Installation(
            id=data.get("id"),
            name=data.get("name"),
            user_role=data.get("user_role"),
            features=data.get("features"),
        )

    async def all(
        self,
        filter: Optional[str] = None,
    ):
        """
        {
            'id': 1,
            'name': 'John Doe',
            'description': '',
            'gateway_model': 'openmotics',
            '_acl': {'configure': {'allowed': True}, 'view': {'allowed': True}, 'control': {'allowed': True}},
            '_version': 1.0,
            'user_role': {'role': 'ADMIN', 'user_id': 1},
            'registration_key': 'xxxxx-xxxx-xxxxxx-xxxxxx',
            'platform': 'CLASSIC',
            'building_roles': [],
            'version': '1.16.5',
            'network': {'local_ip_address': '172.16.1.25'},
            'flags': {'UNREAD_NOTIFICATIONS': 0, 'ONLINE': None}
        }
        """
        path = f"/base/installations"
        return await self.api_client.get(path)

    async def discovery(
        self,
    ):
        path = f"/base/discovery"
        return await self.api_client.get(path)

    async def by_id(
        self,
        installation_id: str = None,
    ):
        """ "
        {
            'id': 21,
            'name': 'John Doe',
            'description': '',
            'gateway_model': 'openmotics',
            '_acl': {'configure': {'allowed': True}, 'view': {'allowed': True}, 'control': {'allowed': True}},
            '_version': 1.0, 'user_role': {'role': 'ADMIN', 'user_id': 1},
            'registration_key': 'xxxxx-xxxxx-xxxxxxx',
            'platform': 'CLASSIC',
            'building_roles': [],
            'version': '1.16.5',
            'network': {'local_ip_address': '172.16.1.25'},
            'flags': {'UNREAD_NOTIFICATIONS': 0, 'ONLINE': None},
            'features':
                {'outputs': {'available': True, 'used': True, 'metadata': None},
                 'thermostats': {'available': True, 'used': False, 'metadata': None},
                 'energy': {'available': True, 'used': True, 'metadata': None},
                 'apps': {'available': True, 'used': False, 'metadata': None},
                 'shutters': {'available': True, 'used': False, 'metadata': None},
                 'consumption': {'available': False, 'used': False, 'metadata': None},
                 'scheduler': {'available': True, 'used': True, 'metadata': None},
                 'ems': {'available': False, 'used': False, 'metadata': None}},
                 'gateway_features': ['metrics', 'dirty_flag', 'scheduling',
                 'factory_reset', 'isolated_plugins',
                 'websocket_maintenance', 'shutter_positions',
                 'ventilation', 'default_timer_disabled',
                 '100_steps_dimmer', 'input_states']
        }
        """
        path = f"/base/installations/{installation_id}"
        return await self.api_client.get(path)

    async def status_by_id(
        self,
        installation_id: str = None,
    )  -> Optional[Dict[str, Union[bool, int, str]]]:
        """
        Function implemented to return the status of all connected devices in one call
        """
        self.status = {
            "outlets": None,
            "lights": None,
            "shutters": None,
            "groupsactions": None,
            "sensors": None,
        }
        
        # inst_features = {}
        installation = await self.by_id(installation_id=installation_id)
        inst_features = installation['features']
    
        # outlets & lights: (an output can be a light or an outlet)
        if feature_used( features=inst_features, feat_to_check='outputs'):
            outlets = None
            outlets = await self.outputs.outlets(installation_id)
            if outlets:
                self.status["outlets"] = outlets
            
            lights = None
            lights = await self.outputs.lights(installation_id)
            if lights:
                self.status["lights"] = lights
        if feature_used( features=inst_features, feat_to_check='shutters'):
            shutters = None
            shutters = await self.shutters.all(installation_id)
            if shutters:
                self.status["shutters"] = shutters

        self.status["groupactions"] = await self.groupactions.all(installation_id)

        self.status["sensors"] = await self.sensors.all(installation_id)

        print(type(self.status))

        return self.status
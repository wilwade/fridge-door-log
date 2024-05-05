"""
Basic logger for when the fridge doors open and close using gehome
"""

import aiohttp
import asyncio
import logging
from datetime import timedelta
from typing import Any, Dict, Tuple
from credentials import USERNAME, PASSWORD, REGION

from gehomesdk import (
    EVENT_ADD_APPLIANCE,
    EVENT_APPLIANCE_STATE_CHANGE,
    EVENT_APPLIANCE_INITIAL_UPDATE,
    ErdApplianceType,
    ErdCode,
    ErdDoorStatus,
    ErdCodeType,
    GeAppliance,
    GeWebsocketClient,
)

_LOGGER = logging.getLogger(__name__)

async def log_state_change(data: Tuple[GeAppliance, Dict[ErdCodeType, Any]]):
    """Log changes in appliance state"""
    _, state_changes = data
    door_status = state_changes.get(ErdCode.DOOR_STATUS)
    if door_status:
        _LOGGER.info(f'Door Change: {door_status}')
        freezer_status = door_status.freezer
        _LOGGER.info(f'Freezer status: {freezer_status}')
    
async def detect_appliance_type(appliance: GeAppliance):
    """
    Detect the appliance type.
    This should only be triggered once since the appliance type should never change.
    """
    _LOGGER.info(f'Appliance state change detected in {appliance}')


# async def do_periodic_update(appliance: GeAppliance):
#     """Request a full state update every minute forever"""
#     _LOGGER.debug(f'Registering update callback for {appliance:s}')
#     while True:
#         await asyncio.sleep(60 * 1)
#         _LOGGER.debug(f'Requesting update for {appliance:s}')
#         await appliance.async_request_update()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)-8s %(message)s')

    loop = asyncio.get_event_loop()
    client = GeWebsocketClient(USERNAME, PASSWORD, REGION, loop)
    client.add_event_handler(EVENT_APPLIANCE_INITIAL_UPDATE, detect_appliance_type)
    client.add_event_handler(EVENT_APPLIANCE_STATE_CHANGE, log_state_change)
    # client.add_event_handler(EVENT_ADD_APPLIANCE, do_periodic_update)

    session = aiohttp.ClientSession()
    asyncio.ensure_future(client.async_get_credentials_and_run(session), loop=loop)
    loop.run_until_complete(asyncio.sleep(7400))

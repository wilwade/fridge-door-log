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
#     _LOGGER.debug(f'Registering update callback for {appliance}')
#     while True:
#         await asyncio.sleep(60 * 1)
#         _LOGGER.debug(f'Requesting update for {appliance}')
#         await appliance.async_request_update()

async def main():
    while True:
        try:
            loop = asyncio.get_running_loop()
            client = GeWebsocketClient(USERNAME, PASSWORD, REGION, loop)
            client.add_event_handler(EVENT_APPLIANCE_INITIAL_UPDATE, detect_appliance_type)
            client.add_event_handler(EVENT_APPLIANCE_STATE_CHANGE, log_state_change)
            # client.add_event_handler(EVENT_ADD_APPLIANCE, do_periodic_update)
        
            async with aiohttp.ClientSession() as session:
                await client.async_get_credentials_and_run(session)
                await asyncio.sleep(7400)
        except Exception as e:
            _LOGGER.error(f"An exception occurred in main: {e}")
            await asyncio.sleep(10)  # Wait for 10 seconds before restarting

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)-8s %(message)s')

    asyncio.run(main())

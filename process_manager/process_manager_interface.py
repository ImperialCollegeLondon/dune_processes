"""Module providing functions to interact with the drunc process manager."""

import asyncio
from enum import Enum

from django.conf import settings
from drunc.process_manager.process_manager_driver import ProcessManagerDriver
from drunc.utils.shell_utils import DecodedResponse, create_dummy_token_from_uname
from druncschema.process_manager_pb2 import (
    LogRequest,
    ProcessInstanceList,
    ProcessQuery,
    ProcessUUID,
)


def get_process_manager_driver() -> ProcessManagerDriver:
    """Get a ProcessManagerDriver instance."""
    token = create_dummy_token_from_uname()
    return ProcessManagerDriver(
        settings.PROCESS_MANAGER_URL, token=token, aio_channel=True
    )


async def _get_session_info() -> ProcessInstanceList:
    pmd = get_process_manager_driver()
    query = ProcessQuery(names=[".*"])
    return await pmd.ps(query)


def get_session_info() -> ProcessInstanceList:
    """Get info about all sessions from process manager."""
    return asyncio.run(_get_session_info())


class ProcessAction(Enum):
    """Enum for process actions."""

    RESTART = "restart"
    KILL = "kill"
    FLUSH = "flush"


async def _process_call(uuids: list[str], action: ProcessAction) -> None:
    pmd = get_process_manager_driver()
    uuids_ = [ProcessUUID(uuid=u) for u in uuids]

    match action:
        case ProcessAction.RESTART:
            for uuid_ in uuids_:
                query = ProcessQuery(uuids=[uuid_])
                await pmd.restart(query)
        case ProcessAction.KILL:
            query = ProcessQuery(uuids=uuids_)
            await pmd.kill(query)
        case ProcessAction.FLUSH:
            query = ProcessQuery(uuids=uuids_)
            await pmd.flush(query)


def process_call(uuids: list[str], action: ProcessAction) -> None:
    """Perform an action on a process with a given UUID.

    Args:
        uuids: List of UUIDs of the process to be actioned.
        action: Action to be performed {restart,flush,kill}.
    """
    return asyncio.run(_process_call(uuids, action))


async def _get_process_logs(uuid: str) -> list[DecodedResponse]:
    pmd = get_process_manager_driver()
    query = ProcessQuery(uuids=[ProcessUUID(uuid=uuid)])
    request = LogRequest(query=query, how_far=100)
    return [item async for item in pmd.logs(request)]


def get_process_logs(uuid: str) -> list[DecodedResponse]:
    """Retrieve logs for a process from the process manager.

    Args:
      uuid: UUID of the process.

    Returns:
      The process logs.
    """
    return asyncio.run(_get_process_logs(uuid))


async def _boot_process(user: str, data: dict[str, str | int]) -> None:
    pmd = get_process_manager_driver()
    async for item in pmd.dummy_boot(user=user, **data):
        pass


def boot_process(user: str, data: dict[str, str | int]) -> None:
    """Boot a process with the given data.

    Args:
        user: the user to boot the process as.
        data: the data for the process.
    """
    return asyncio.run(_boot_process(user, data))

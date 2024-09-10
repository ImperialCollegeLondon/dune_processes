"""Views for the main app."""

import asyncio
import uuid

import django_tables2
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from drunc.process_manager.process_manager_driver import ProcessManagerDriver
from drunc.utils.shell_utils import create_dummy_token_from_uname
from druncschema.process_manager_pb2 import (
    ProcessInstance,
    ProcessInstanceList,
    ProcessQuery,
    ProcessUUID,
)

from .tables import ProcessTable


def get_process_manager_driver() -> ProcessManagerDriver:
    """Get a ProcessManagerDriver instance."""
    token = create_dummy_token_from_uname()
    return ProcessManagerDriver("drunc:10054", token=token, aio_channel=True)


async def get_session_info() -> ProcessInstanceList:
    """Get info about all sessions from process manager."""
    pmd = get_process_manager_driver()
    query = ProcessQuery(names=[".*"])
    return await pmd.ps(query)


def index(request: HttpRequest) -> HttpResponse:
    """View that renders the index/home page."""
    val = asyncio.run(get_session_info())

    status_enum_lookup = dict(item[::-1] for item in ProcessInstance.StatusCode.items())

    table_data = []
    process_instances = val.data.values
    for process_instance in process_instances:
        metadata = process_instance.process_description.metadata
        table_data.append(
            {
                "uuid": process_instance.uuid.uuid,
                "name": metadata.name,
                "user": metadata.user,
                "session": metadata.session,
                "status_code": status_enum_lookup[process_instance.status_code],
                "exit_code": process_instance.return_code,
            }
        )

    table = ProcessTable(table_data)

    # sort table data based on request parameters
    table_configurator = django_tables2.RequestConfig(request)
    table_configurator.configure(table)

    context = {"table": table}

    return render(request=request, context=context, template_name="main/index.html")


async def _restart_process_call(uuid: str) -> None:
    """Restart a process with a given UUID.

    Args:
        uuid: UUID of the process to be restarted.
    """
    pmd = get_process_manager_driver()
    query = ProcessQuery(uuids=[ProcessUUID(uuid=uuid)])
    await pmd.restart(query)


def restart_process(request: HttpRequest, uuid: uuid.UUID) -> HttpResponse:
    """Restart the process associated to the given UUID.

    Args:
        request: HttpRequest object. This is not used in the function, but is required
            by Django.
        uuid: UUID of the process to be restarted.

    Returns:
        HttpResponse, redirecting to the main page.
    """
    asyncio.run(_restart_process_call(str(uuid)))
    return HttpResponseRedirect(reverse("index"))


async def _kill_process_call(uuid: str) -> None:
    """Kill a process with a given UUID.

    Args:
        uuid: UUID of the process to be killed.
    """
    pmd = get_process_manager_driver()
    query = ProcessQuery(uuids=[ProcessUUID(uuid=uuid)])
    await pmd.kill(query)


def kill_process(request: HttpRequest, uuid: uuid.UUID) -> HttpResponse:
    """Kill the process associated to the given UUID.

    Args:
        request: Django HttpRequest object (unused, but required by Django).
        uuid: UUID of the process to be killed.

    Returns:
        HttpResponse redirecting to the index page.
    """
    asyncio.run(_kill_process_call(str(uuid)))
    return HttpResponseRedirect(reverse("index"))

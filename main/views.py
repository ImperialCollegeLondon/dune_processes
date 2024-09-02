"""Views for the main app."""

import asyncio

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from drunc.process_manager.process_manager_driver import ProcessManagerDriver
from drunc.utils.shell_utils import create_dummy_token_from_uname
from druncschema.process_manager_pb2 import (
    ProcessInstance,
    ProcessInstanceList,
    ProcessQuery,
)

from .tables import ProcessTable


async def get_session_info() -> ProcessInstanceList:
    """Get info about all sessions from process manager."""
    token = create_dummy_token_from_uname()
    pmd = ProcessManagerDriver("drunc:10054", token=token, aio_channel=True)
    query = ProcessQuery(names=[".*"])
    return await pmd.ps(query)


def index(request: HttpRequest) -> HttpResponse:
    """View that renders the index/home page."""
    val = asyncio.run(get_session_info())

    status_enum_lookup = dict(item[::-1] for item in ProcessInstance.StatusCode.items())

    table = []
    process_instances = val.data.values
    for process_instance in process_instances:
        metadata = process_instance.process_description.metadata
        table.append(
            {
                "uuid": process_instance.uuid.uuid,
                "name": metadata.name,
                "user": metadata.user,
                "session": metadata.session,
                "status_code": status_enum_lookup[process_instance.status_code],
                "exit_code": process_instance.return_code,
            }
        )

    context = {"table": ProcessTable(table)}

    return render(request=request, context=context, template_name="main/index.html")

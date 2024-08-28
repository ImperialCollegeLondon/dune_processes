"""Views for the main app."""

import asyncio

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from drunc.process_manager.process_manager_driver import ProcessManagerDriver
from drunc.utils.shell_utils import create_dummy_token_from_uname
from druncschema.process_manager_pb2 import ProcessInstanceList, ProcessQuery


async def get_session_info() -> ProcessInstanceList:
    """Get info about all sessions from process manager."""
    token = create_dummy_token_from_uname()
    pmd = ProcessManagerDriver("drunc:10054", token=token, aio_channel=True)
    query = ProcessQuery(names=[".*"])
    return await pmd.ps(query)


def index(request: HttpRequest) -> HttpResponse:
    """View that renders the index/home page."""
    val = asyncio.run(get_session_info())
    context = {"values": val.data.values}

    return render(request=request, context=context, template_name="main/index.html")

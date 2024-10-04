"""Views for the process_manager app."""

import asyncio
import uuid
from enum import Enum

import django_tables2
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
from drunc.process_manager.process_manager_driver import ProcessManagerDriver
from drunc.utils.shell_utils import DecodedResponse, create_dummy_token_from_uname
from druncschema.process_manager_pb2 import (
    LogRequest,
    ProcessInstance,
    ProcessInstanceList,
    ProcessQuery,
    ProcessUUID,
)

from .forms import BootProcessForm
from .tables import ProcessTable


def get_process_manager_driver() -> ProcessManagerDriver:
    """Get a ProcessManagerDriver instance."""
    token = create_dummy_token_from_uname()
    return ProcessManagerDriver(
        settings.PROCESS_MANAGER_URL, token=token, aio_channel=True
    )


async def get_session_info() -> ProcessInstanceList:
    """Get info about all sessions from process manager."""
    pmd = get_process_manager_driver()
    query = ProcessQuery(names=[".*"])
    return await pmd.ps(query)


@login_required
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

    with transaction.atomic():
        # atomic to avoid race condition with kafka consumer
        messages = request.session.load().get("messages", [])
        request.session.pop("messages", [])
        request.session.save()

    context = {"table": table, "messages": messages}
    return render(
        request=request, context=context, template_name="process_manager/index.html"
    )


class ProcessAction(Enum):
    """Enum for process actions."""

    RESTART = "restart"
    KILL = "kill"
    FLUSH = "flush"


async def _process_call(uuids: list[str], action: ProcessAction) -> None:
    """Perform an action on a process with a given UUID.

    Args:
        uuids: List of UUIDs of the process to be actioned.
        action: Action to be performed {restart,flush,kill}.
    """
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


@login_required
@permission_required("main.can_modify_processes", raise_exception=True)
def process_action(request: HttpRequest) -> HttpResponse:
    """Perform an action on the selected processes.

    Both the action and the selected processes are retrieved from the request.

    Args:
        request: Django HttpRequest object.

    Returns:
        HttpResponse redirecting to the index page.
    """
    try:
        action = request.POST.get("action", "")
        action_enum = ProcessAction(action.lower())
    except ValueError:
        return HttpResponseRedirect(reverse("process_manager:index"))

    if uuids_ := request.POST.getlist("select"):
        asyncio.run(_process_call(uuids_, action_enum))
    return HttpResponseRedirect(reverse("process_manager:index"))


async def _get_process_logs(uuid: str) -> list[DecodedResponse]:
    """Retrieve logs for a process from the process manager.

    Args:
      uuid: UUID of the process.

    Returns:
      The process logs.
    """
    pmd = get_process_manager_driver()
    query = ProcessQuery(uuids=[ProcessUUID(uuid=uuid)])
    request = LogRequest(query=query, how_far=100)
    return [item async for item in pmd.logs(request)]


@login_required
@permission_required("main.can_view_process_logs", raise_exception=True)
def logs(request: HttpRequest, uuid: uuid.UUID) -> HttpResponse:
    """Display the logs of a process.

    Args:
      request: the triggering request.
      uuid: identifier for the process.

    Returns:
      The rendered page.
    """
    logs_response = asyncio.run(_get_process_logs(str(uuid)))
    context = dict(log_text="\n".join(val.data.line for val in logs_response))
    return render(
        request=request, context=context, template_name="process_manager/logs.html"
    )


async def _boot_process(user: str, data: dict[str, str | int]) -> None:
    """Boot a process with the given data.

    Args:
        user: the user to boot the process as.
        data: the data for the process.
    """
    pmd = get_process_manager_driver()
    async for item in pmd.dummy_boot(user=user, **data):
        pass


class BootProcessView(PermissionRequiredMixin, FormView):  # type: ignore [type-arg]
    """View for the BootProcess form."""

    template_name = "process_manager/boot_process.html"
    form_class = BootProcessForm
    success_url = reverse_lazy("process_manager:index")
    permission_required = "main.can_modify_processes"

    def form_valid(self, form: BootProcessForm) -> HttpResponse:
        """Boot a Process when valid form data has been POSTed.

        Args:
            form: the form instance that has been validated.

        Returns:
            A redirect to the index page.
        """
        asyncio.run(_boot_process("root", form.cleaned_data))
        return super().form_valid(form)

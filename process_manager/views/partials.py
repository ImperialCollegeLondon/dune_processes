"""View functions for partials."""

import django_tables2
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from druncschema.process_manager_pb2 import (
    ProcessInstance,
)

from ..process_manager_interface import get_session_info
from ..tables import ProcessTable


@login_required
def process_table(request: HttpRequest) -> HttpResponse:
    """Renders the process table.

    This view may be called using either GET or POST methods. GET renders the table with
    no check boxes selected. POST renders the table with checked boxes for any table row
    with a uuid provided in the select key of the request data.
    """
    selected_rows = request.POST.getlist("select", [])
    session_info = get_session_info()

    status_enum_lookup = dict(item[::-1] for item in ProcessInstance.StatusCode.items())

    table_data = []
    process_instances = session_info.data.values
    for process_instance in process_instances:
        metadata = process_instance.process_description.metadata
        uuid = process_instance.uuid.uuid
        table_data.append(
            {
                "uuid": uuid,
                "name": metadata.name,
                "user": metadata.user,
                "session": metadata.session,
                "status_code": status_enum_lookup[process_instance.status_code],
                "exit_code": process_instance.return_code,
                "checked": (uuid in selected_rows),
            }
        )
    table = ProcessTable(table_data)

    # sort table data based on request parameters
    table_configurator = django_tables2.RequestConfig(request)
    table_configurator.configure(table)

    return render(
        request=request,
        context=dict(table=table),
        template_name="process_manager/partials/process_table.html",
    )

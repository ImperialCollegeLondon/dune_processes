"""View functions for pages."""

import uuid

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from ..forms import BootProcessForm
from ..process_manager_interface import boot_process, get_process_logs


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """View that renders the index/home page."""
    return render(request=request, template_name="process_manager/index.html")


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
    logs_response = get_process_logs(str(uuid))
    context = dict(log_text="\n".join(val.data.line for val in logs_response))
    return render(
        request=request, context=context, template_name="process_manager/logs.html"
    )


class BootProcessView(PermissionRequiredMixin, FormView[BootProcessForm]):
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
        boot_process("root", form.cleaned_data)
        return super().form_valid(form)

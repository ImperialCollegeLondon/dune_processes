"""View functions for performing actions on DUNE processes."""

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse

from ..process_manager_interface import ProcessAction, process_call


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
        process_call(uuids_, action_enum)
    return HttpResponseRedirect(reverse("process_manager:index"))

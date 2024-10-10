"""Views for the main app."""

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """View that renders the index/home page."""
    return render(request=request, template_name="main/index.html")


class HelpView(View):
    """View that renders the help page."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Render the help page."""
        return render(request=request, template_name="main/help.html")

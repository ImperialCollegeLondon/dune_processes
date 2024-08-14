"""Views for the main app."""

from django.shortcuts import render


def index(request):
    """View that renders the index/home page."""
    return render(request=request, template_name="main/index.html")

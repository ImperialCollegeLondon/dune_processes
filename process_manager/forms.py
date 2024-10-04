"""Forms for the process_manager app."""

from django import forms


class BootProcessForm(forms.Form):
    """Form for booting processes."""

    session_name = forms.CharField()
    n_processes = forms.IntegerField()
    sleep = forms.IntegerField()
    n_sleeps = forms.IntegerField()
